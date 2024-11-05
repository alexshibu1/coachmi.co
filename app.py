# Add this to the top of your app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse
from retrieval_system import generate_response  # Assuming this function is correct and exists

app = Flask(__name__)
CORS(app)

# Dictionary to keep user sessions and track conversation flow
user_sessions = {}

def get_or_create_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = {"responses": []}
    return user_sessions[user_id]

# Function to handle user query
def handle_query(user_id, message_body):
    session = get_or_create_session(user_id)
    session["responses"].append(message_body)
    return generate_advice_from_responses(session["responses"])

# Function to generate advice in a casual, strong coaching tone
def generate_advice_from_responses(responses):
    # Casual, straight-to-the-point prompt for AI model
    prompt = "You’re a startup coach with a strong, no-nonsense style. Here’s what the user has shared so far:\n"
    for i, response in enumerate(responses, 1):
        prompt += f"{i}. {response}\n"
    prompt += (
        "Based on this info, give your best, no-nonsense advice. No fluffy or corporate jargon—just "
        "straight-to-the-point guidance on getting users, building traction, and making an impact. "
        "Keep it actionable, and only include resources if they're useful for what the user needs right now."
    )
    
    # Generate advice from AI model
    advice = generate_response(prompt)  # Replace with your actual model function
    return advice

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat_reply():
    if request.method == 'OPTIONS':
        response = app.response_class(status=200)
        response.headers.add("Access-Control-Allow-Origin", "*")  # Allow all origins
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.json
    user_id = data.get("user_id")
    message_body = data.get("message").strip()

    # Use handle_query to process the user input
    response_text = handle_query(user_id, message_body)
    return jsonify({"reply": response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
