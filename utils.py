import asyncio
import csv
import json

import aiohttp

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
        return events

async def create_events_in_the_system(events):
    futures = [e.create_with_api_async() for e in events.values()]
    await asyncio.wait(futures)


async def get_contacts_from_api():
    json_params = json.dumps({
        "sequential": 1
    })
    params = {
        "key": config.KEY,
        "api_key": config.API_KEY,
        "json": json_params,
        "entity": "Contact",
        "action": "get"
    }
    contacts = dict()
    async with aiohttp.ClientSession() as session:
        async with session.post(config.API_URL, params=params) as resp:
            r_json = await resp.json()
            result = r_json['values']
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
        return participants

async def create_participants_in_the_system(participants):
    futures = [p.create_with_api_async() for p in participants]
    done, _ = await asyncio.wait(futures)
