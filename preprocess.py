import json
import os
import re
import codecs

HISTORY_PATH = 'slack_history'

METADATA = json.loads(open(os.path.join(HISTORY_PATH, 'metadata.json')).read())

USERS = METADATA['users']
USER = METADATA['auth_info']['user']
USER_ID = METADATA['auth_info']['user_id']

lines = []

fp = codecs.open("preprocessed.txt", "w", "utf-8")

def preprocess(text):
    text = re.sub(r'<http[^>]+', '<URL', text)
    text = re.sub(r'http[^\s]+', 'URL', text)
#    text = re.sub(r':([^:]+):', lambda x: '<:' + x.group(1) + ':>', text)
#    text = re.sub(r'<@([^>]+)>', lambda x: '@' + x.group(1).split('|')[0], text)
#    text = re.sub(r'<#([^>]+)>', lambda x: '#' + x.group(1).split('|')[0], text)
    return text

for folder in ['direct_messages', 'private_channels', 'channels']:
    for filename in os.listdir(os.path.join(HISTORY_PATH, folder)):
        if filename.endswith(".json") and not filename.startswith('sk-'):
            print os.path.join(HISTORY_PATH, folder, filename)
            data = json.loads(open(os.path.join(HISTORY_PATH, folder, filename)).read())
            for message in data['messages']:
                if 'user' not in message: # skip empty archives
                    continue

                print >> fp, "[%s]" % message['user']
#                print >> fp, "[%s]" % USERS.get(message['user'], 'SOMEONE').upper()
                print >> fp, preprocess(message['text']) #.encode("latin-1","ignore")
                print >> fp
        else:
            continue
    print >> fp, "\n***\n" # Mark "end of conversations" to give the network a chance to understand it
