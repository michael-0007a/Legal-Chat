from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

API_KEY = "API_KEY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "Greetings! I'm your Indian legal chatbot. Feel free to ask me any questions related to Indian law. I'm unable to answer questions on other topics."}
    ]
)

def is_legal_query(response):
    legal_keywords = ["law", "legal", "act", "court", "rights", "crime", "section", "penalty", "contract", "jurisdiction", "justice", "indian", "constitution"]
    return any(keyword in response.lower() for keyword in legal_keywords)

def format_response(text):
    formatted_text = text.replace("**", "<strong>").replace("**", "</strong>")
    formatted_text = formatted_text.replace("*", "<em>").replace("*", "</em>")
    formatted_text = formatted_text.replace("\n", "<br>")
    
    return formatted_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_with_bot():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    
    response = chat.send_message(user_input)
    
    if is_legal_query(response.text):
        formatted_response = format_response(response.text)
        return jsonify({"response": formatted_response})
    else:
        return jsonify({"response": "I can only answer questions related to legal queries. Please ask about Indian law."})

if __name__ == "__main__":
    app.run(debug=True, port=8080)


