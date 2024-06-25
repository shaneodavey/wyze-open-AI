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






