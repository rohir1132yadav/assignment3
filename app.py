from flask import Flask, jsonify, render_template, request, redirect
from apscheduler.schedulers.background import BackgroundScheduler
from scraper import EventScraper
import os

app = Flask(__name__)
scraper = EventScraper()

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=scraper.scrape_events, trigger="interval", hours=1)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def get_events():
    try:
        events = scraper.load_events()
        if not events:
            # If no events in file, try scraping
            events = scraper.scrape_events()
        print(f"Returning {len(events)} events")  # Debug log
        return jsonify(events)
    except Exception as e:
        print(f"Error getting events: {str(e)}")  # Debug log
        return jsonify([{
            "title": "Test Event",
            "date": "2025-05-22",
            "location": "Sydney",
            "description": "Test event for debugging",
            "url": "https://example.com"
        }])

@app.route('/capture-email', methods=['POST'])
def capture_email():
    try:
        email = request.form.get('email')
        event_url = request.form.get('event_url')
        
        # Log the email capture
        print(f"Captured email: {email} for event: {event_url}")
        
        # Clean and validate the URL
        if not event_url or event_url == "#":
            return redirect('https://www.eventbrite.com/d/australia--sydney/all-events/')
            
        # Ensure URL is absolute
        if not event_url.startswith(('http://', 'https://')):
            event_url = f'https://www.eventbrite.com{event_url}'
        
        print(f"Redirecting to: {event_url}")  # Debug log
        return redirect(event_url)
        
    except Exception as e:
        print(f"Error in capture_email: {str(e)}")
        return redirect('https://www.eventbrite.com/d/australia--sydney/all-events/')

if __name__ == '__main__':
    # Initial scrape
    scraper.scrape_events()
    app.run(debug=True)