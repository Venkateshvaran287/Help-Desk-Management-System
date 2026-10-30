# IT Help Desk Management System

A web-based version of a Python list-based IT Help Desk Management System, built with Flask.

## Features
- Create support tickets
- View all tickets
- Search tickets by ID
- Update ticket status, priority and problem description
- Delete tickets
- Dashboard statistics for ticket status and priority

## Technologies
- Python
- Flask
- HTML
- CSS
- Python list (in-memory ticket storage)

## Run locally
1. Install Python.
2. Open this project folder in a terminal.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   python app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser.

## Important note about data
This beginner/demo version stores tickets in a Python list in application memory. Tickets are temporary and will be cleared when the app restarts. For a production application, use a database such as SQLite or MySQL.

## Deployment
Push this folder to a public GitHub repository and connect that repository to a Python-compatible hosting service. The included `requirements.txt` and `Procfile` provide the basic deployment configuration.
