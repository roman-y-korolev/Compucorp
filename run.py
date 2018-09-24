import asyncio
import logging
import os
import sys

import config
import utils

logger = logging.getLogger()

formatter = logging.Formatter('%(asctime)s %(levelname)s [%(module)s]: %(message)s')
logging_out = logging.StreamHandler(sys.stdout)
logging_out.setFormatter(formatter)
logging_out.setLevel(logging.DEBUG)
logger.addHandler(logging_out)
logger.setLevel(logging.DEBUG)

events_path = config.LOADED_PATH + config.EVENTS_PATH
participants_path = config.LOADED_PATH + config.PARTICIPANTS_PATH


async def main():
    '''
    read csv with events and participants data
    than create events and participants in the main system with API
    '''
    events = dict()
    for path in os.listdir(events_path):  # get all files with Events
        path = events_path + path
        events.update(utils.get_events_from_csv(path))

    await utils.create_events_in_the_system(events)

    contacts = await utils.get_contacts_from_api()

    for path in os.listdir(participants_path):  # get all files with Participants
        path = participants_path + path
        partcipants = utils.get_participants_from_csv(path=path, contacts=contacts, events=events)

    await utils.create_participants_in_the_system(partcipants)

    # move files to processed dir
    if not config.DEBUG:
        for path in os.listdir(events_path):
            os.rename(events_path + path, config.PROCESSED_PATH + config.EVENTS_PATH + path)

        for path in os.listdir(participants_path):
            os.rename(participants_path + path, config.PROCESSED_PATH + config.PARTICIPANTS_PATH + path)


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(main())
ioloop.close()
