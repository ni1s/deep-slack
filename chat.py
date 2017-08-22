# -*- coding: utf-8 -*-

import json
import os
import re
import codecs
import sys
import subprocess

if len(sys.argv) > 1:
    message = sys.argv[1]
else:
    print "Don't forget to pass a message to chat.py as the second argument."
    raise SystemExit

HISTORY_PATH = 'slack_history'

METADATA = json.loads(open(os.path.join(HISTORY_PATH, 'metadata.json')).read())

USERS = METADATA['users']
USER = METADATA['auth_info']['user']
USER_ID = METADATA['auth_info']['user_id']

os.chdir('word-rnn-tensorflow')

# TODO: preprocess message
prime = '"[SOMEONE] ' + message + " [%s] " % USER_ID + ' "'
output = subprocess.check_output(['python', 'sample.py', '-n', '2000', '--prime', prime, '--save_dir', 'save/deep_slack'])

print ">>>>>>>>>>>>>>>"
match = re.search(r"(\[%s\]\s[^\[]+)+" % USER_ID, output)
print "\n".join(list(match.groups()))
print "<<<<<<<<<<<<<<<"
print "output", output.replace("[", "\n[").replace("]", "]\n")
