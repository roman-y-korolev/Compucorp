import asyncio
import os

import config
import utils

events_path = config.LOADED_PATH + config.EVENTS_PATH
participants_path = config.LOADED_PATH + config.PARTICIPANTS_PATH


async def main():
    '''
    read csv with events and participants data
    than create events and participants in the main system with API
    '''
    events = dict()
    futures = []
    for path in os.listdir(events_path):  # get all files with Events
        path = events_path + path
        futures.append(utils.get_events_from_csv(path))
    done, _ = await asyncio.wait(futures)  # wait. We need all events for next steps
    for future in done:
        events.update(future.result())

    done, _ = await asyncio.wait([utils.get_contacts_from_api()])  # wait. we need all contacts for participants
    for future in done:
        contacts = future.result()

    futures = []
    for path in os.listdir(participants_path):  # get all files with Participants
        path = participants_path + path
        futures.append(utils.get_participants_from_csv(path=path, contacts=contacts, events=events))
    done, _ = await asyncio.wait(futures)

    for path in os.listdir(events_path):
        os.rename(events_path + path, config.PROCESSED_PATH + config.EVENTS_PATH + path)

    for path in os.listdir(participants_path):
        os.rename(participants_path + path, config.PROCESSED_PATH + config.PARTICIPANTS_PATH + path)


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(main())
ioloop.close()
