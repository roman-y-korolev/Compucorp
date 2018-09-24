import asyncio
import csv
import json
import logging

import aiohttp

import config
from models import Event, Participant, Contact

logger = logging.getLogger(__name__)


def get_events_from_csv(path):
    '''
    Getting events data from csv file

    :param path: path to csv file
    :type path: str
    :return: dict of events with event names as keys
    :rtype: dict
    '''
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
    '''
    Creating events in the CiviCRM system
    use method create_with_api of Event model

    :param events: dict of events
    :type events: dict
    :return: None
    :rtype: None
    '''
    futures = [e.create_with_api() for e in events.values()]
    await asyncio.wait(futures)


async def get_contacts_from_api():
    '''
    Getting contacts from the CiviCRM system with API

    :return: dict of contscts with contact names as keys
    :rtype: dict
    '''
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
    '''
    Getting participant data from csv file

    :param path: path to csv file
    :type path: str
    :param events: dict of events
    :type events: dict
    :param contacts: dict of contacts
    :type contacts: dict
    :return: list of participants (model Participant)
    :rtype: list
    '''
    participants = []
    with open(path) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row_num, row in enumerate(csv_reader):
            if (row_num) > 0:
                if row[0] in events and row[1] in contacts:
                    participant = Participant(
                        event=events[row[0]],
                        contact=contacts[row[1]],
                        participant_status=row[2] if row[2] in config.VALID_STATUSES else 'Registered'
                    )
                    participants.append(participant)
                else:
                    if row[0] not in events:
                        logger.warning('Participant did not created. Event name "{}" is wrong')
                    if row[1] not in contacts:
                        logger.warning('Participant did not created. Contact name "{}" is wrong')
        return participants


async def create_participants_in_the_system(participants):
    '''
    Creating participants in the CiviCRM system
    :param participants:
    :type participants:
    :return: None
    :rtype:None
    '''
    futures = [p.create_with_api() for p in participants]
    done, _ = await asyncio.wait(futures)
