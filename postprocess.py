# -*- coding: utf-8 -*-

import re
import codecs
import json
import os

HISTORY_PATH = 'slack_history'
RNN_PATH = 'word-rnn-tensorflow'

METADATA = json.loads(open(os.path.join(HISTORY_PATH, 'metadata.json')).read())

USERS = METADATA['users']
USER = METADATA['auth_info']['user']
USER_ID = METADATA['auth_info']['user_id']

print USERS

fp = codecs.open(os.path.join(RNN_PATH, "sample.txt"), "r", "latin-1")
text = fp.read()

fp = codecs.open("formatted.txt", "w", "utf-8")

text = re.sub(r'\[([^\]]+)\]', lambda x: "\n\n[" + USERS.get(x.group(1).upper(), x.group(1)).upper() + "]\n", text)

print >> fp, text
