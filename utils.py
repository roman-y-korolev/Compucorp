import csv

import requests

import config
from models import Event, Participant, Contact


def get_events_from_csv(path):
    events = dict()
    with open(path) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row_num, row in enumerate(csv_reader):
            if (row_num) > 0:
                event = Event(
                    event_name=row[0],
                    event_type=row[1],
                    start_date=row[2],
                    start_time=row[3]
                )
                events[row[0]] = event
                event.create_with_api()
        return events


def get_contacts_from_api():
    r = requests.get(config.CONTACTS_URL)
    result = r.json()['values']
    contacts = dict()
    for contact in result:
        contacts[contact['display_name']] = Contact(
            contact_name=contact['display_name'],
            contact_id=contact['contact_id'])

    return contacts


def get_participants_from_csv(path, events, contacts):
    participants = []
    with open(path) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row_num, row in enumerate(csv_reader):
            if (row_num) > 0:
                participant = Participant(
                        event=events[row[0]] if row[0] in events else None,
                        contact=contacts[row[1]] if row[1] in contacts else None,
                        participant_status=row[2]
                    )
                participants.append(participant)
                participant.create_with_api()
        return participants
