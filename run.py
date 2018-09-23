import os

import config
import utils

events_path = config.LOADED_PATH + config.EVENTS_PATH
participants_path = config.LOADED_PATH + config.PARTICIPANTS_PATH

events = dict()
for path in os.listdir(events_path):
    path = events_path + path
    events.update(utils.get_events_from_csv(path))

contacts = utils.get_contacts_from_api()

participants = []
for path in os.listdir(participants_path):
    path = participants_path + path
    participants.extend(utils.get_participants_from_csv(path=path, contacts=contacts, events=events))
