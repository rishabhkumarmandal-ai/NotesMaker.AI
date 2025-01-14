from flask import Flask, request, jsonify
import openai
import requests
import schedule
import time
import threading

app = Flask(__name__)

# Set up OpenAI API
openai.api_key = "your_openai_api_key"
# User data storage
user_data = {}

# Function to proactively message users
def send_proactive_message():
    global user_data
    for user_id in user_data:
        print(f"Proactive Message: Hi {user_data[user_id]['name']}, how can I help you with your studies today?")
        # Additional messaging logic (email, notification, etc.) can be added here

def schedule_proactive_messages():
    schedule.every().day.at("09:00").do(send_proactive_message)  # Adjust the time as needed
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=schedule_proactive_messages, daemon=True).start()

# Function to fetch GATE questions (Dummy implementation)
def get_gate_questions(topic):
    return [f"Sample question for {topic}", "Question 2", "Question 3"]

# Function to fetch YouTube links
def get_youtube_links(topic):
    youtube_api_key = "your_youtube_api_key"
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={topic}&key={youtube_api_key}&maxResults=5"
    response = requests.get(search_url)
    videos = response.json().get("items", [])
    return [f"https://www.youtube.com/watch?v={video['id']['videoId']}" for video in videos if video.get("id", {}).get("videoId")]

# Function to fetch GeeksforGeeks links
def get_gfg_links(topic):
    search_url = f"https://geeksforgeeks.org/search?q={topic}"
    return [search_url]  # Placeholder for GFG scraping logic

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id")
    message = data.get("message")

    if user_id not in user_data:
        user_data[user_id] = {"name": f"User {user_id}"}

    # Check for topic-based queries
    if "topic" in message.lower():
        topic = message.split(":")[1].strip()  # Extract the topic
        gate_questions = get_gate_questions(topic)
        youtube_links = get_youtube_links(topic)
        gfg_links = get_gfg_links(topic)

        response = {
            "message": f"Here is some material for the topic '{topic}':",
            "gate_questions": gate_questions,
            "youtube_links": youtube_links,
            "gfg_links": gfg_links,
        }
        return jsonify(response)

    # Default response using OpenAI GPT
    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
    )
    return jsonify({"message": gpt_response["choices"][0]["message"]["content"]})

if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")

# Existing chatbot logic...

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
