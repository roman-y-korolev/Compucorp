import json
from datetime import datetime

import requests

import config


class Event():
    def __init__(self, event_name, event_type, start_date, start_time):
        self.event_name = event_name
        self.event_type = event_type
        self.event_start = datetime.strptime(start_date + start_time.upper(), '%d/%m/%Y%H.%M%p')
        self.event_id = None

    def create_with_api(self):
        json_params = json.dumps({
            "title": self.event_name,
            "event_type_id": self.event_type,
            "start_date": self.event_start.strftime("%Y-%m-%d %H:%M:%S")
        })

        params = {
            "key": config.KEY,
            "api_key": config.API_KEY,
            "json": json_params,
            "entity": "Event",
            "action": "create"
        }
        r = requests.post(url=config.API_URL, params=params)
        self.event_id = r.json()['id']


class Contact():
    def __init__(self, contact_name, contact_id):
        self.contact_name = contact_name
        self.contact_id = contact_id


class Participant():
    def __init__(self, event, contact, participant_status):
        self.event = event
        self.contact = contact
        self.participant_status = participant_status

    def create_with_api(self):
        json_params = json.dumps({
            "event_id": self.event.event_id,
            "contact_id": self.contact.contact_id,
            "status_id": self.participant_status
        })

        params = {
            "key": config.KEY,
            "api_key": config.API_KEY,
            "json": json_params,
            "entity": "Participant",
            "action": "create"
        }
        requests.post(url=config.API_URL, params=params)
