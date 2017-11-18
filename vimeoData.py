import vimeo
from datetime import datetime
import json
from glob import glob
import os.path
import ast
import re

# Access the vimeo API
# v = vimeo.VimeoClient(token="15788d8848c4bd4d5bc044ea110e7d52", key="a549d0fcfcf1ac4456c83f4dd5788364a00ddd3c", secret="37sdo9zfjEieq7UB0gKRR41xxfuz3nzW7GmIL770lTJ4L5gUcGpvQGGlYjIWfaqlZvEoEFZPs6KxnLqQgV7RGu2bAalm86iV5esLnz81fxXeJBx0Fxuwr04oNJfp2QaG")
# vInfo = v.get('https://api.vimeo.com/videos/51533137') #, params={"fields": "tags"})
# vInfo = v.get('https://api.vimeo.com/users/eyeofestival/videos?per_page=100&page=4')
# assert vInfo.status_code == 200
# print vInfo.json()[u'data'][0][u'tags'] # ["tags"][0]
# print vInfo.json()

# load json files
data = []
data_in = []

pattern = os.path.join('json', '*.json')
for file_name in glob(pattern):
    print file_name
    with open(file_name) as f:
        json_load = f.read()
        j = ast.literal_eval(json_load)
        data_in.extend(j[u'data'])

# with open('json/allVids01.json') as json_data:
#     j = json_data.read()
#     json_string = ast.literal_eval(j) # json.dumps(json_data)
#     print json_string[u'data'][0]

print len(data_in)

data_out = {}
data_out['talks'] = []
data_out['tags'] = {}
data_out['people'] = {}

# Iterate through video data
for vid in data_in:

    # Ignore Inst Int videos - they will weight the Eyeo videos toward interactive installation
    if 'INSTINT' not in vid[u'name'] and 'titles' not in vid[u'name'] and 'Titles' not in vid[u'name'] and 'TITLES' not in vid[u'name']:

        # for the name - get the string after the "-" in the title, dop off the
        # u'name': u'Eyeo 2017 - Taeyoon Choi ||',

        name = vid[u'name']
        name = name.replace(u'\u2013', '-');

        if '2011' in name: # 2011 videos have the name at the front
            name = name.split(' - ',1)[0]
        elif ' - ' in name:
            print name
            name = name.split(' - ',1)[1]

        # remove nums
        if any(char.isdigit() for char in name):
            name = ''.join([i for i in name if not i.isdigit()])
            name = name[1:]

        # remove suffix
        name = name.replace('.mov', '');
        name = name.replace('.mp4', '');
        name = name.replace(' ||', '');

        # Add to people counter, ignore panels
        if 'panel' not in name and 'Panel' not in name:
            names = []
            # print 'NOT PANEL' + name
            if 'and' in name:
                names = name.split(' and ',1)
            elif '&' in name:
                names = name.split(' & ',1)
                print names
            else:
                names.append(name)
            for n in names:
                if n not in data_out['people']:
                    data_out['people'][n] = {}
                    data_out['people'][n]['num'] = 1
                else:
                    data_out['people'][n]['num'] += 1

        first_name = name.split(' ',1)[0]
        first_name = first_name.lower()

        talk = {}
        talk['description'] = vid[u'description']
        talk['name'] = name
        data_out['talks'].append(talk)

        dt = datetime.strptime(vid[u'release_time'], '%Y-%m-%dT%H:%M:%S+00:00')
        y = dt.strftime('%Y')

        if y not in data_out['tags']:
            data_out['tags'][y] = {}

        # if (vid[u'tags'][0][u'name'] == u'eyeo2017'):
            # print vid[u'tags'][0][u'name']

        for tag in vid[u'tags']:

            # lowercase
            tag[u'name'] = tag[u'name'].lower();

            # remove unwanted characters
            for char in ' -_#@':
                tag[u'name'] = tag[u'name'].replace(char,'')

            # Remove unwanted tags - interactiveInstallation
            match = False
            ignore_strings = {'Ignite', 'ignite', 'eyeo', 'inst-int', 'INST_INT', 'Eyeo', 'instint', first_name}
            for istr in ignore_strings:
                if istr in tag[u'name']:
                    match = True

            if match is False:
                if tag[u'name'] not in data_out['tags'][y]:
                    data_out['tags'][y][tag[u'name']] = {}
                    data_out['tags'][y][tag[u'name']]['num'] = 1
                else:
                    data_out['tags'][y][tag[u'name']]['num'] += 1


print data_out['people']

