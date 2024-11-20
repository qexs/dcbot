from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Google Generative AI API anahtarınızı burada ayarlayın
genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel('gemini-pro',
    safety_settings=[
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.json.get('input')
    prompt = f"Kendini siber güvenlik uzmanı gibi düşünerek soruyu cevapla: '{user_input}'"
    
    # Modeli kullanarak yanıt oluşturma
    response = model.generate_content(prompt)
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)
