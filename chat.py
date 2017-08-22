# -*- coding: utf-8 -*-

import json
import os
import re
import codecs
import sys
import subprocess
import preprocess

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
# + " [%s] " % USER_ID +
prime = '[SOMEONE] ' + preprocess.preprocess(message)
output = subprocess.check_output(['python', 'sample.py', '-n', '2000', '--prime', prime, '--save_dir', 'save/deep_slack']) #, '--pick', '2'])

print ">>>>>>>>>>>>>>>"
match = re.search(r"((\[%s\]\s[^\[]+)+)" % USER_ID, output)
reply = match.groups()[0]
print reply.replace("[", "\n[").replace("]", "]\n") #"\n".join(list(match.groups()))
print "<<<<<<<<<<<<<<<"
print "output", output.replace("[", "\n[").replace("]", "]\n")
