import json
import logging
from datetime import datetime

import aiohttp

import config

logger = logging.getLogger(__name__)


class Event():
    def __init__(self, event_name, event_type, start_date, start_time):
        self.event_name = event_name
        self.event_type = event_type
        self.event_start = datetime.strptime(start_date + start_time.upper(), '%d/%m/%Y%H.%M%p')
        self.event_id = None

    async def create_with_api(self):
        '''
        Creating event in the CiviCRM system with API
        async method uses aiohttp
        :return: None
        :rtype: None
        '''
        logger.info('Start create event "{}"'.format(self.event_name))
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
        async with aiohttp.ClientSession() as session:
            async with session.post(config.API_URL, params=params) as resp:
                r_json = await resp.json()
                self.event_id = r_json['id']
        logger.info('Finish create event "{}"'.format(self.event_name))


class Participant():
    def __init__(self, event, contact, participant_status):
        self.event = event
        self.contact = contact
        self.participant_status = participant_status

    async def create_with_api(self):
        '''
        Creating participant in the CiviCRM system with API
        async method uses aiohttp
        :return: None
        :rtype: None
        '''
        logger.info('Start create participant "{contact} {event}"'.format(
            contact=self.contact.contact_name,
            event=self.event.event_name))
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
        async with aiohttp.ClientSession() as session:
            async with session.post(config.API_URL, params=params) as resp:
                await resp.json()
        logger.info('Finish create participant "{contact} {event}"'.format(
            contact=self.contact.contact_name,
            event=self.event.event_name))


class Contact():
    def __init__(self, contact_name, contact_id):
        self.contact_name = contact_name
        self.contact_id = contact_id
