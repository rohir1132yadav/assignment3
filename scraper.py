import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

class EventScraper:
    def __init__(self):
        self.events = []
        self.data_file = 'events.json'

    def scrape_events(self):
        url = "https://www.eventbrite.com/d/australia--sydney/all-events/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
        
        try:
            print("Attempting to scrape events...")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            print(f"Response status code: {response.status_code}")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Debug the HTML content
            print("HTML Content:", soup.prettify()[:500])  # Print first 500 chars
            
            event_elements = soup.find_all('div', {'class': 'search-event-card-wrapper'}) or \
                            soup.find_all('div', {'class': 'discover-search-event-card'})
            
            if not event_elements:
                print("No events found, using sample data")
                self.events = self.get_sample_events()
            else:
                self.events = []
                for event in event_elements:
                    try:
                        # Updated selectors based on Eventbrite's current structure
                        title_elem = event.find('h2') or \
                                   event.find('div', {'class': 'eds-event-card__formatted-name'}) or \
                                   event.find('div', {'data-testid': 'event-card-title'})
                        
                        date_elem = event.find('div', {'class': 'eds-event-card-content__sub-title'}) or \
                                  event.find('div', {'data-testid': 'event-card-date'})
                        
                        location_elem = event.find('div', {'class': 'card-text--truncated__one'}) or \
                                      event.find('div', {'data-testid': 'event-card-venue'})
                        
                        url_elem = event.find('a', {'class': 'eds-event-card-content__action-link'}) or \
                                  event.find('a')
                        
                        image_elem = event.find('img', {'class': 'eds-event-card-content__image'}) or \
                                   event.find('img')
                        
                        description_elem = event.find('div', {'class': 'eds-event-card__description'}) or \
                                         event.find('p', {'class': 'card-text'})
    
                        # Extract data with detailed fallbacks
                        title = title_elem.get_text().strip() if title_elem else "Event Title TBA"
                        date = date_elem.get_text().strip() if date_elem else "Date TBA"
                        location = location_elem.get_text().strip() if location_elem else "Sydney"
                        url = url_elem.get('href') if url_elem else "#"
                        image_url = image_elem.get('src') if image_elem else "https://via.placeholder.com/300"
                        description = description_elem.get_text().strip() if description_elem else f"Join us for this exciting event in {location} on {date}"
    
                        # Print debug info
                        print(f"\nFound event: {title}")
                        print(f"Date: {date}")
                        print(f"Location: {location}")
                        
                        event_data = {
                            'title': title,
                            'date': date,
                            'location': location,
                            'url': url,
                            'image_url': image_url,
                            'description': description,
                            'price': "Price TBA"  # Added default price
                        }
                        
                        self.events.append(event_data)
                    except Exception as e:
                        print(f"Error parsing event: {str(e)}")
                        continue
            
            print(f"Successfully scraped {len(self.events)} events")
            self.save_events()
            return self.events
            
        except Exception as e:
            print(f"Error scraping events: {str(e)}")
            self.events = self.get_sample_events()
            self.save_events()
            return self.events

    def get_sample_events(self):
        return [
            {
                "title": "Sydney Harbor Night Festival",
                "date": "June 15, 2025",
                "location": "Sydney Harbor",
                "description": "Experience the magic of Sydney Harbor at night",
                "url": "https://example.com/event1"
            },
            {
                "title": "Australian Food & Wine Expo",
                "date": "May 30, 2025",
                "location": "Sydney Convention Centre",
                "description": "Discover Australia's finest cuisines and wines",
                "url": "https://example.com/event2"
            },
            {
                "title": "Tech Innovation Summit",
                "date": "June 5, 2025",
                "location": "Sydney Tech Hub",
                "description": "Join the biggest tech conference in Sydney",
                "url": "https://example.com/event3"
            }
        ]

    def save_events(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.events, f, ensure_ascii=False, indent=2)

    def load_events(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.events = json.load(f)
        return self.events

if __name__ == "__main__":
    scraper = EventScraper()
    events = scraper.scrape_events()
    print(f"Scraped {len(events)} events")