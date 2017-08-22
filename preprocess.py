# -*- coding: utf-8 -*-

import json
import os
import re
import codecs
import sys

# TODO:
# add token after username?
# filter <uploaded> et.c.?

ANONMYIZE = '--anonymize' in sys.argv

HISTORY_PATH = 'slack_history'

METADATA = json.loads(open(os.path.join(HISTORY_PATH, 'metadata.json')).read())

USERS = METADATA['users']
USER = METADATA['auth_info']['user']
USER_ID = METADATA['auth_info']['user_id']

lines = []

def clean_string(s):
    for x in [u'\u0027', u'\u0060', u'\u00B4', u'\u2018', u'\u2019', u'\u201B', u'\x60', u'\xB4']:
        s = s.replace(x,"'")
    for x in [u'\u201C', u'\u201D', u'\u201F']:
        s = s.replace(x,'"')
    s = s.replace(u'\u2026', u' \u2026') # ...
    return s

def preprocess(text):
    text = ' ' + text + ' '
    text = re.sub(r'\s`{3,}[^`]+`{3,}\s', '', text) # remove preformatted
    text = re.sub(r'\s`[^`]+`\s', '', text) # remove code
    text = clean_string(text)
    text = re.sub(r'<http[^>]+', '<URL', text) # hide urls
    text = re.sub(r'http[^\s]+', 'URL', text) # hide urls
    text = re.sub(r'\s\*([^\*]+)\*\s', lambda x: ' ' + x.group(1) + ' ', text) # bold
    text = re.sub(r'\s_([^_]+)_\s', lambda x: ' ' + x.group(1) + ' ', text) # underline
    text = re.sub(r'\s~([^~]+)~\s', lambda x: ' ' + x.group(1) + ' ', text) # strike
    text = re.sub(r'\:([\w\-\+]+)\:', lambda x: '$' + x.group(1) + '$', text) # encode emoticons
    text = re.sub(r'<@([^>]+)>', lambda x: '@' + x.group(1).split('|')[0], text) # @usernames
    text = re.sub(r'<#([^>]+)>', lambda x: '#' + x.group(1).split('|')[0], text) # #channels
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data
    """
    # string = re.sub(r"[^가-힣A-Za-z0-9(),!?\'\`]", " ", string)
    string = text
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r":\s", " : ", string)
    string = re.sub(r"\"", " \" ", string)
    string = re.sub(r",", " , ", string)
    # string = re.sub(r"\.\s", " . ", string)
    string = re.sub(r'(\.+)\s', lambda x: " " + (" ".join(x.group(1))) + " ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"/", " / ", string)
    string = re.sub(r"\(", " ( ", string)
    string = re.sub(r"\)", " ) ", string)
    string = re.sub(r"\?", " ? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()
#    return text.strip()

if __name__ == "__main__":
    fp = codecs.open("preprocessed.txt", "w", "utf-8")
    for folder in ['direct_messages', 'private_channels', 'channels']:
        for filename in os.listdir(os.path.join(HISTORY_PATH, folder)):
            if filename.endswith(".json") and not filename.startswith('sk-'):
                print os.path.join(HISTORY_PATH, folder, filename)
                data = json.loads(open(os.path.join(HISTORY_PATH, folder, filename)).read())
                for message in data['messages']:
                    if 'user' not in message: # skip empty archives
                        continue

                    if ANONMYIZE and message['user'] != USER_ID:
                        print >> fp, "[SOMEONE]"
                    else:
                        print >> fp, "[%s]" % message['user']
    #                print >> fp, "[%s]" % USERS.get(message['user'], 'SOMEONE').upper()
                    print >> fp, preprocess(message['text']) #.encode("latin-1","ignore")
                    print >> fp
            else:
                continue
        print >> fp, "\n***\n" # Mark "end of conversations" to give the network a chance to understand it
