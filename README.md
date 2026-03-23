🔥 Google Calendar API Project

📌 Overview

This project demonstrates integration with the Google Calendar API using OAuth2 authentication and Flask-based REST endpoints.

⚙️ Features
OAuth2 authentication flow
List upcoming calendar events
Create new calendar events
Token persistence (token.json)
Modular service architecture


🛠️ Tech Stack
Python
Flask
Google Calendar API
OAuth2


🚀 How to Run (2-minute setup)


git clone <your-repo>
cd calendar-api
pip install -r requirements.txt
python app.py



🔑 Setup Google Credentials
Go to Google Cloud Console
Create OAuth Client (Desktop App)
Download credentials.json
Place it in root folder


▶️ Test Endpoints

Open browser:

http://127.0.0.1:5000/calendar_test_list

Create event:

curl -X POST http://127.0.0.1:5000/calendar_test_create

🧪 First Run
Browser will open → Google login
Accept permissions
token.json will be created


⚠️ Notes
Only test users can access the app (OAuth limitation)
Token expires → re-auth required

Example use cases:

Meeting scheduler backend
Appointment booking system
Personal productivity automation
AI assistant calendar integration