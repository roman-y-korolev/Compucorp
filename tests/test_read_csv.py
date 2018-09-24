import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest
import logging
import datetime
import config
import utils

logger = logging.getLogger(__name__)

EVENT_PATH = 'tests/' + config.LOADED_PATH + config.EVENTS_PATH + 'Events.csv'
PARTICIPANT_PATH = 'tests/' + config.LOADED_PATH + config.PARTICIPANTS_PATH + 'Participants.csv'


def test_read_events():
    events = utils.get_events_from_csv(path=EVENT_PATH)
    assert events['A new event 1'].event_name == 'A new event 1'
    assert events['A new event 1'].event_start == datetime.datetime(2023, 1, 18, 20, 0, 0)
    assert len(events) == 5


@pytest.mark.asyncio
async def test_read_participants():
    events = utils.get_events_from_csv(path=EVENT_PATH)
    contacts = await utils.get_contacts_from_api()
    participants = utils.get_participants_from_csv(path=PARTICIPANT_PATH, events=events, contacts=contacts)
    assert participants[0].event.event_name == 'A new event 1'
    assert participants[0].contact.contact_name == 'Damaris Wilson'
    assert participants[0].contact.contact_id == '3'
    assert len(participants) == 18
