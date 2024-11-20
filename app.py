from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai
import subprocess

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

# Ana sayfa
@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Metin Üret ve Shell Ekranı</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            <style>
                body {
                    background-color: #f0f2f5;
                    font-family: Arial, sans-serif;
                }
                .container {
                    margin-top: 50px;
                    max-width: 600px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                }
                h1 {
                    color: #343a40;
                    margin-bottom: 20px;
                    text-align: center;
                }
                .form-group input {
                    border-radius: 8px;
                    border: 1px solid #ced4da;
                    padding: 10px;
                }
                .btn-primary {
                    background-color: #007bff;
                    border-color: #007bff;
                    border-radius: 8px;
                }
                .btn-primary:hover {
                    background-color: #0056b3;
                    border-color: #0056b3;
                }
                pre {
                    background-color: #e9ecef;
                    padding: 10px;
                    border-radius: 8px;
                    max-height: 300px;
                    overflow-y: auto;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Metin Üret ve Shell Ekranı</h1>
                
                <h3>Metin Üret</h3>
                <form id="generateForm">
                    <div class="form-group">
                        <input type="text" name="input" class="form-control" placeholder="Metin girin..." required>
                    </div>
                    <button type="submit" class="btn btn-primary btn-block">Üret</button>
                </form>
                <pre id="generateResponse"></pre>

                <h3>Shell Ekranı</h3>
                <form action="/execute" method="post">
                    <div class="form-group">
                        <input type="text" name="command" class="form-control" placeholder="Komut girin..." required>
                    </div>
                    <button type="submit" class="btn btn-primary btn-block">Çalıştır</button>
                </form>
                <pre>{{ output }}</pre>
            </div>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script>
                $(document).ready(function() {
                    $('#generateForm').on('submit', function(event) {
                        event.preventDefault();
                        $.ajax({
                            url: '/generate',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify({input: $('input[name="input"]').val()}),
                            success: function(data) {
                                $('#generateResponse').text(data.response);
                            },
                            error: function() {
                                $('#generate Response').text('Bir hata oluştu. Lütfen tekrar deneyin.');
                            }
                        });
                    });
                });
            </script>
        </body>
        </html>
    ''', output='')

# Metin üretme
@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.json.get('input')
    prompt = f"Kendini siber güvenlik uzmanı gibi düşünerek soruyu cevapla: '{user_input}'"
    
    # Modeli kullanarak yanıt oluşturma
    response = model.generate_content(prompt)
    return jsonify({'response': response.text})

# Komut çalıştırma
@app.route('/execute', methods=['POST'])
def execute():
    command = request.form['command']
    try:
        # Komutu çalıştır ve çıktısını al
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Metin Üret ve Shell Ekranı</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            <style>
                body {
                    background-color: #f0f2f5;
                    font-family: Arial, sans-serif;
                }
                .container {
                    margin-top: 50px;
                    max-width: 600px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                }
                h1 {
                    color: #343a40;
                    margin-bottom: 20px;
                    text-align: center;
                }
                .form-group input {
                    border-radius: 8px;
                    border: 1px solid #ced4da;
                    padding: 10px;
                }
                .btn-primary {
                    background-color: #007bff;
                    border-color: #007bff;
                    border-radius: 8px;
                }
                .btn-primary:hover {
                    background-color: #0056b3;
                    border-color: #0056b3;
                }
                pre {
                    background-color: #e9ecef;
                    padding: 10px;
                    border-radius: 8px;
                    max-height: 300px;
                    overflow-y: auto;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Metin Üret ve Shell Ekranı</h1>
                <h3>Metin Üret</h3>
                <form id="generateForm">
                    <div class="form-group">
                        <input type="text" name="input" class="form-control" placeholder="Metin girin..." required>
                    </div>
                    <button type="submit" class="btn btn-primary btn-block">Üret</button>
                </form>
                <pre id="generateResponse">{{ output }}</pre>

                <h3>Shell Ekranı</h3>
                <form action="/execute" method="post">
                    <div class="form-group">
                        <input type="text" name="command" class="form-control" placeholder="Komut girin..." required>
                    </div>
                    <button type="submit" class="btn btn-primary btn-block">Çalıştır</button>
                </form>
                <pre>{{ output }}</pre>
            </div>
        </body>
        </html>
    ''', output=output)

if __name__ == '__main__':
    app.run(debug=True)
