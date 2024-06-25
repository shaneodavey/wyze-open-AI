from flask import Flask, request
import time
import speech_recognition as sr
import pyttsx3
import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize Flask app
app = Flask(__name__)

# OpenAI API key
openai.api_key = 'your-openai-api-key'

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def speak(message):
    tts_engine.say(message)
    tts_engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def chatgpt_response(prompt):
    response = openai.Completion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def send_notification(subject, body):
    sender_email = "your-email@example.com"
    receiver_email = "receiver-email@example.com"
    password = "your-email-password"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.example.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.close()
        print("Notification sent successfully")
    except Exception as e:
        print(f"Failed to send notification: {e}")

@app.route('/motion_detected', methods=['POST'])
def motion_detected():
    data = request.json
    if data and data.get('event') == 'motion detected':
        speak("Attention, you are now being recorded. Do you have a message for the householder?")
        message = listen()
        if message:
            gpt_response = chatgpt_response(f"Visitor message: {message}")
            speak(f"Message received: {gpt_response}")
            send_notification("New Visitor Message", f"Message: {message}\nResponse: {gpt_response}")
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
