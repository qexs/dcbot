from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai
import subprocess

app = Flask(__name__)

# Google Generative AI API anahtarınızı burada ayarlayın
genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel(
    "gemini-pro",
    safety_settings=[
        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ],
)

# Ana sayfa
@app.route("/")
def index():
    return render_template_string(
        '''
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Hacker Arayüzü</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            <style>
                body {
                    background-color: #0d0d0d;
                    color: #00ff00;
                    font-family: 'Courier New', Courier, monospace;
                    text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00;
                }
                .container {
                    margin-top: 50px;
                    max-width: 800px;
                    background: #1e1e1e;
                    border-radius: 10px;
                    box-shadow: 0 0 20px #00ff00;
                    padding: 20px;
                }
                h1, h3 {
                    color: #00ff00;
                    text-align: center;
                }
                .form-group input, button {
                    border-radius: 8px;
                }
                .form-group input {
                    background: #333333;
                    color: #00ff00;
                    border: 1px solid #00ff00;
                }
                .btn-primary {
                    background-color: #00ff00;
                    border-color: #00ff00;
                    color: #000;
                    font-weight: bold;
                }
                .btn-primary:hover {
                    background-color: #00cc00;
                    border-color: #00cc00;
                }
                pre {
                    background: #0d0d0d;
                    color: #00ff00;
                    border: 1px solid #00ff00;
                    padding: 15px;
                    border-radius: 10px;
                    max-height: 300px;
                    overflow-y: auto;
                    box-shadow: 0 0 10px #00ff00;
                }
                .footer {
                    text-align: center;
                    color: #007bff;
                    margin-top: 30px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>💻 Hacker Arayüzü 💻</h1>

                <h3>⚡ Metin Üret ⚡</h3>
                <form id="generateForm">
                    <div class="form-group">
                        <input type="text" name="input" class="form-control" placeholder="Metin girin..." required>
                    </div>
                    <button type="submit" class="btn btn-primary btn-block">Üret</button>
                </form>
                <pre id="generateResponse"></pre>

                <h3>💀 Shell Ekranı 💀</h3>
                <form action="/shell" method="get">
                    <button type="submit" class="btn btn-primary btn-block">Shell Ekranına Git</button>
                </form>

                <h3>🔥 PentestGPT 🔥</h3>
                <form action="/pentestgpt" method="get">
                    <button type="submit" class="btn btn-primary btn-block">PentestGPT Ekranına Git</button>
                </form>

                <div class="footer">
                    <p>⚠️ Yalnızca Yetkili ve Etik Kullanım İçindir ⚠️</p>
                </div>
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
                                $('#generateResponse').text('Bir hata oluştu. Lütfen tekrar deneyin.');
                            }
                        });
                    });
                });
            </script>
        </body>
        </html>
        '''
    )


# Metin üretme
@app.route("/generate", methods=["POST"])
def generate():
    user_input = request.json.get("input")
    prompt = f"Kendini bir siber güvenlik uzmanı gibi düşünerek soruyu yanıtla: '{user_input}'"
    response = model.generate_content(prompt)
    return jsonify({"response": response.text})


# Shell ekranı
@app.route("/shell")
def shell():
    return render_template_string(
        '''
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <title>💀 Shell Ekranı 💀</title>
            <style>
                body {
                    background-color: #0d0d0d;
                    color: #00ff00;
                    font-family: 'Courier New', Courier, monospace;
                }
                .container {
                    margin: 50px auto;
                    max-width: 600px;
                    text-align: center;
                }
                input {
                    background: #333333;
                    color: #00ff00;
                    border: 1px solid #00ff00;
                    padding: 10px;
                    width: 100%;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }
                button {
                    background-color: #00ff00;
                    color: #000;
                    font-weight: bold;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #00cc00;
                }
                pre {
                    background: #0d0d0d;
                    padding: 15px;
                    border: 1px solid #00ff00;
                    border-radius: 8px;
                    color: #00ff00;
                    overflow-y: auto;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Shell Ekranı</h1>
                <form action="/execute" method="post">
                    <input type="text" name="command" placeholder="Komut girin..." required>
                    <button type="submit">Çalıştır</button>
                </form>
            </div>
        </body>
        </html>
        '''
    )


@app.route("/execute", methods=["POST"])
def execute():
    command = request.form.get("command")
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    return f"<pre>{output}</pre>"


# PentestGPT ekranı
@app.route("/pentestgpt")
def pentestgpt():
    return render_template_string(
        '''
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PentestGPT</title>
            <style>
                body {
                    background-color: #0d0d0d;
                    color: #00ff00;
                    font-family: 'Courier New', Courier, monospace;
                }
                .container {
                    margin: 50px auto;
                    max-width: 600px;
                    text-align: center;
                }
                input {
                    background: #333333;
                    color: #00ff00;
                    border: 1px solid #00ff00;
                    padding: 10px;
                    width: 100%;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }
                button {
                    background-color: #00ff00;
                    color: #000;
                    font-weight: bold;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #00cc00;
                }
                pre {
                    background: #0d0d0d;
                    padding: 15px;
                    border: 1px solid #00ff00;
                    border-radius: 8px;
                    color: #00ff00;
                    overflow-y: auto;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>PentestGPT</h1>
                <p>Penetrasyon testleri için sorularınızı buraya yazabilirsiniz.</p>
                <form id="pentestForm">
                    <input type="text" name="input" placeholder="Sorunuzu girin..." required>
                    <button type="submit">Sor</button>
                </form>
                <pre id="pentestResponse"></pre>
            </div>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script>
                $(document).ready(function() {
                    $('#pentestForm').on('submit', function(event) {
                        event.preventDefault();
                        $.ajax({
                            url: '/generate',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify({input: $('input[name="input"]').val()}),
                            success: function(data) {
                                $('#pentestResponse').text(data.response);
                            },
                            error: function() {
                                $('#pentestResponse').text('Bir hata oluştu. Lütfen tekrar deneyin.');
                            }
                        });
                    });
                });
            </script>
        </body>
        </html>
        '''
    )


if __name__ == "__main__":
    app.run(debug=True)
