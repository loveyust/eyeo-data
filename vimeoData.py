import vimeo
from datetime import datetime
import json
from glob import glob
import os.path
import ast
import re
import operator
from operator import attrgetter
from operator import itemgetter
import csv

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
data_out['people'] = []

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
            # print name
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
                # print names
            else:
                names.append(name)

            # check if person exists
            for n in names:
                limited_list = [element for element in data_out['people'] if element['name'] == n]
                if (len(limited_list) > 0):
                    limited_list[0]['num'] += 1

                #if any(obj['name'] == n for obj in data_out['people']):
                #    obj['num'] += 1
                else:
                    new_person = {}
                    new_person['name'] = n
                    new_person['num'] = 1
                    data_out['people'].append(new_person)

            # for n in names:
            #     if n not in data_out['people']:
            #         data_out['people'][n] = {}
            #         data_out['people'][n]['num'] = 1
            #     else:
            #         data_out['people'][n]['num'] += 1

        name_full = name.split(' ',1)
        first_name = name_full[0].lower()
        last_name = ''
        if (len(name_full) > 1):
            last_name = name_full[1].lower()

        talk = {}
        talk['description'] = vid[u'description']
        talk['name'] = name
        data_out['talks'].append(talk)

        dt = datetime.strptime(vid[u'release_time'], '%Y-%m-%dT%H:%M:%S+00:00')
        y = dt.strftime('%Y')

        #if y not in data_out['tags']:
        #    data_out['tags'][y] = {}

        # if (vid[u'tags'][0][u'name'] == u'eyeo2017'):
            # print vid[u'tags'][0][u'name']

        for tag in vid[u'tags']:

            # lowercase
            current_tag = tag[u'name'].lower();

            # remove unwanted characters
            for char in ' -_#@':
                current_tag = current_tag.replace(char,'')

            # coorect some misspellings
            if (current_tag == 'datavisaulization'):
               current_tag = 'datavisualization'
            elif (current_tag == 'datviz'):
               current_tag = 'dataviz'
            elif (current_tag == 'processing2.0'):
               current_tag = 'processing'
            elif (current_tag == 'datastorie'):
               current_tag = 'datastories'
            elif (current_tag == 'fatlabs'):
               current_tag = 'fatlab'
            elif (current_tag == 'interactiveenvironmnet'):
               current_tag = 'interactiveenvironment'
            elif (current_tag == 'interactiveinstallations'):
               current_tag = 'interactiveinstallation'
            elif (current_tag == 'of'):
               current_tag = 'openframeworks'
            elif (current_tag == '9/11memorial'):
               current_tag = '911memorial'

            # datavisualization, datavisaulization, dataviz, datviz
            # fatlab, fatlabs
            # interactiveenvironmnet
            # infographics, infoviz

            # Remove unwanted tags - interactiveInstallation
            match = False
            ignore_strings = {'Ignite', 'ignite', 'eyeo', 'yeo', 'inst-int', 'INST_INT', 'Eyeo', 'instint', first_name, last_name}
            for istr in ignore_strings:
                if istr in current_tag:
                    match = True

            if match is False:
                # if current_tag not in data_out['tags'][y]:
                #     data_out['tags'][y][current_tag] = {}
                #     data_out['tags'][y][current_tag]['num'] = 1
                # else:
                #     data_out['tags'][y][current_tag]['num'] += 1
                if current_tag not in data_out['tags']:
                    data_out['tags'][current_tag] = {}
                    data_out['tags'][current_tag][y] = {}
                    data_out['tags'][current_tag][y]['num'] = 1
                else:
                    if y not in data_out['tags'][current_tag]:
                        data_out['tags'][current_tag][y] = {}
                        data_out['tags'][current_tag][y]['num'] = 1
                    else:
                        data_out['tags'][current_tag][y]['num'] += 1

data_out['people'].sort(key=itemgetter("num"), reverse=True)

with open('data.json', 'w') as outfile:
    json.dump(data_out, outfile)

# Write to a D3 ready csv
data_csv = [['key','value','date']];

for t in data_out['tags']:
    
    b_ignore = False
    if (len(data_out['tags'][t]) == 1):
        for y in data_out['tags'][t]:
            # print t + ' ' + str(data_out['tags'][t][y]['num'])
            if (data_out['tags'][t][y]['num'] == 1):
                b_ignore = True
    if b_ignore == False:
        new_data_csv_wrapper = []
        for x in range(0, 8):
            new_data_csv = []
            new_data_csv.append(t)
            new_data_csv.append(0)
            s = str(2011 + x) + '0101'
            date = datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8]))
            s = date.strftime("%m/%d/%y")
            new_data_csv.append(s)
            new_data_csv_wrapper.append(new_data_csv)
            #print "We're on time %d" % (x)

        for y in data_out['tags'][t]:

            s = str(y) + '0101'
            date = datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8]))
            s = date.strftime("%m/%d/%y")

            for d in range (0, 8):
                if (s == new_data_csv_wrapper[d][2]):
                    # found matching date, change the score
                    new_data_csv_wrapper[d][1] = data_out['tags'][t][y]['num'] # / 100.0

            # new_data_csv.append(data_out['tags'][t][y]['num'] / 100.0)
            # s = str(y) + '0101'
            # date = datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8]))
            # s = date.strftime("%m/%d/%y")
            # new_data_csv.append(s)

        for i in range(len(new_data_csv_wrapper)):
            data_csv.append(new_data_csv_wrapper[i])

csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONE)
myFile = open('data_tags.csv', 'w')
with myFile:
   writer = csv.writer(myFile, dialect='myDialect')
   writer.writerows(data_csv)




