#!/usr/bin/python

import sys
import subprocess
import codecs
import os
import re
import xml.etree.ElementTree as xml

script_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_directory)

file_name = 'dspace-xmlui/src/main/webapp/i18n/messages_cs.xml'

root_directory = '../../..'
os.chdir(root_directory)

grep_command = 'grep -R "[>\'\\"]xmlui\\." --include=*.java --include=*.xsl --include=*.xmap --include=*.xslt'

output = subprocess.check_output(grep_command, shell=True)
output_lines = output.strip().split('\n')

message_prefixes = set()
for line in output_lines:
    match = re.search("^([^:]+):.*[>'\"](xmlui\.[^<'\"]+)(?:[<'\"]|$)", line, re.U)
    if (match):
        message_prefixes.add((match.group(2), match.group(1)))

message_prefixes = sorted(message_prefixes, key=lambda x: -len(x[0]))

root = xml.parse(file_name)
for message in root.findall('message'):
    key = message.get('key')
    result_type = 'NO'
    result_file = ''
    for (prefix, file_name) in message_prefixes:
        if (key == prefix):
            result_type = 'YES'
            result_file = file_name
            break
        elif (key.startswith(prefix)):
            result_type = prefix
            result_file = file_name
            break
    print '|'.join([key, result_type, result_file])
    ## hmm, what about messages not starting with "xmlui", like "input-forms", etc ...