import json
import os
from flask_mail import Mail, Message
import google.generativeai as genai
from flask import Flask, jsonify, request, send_file, send_from_directory


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "b.rammadhav@gmail.com" # Replace with your Gmail address
app.config['MAIL_PASSWORD'] = "vtopbkngcumofrxh"  # Replace with your Gmail password
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

mail = Mail(app)


# 🔥🔥 FILL THIS OUT FIRST! 🔥🔥
# Get your Gemini API key by:
# - Selecting "Add Gemini API" in the "Project IDX" panel in the sidebar
# - Or by visiting https://g.co/ai/idxGetGeminiKey

todo='AIzaSyCfduMssiW87ji2fPOOE0IXGGtIKXp5YX0' # replace with api key
API_KEY = todo

genai.configure(api_key=API_KEY)




@app.route("/")
def index():
    return send_file('web/index.html')


@app.route("/api/generate", methods=["POST"])
def generate_api():
    if request.method == "POST":
        if API_KEY =="todo":
            return jsonify({ "error": '''
                To get started, get an API key at
                https://g.co/ai/idxGetGeminiKey and enter it in
                main.py
                '''.replace('\n', '') })
        try:
            req_body = request.get_json()
            content = req_body.get("contents")
            model = genai.GenerativeModel(model_name=req_body.get("model"))
            response = model.generate_content(content, stream=True)
            def stream():
                for chunk in response:
                    yield 'data: %s\n\n' % json.dumps({ "text": chunk.text })

            return stream(), {'Content-Type': 'text/event-stream'}

        except Exception as e:
            return jsonify({ "error": str(e) })

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        # Extract data from the request
        recipient = request.form['recipient_email']
        subject = request.form['subject']
        body = request.form['message']

        # Create and send the email
        msg = Message(subject=subject,
                      recipients=[recipient],
                      body=body)
        mail.send(msg)
        return jsonify({"success": "Email sent successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})



@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)


if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 3000)))
