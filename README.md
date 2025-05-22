# Sydney Events Scraper

A web application that scrapes and displays upcoming events in Sydney, with email capture functionality for ticket requests.

## Features

- Scrapes events from Eventbrite Sydney
- Displays events in a modern, responsive grid layout
- Email capture modal for ticket requests
- Automatic event updates every hour
- Persistent storage of events in JSON format

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

- `app.py`: Flask application with API endpoints
- `scraper.py`: Event scraping functionality
- `templates/index.html`: Frontend interface
- `events.json`: Persistent storage for scraped events
- `requirements.txt`: Project dependencies

## Notes

- The scraper runs automatically every hour to update the event list
- Email submissions are currently logged to the console (you can extend this to save to a database)
- The application uses Bootstrap 5 for styling 