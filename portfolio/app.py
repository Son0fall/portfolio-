from flask import Flask, request, jsonify
from flask_cors import CORS
from googletrans import Translator
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
translator = Translator()

# Knowledge base for chatbot responses
KNOWLEDGE_BASE = {
    "greeting": "Hello! How can I help you today?",
    "contact": "You can contact Njabulo via email at njabulomavuso0271@gmail.com or phone at (+268) 78361103. You can also use the contact form on this website.",
    "projects": "Njabulo has worked on several projects including e-commerce platforms, university portals, and government dashboards. You can view them in the Projects section!",
    "experience": "Njabulo has experience as an IT Support Technician at Future Focus Electronics, Full-stack Developer at Limkokwing University, and currently works at the Ministry of Economic Planning & Development.",
    "skills": "Njabulo has skills in programming, web development, database management, problem solving, and team collaboration. Check the Skills section for more details.",
    "education": "Njabulo completed his Form 5 at Ebenezer FEA High School in 2021 and earned an Associate Degree in Information Technology from Limkokwing University with a GPA of 3.46.",
    "help": "I can help you with information about Njabulo's skills, experience, projects, and how to contact him. Just ask!",
    "thanks": "You're welcome! Let me know if you have any other questions.",
    "name": "I'm a chatbot assistant for Njabulo Mavuso. I can help answer questions about his portfolio and experience.",
    "bye": "Goodbye! Feel free to return if you have more questions.",
    "default": "I'm sorry, I didn't understand that. Could you please rephrase? You can ask about Njabulo's skills, experience, projects, or how to contact him."
}

# Keywords for intent recognition
KEYWORDS = {
    "greeting": ["hello", "hi", "hey", "hola", "howdy"],
    "contact": ["contact", "email", "phone", "reach", "number", "get in touch"],
    "projects": ["project", "work", "portfolio", "github", "show me your work"],
    "experience": ["experience", "job", "work history", "career", "background"],
    "skills": ["skill", "ability", "expertise", "knowledge", "what can you do"],
    "education": ["education", "study", "school", "university", "degree"],
    "help": ["help", "assist", "support", "what can you do"],
    "thanks": ["thank", "thanks", "appreciate", "grateful"],
    "name": ["name", "who are you", "your name"],
    "bye": ["bye", "goodbye", "see you", "later"]
}

def process_message(message):
    """Process user message and generate appropriate response"""
    message = message.lower()
    
    # Check each category
    for intent, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in message:
                return KNOWLEDGE_BASE[intent]
    
    # Special cases
    if "hire" in message:
        return "If you're interested in hiring Njabulo, please click the 'Hire Me' button on the website or use the contact form."
    
    if "reference" in message:
        return "Njabulo has several professional references. You can find them in the References section of this website."
    
    if "devops" in message or "server" in message:
        return "Njabulo specializes in DevOps practices and server administration. He has experience with cloud computing, automation, and server management."
    
    return KNOWLEDGE_BASE["default"]

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()
        lang = data.get('lang', 'en')

        if not user_input:
            return jsonify({'error': 'Empty message received.'}), 400

        # Detect language of the input
        detected_lang = translator.detect(user_input).lang

        # Translate to English if needed
        english_input = translator.translate(user_input, dest='en').text if detected_lang != 'en' else user_input

        # Process the message with NLP
        english_response = process_message(english_input)

        # Translate response to requested language
        translated_response = translator.translate(english_response, dest=lang).text if lang != 'en' else english_response

        return jsonify({
            'original': english_response,
            'translated': translated_response
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Chatbot API is running!"

if __name__ == '__main__':
    app.run(port=5000, debug=True)