# wyze-open-AI
Utilize the Wyze camera's motion detection as a trigger to initiate processes on a more capable device like a Raspberry Pi
High-Level Workflow
Wyze Camera with Motion Detection: Use the camera's built-in motion detection to trigger an event.
Trigger Raspberry Pi Actions: When motion is detected, the camera sends a notification (e.g., via an HTTP request, IFTTT, or webhook) to the Raspberry Pi.
Raspberry Pi Processes: The Raspberry Pi handles the complex tasks like ChatGPT integration and sending notifications.

Step-by-Step Implementation


1. Wyze Camera Setup
Enable Motion Detection: Ensure motion detection is enabled in the Wyze app.

IFTTT Integration: Use IFTTT to trigger an HTTP request when motion is detected.

Create an IFTTT Applet:

IF This: Wyze Motion Detected
Then That: Webhooks - Make a web request
Configure the Webhook:

URL: Endpoint on your Raspberry Pi (e.g., http://<raspberry_pi_ip>:5000/motion_detected)
Method: POST
Content Type: application/json
Body: { "camera": "Wyze Camera", "event": "motion detected" }

2. Raspberry Pi Setup
Install Required Libraries:

bash
pip install flask openai pyttsx3 SpeechRecognition smtplib

Python Script for Raspberry Pi:

Flask Server: To handle incoming webhook requests from IFTTT.
ChatGPT and Notification Logic: As previously outlined.

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
   
Explanation
Flask Server: The Raspberry Pi runs a Flask server to listen for webhook requests from IFTTT.
Motion Detection Trigger: When the Wyze camera detects motion, IFTTT sends a POST request to the Raspberry Pi's Flask server.
Processing: Upon receiving the motion detection trigger, the Raspberry Pi runs the logic to interact with ChatGPT and send notifications.
Additional Steps
Replace Placeholders:
OpenAI API key, email credentials, and settings.
Network Configuration: Ensure the Raspberry Pi is accessible on the network and can receive HTTP requests from IFTTT.
Testing: Test the entire workflow to ensure the motion detection trigger correctly initiates the Flask endpoint and subsequent processes.
This approach leverages the capabilities of the Wyze camera for motion detection and offloads the heavy processing tasks to a more capable device like a Raspberry Pi.






