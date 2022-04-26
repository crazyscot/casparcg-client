#!/usr/bin/env python3
#
# This file is a tool for use with Mediary's Caspar Client.
# Copyright (C) 2018 Mediary Limited. All rights reserved.
#

''' Quick script to turn a list of items into a rundown for Caspar's own client '''

# The names of the fields we wish to provide to the template
fields=('name','title')

# READ CAREFULLY!
# The first member of each group is the LABEL to display in the rundown. It may be the empty string '' if you're feeling lazy.
# Other members of the group are the field data, IN THE SAME ORDER they appear above.
# If you don't provide enough members, the extra fields will not be sent to the template. This may have surprising effects, so you're best off providing data for all the fields.
items=[
        ('Fred', 'Fred Smith', 'Wombat Wrangler'),
        ('Alex', 'Alex Jones', 'Head Wombat Wrangler'),
        ('Jane', 'Jane Doe', 'Wombat Lover'),
]

TEMPLATE='mediary/LOWERTHIRD'
LAYER=20
DEVICE='Local CasparCG'

############################################################################

HEAD='''<?xml version="1.0" encoding="UTF-8"?>
<items>
<allowremotetriggering>false</allowremotetriggering>'''

ITEMHEAD='''
<item>
<type>TEMPLATE</type><devicename>%DEVICE%</devicename>
<label>%label%</label><name>%TEMPLATE%</name>
<channel>1</channel><videolayer>%LAYER%</videolayer><delay>0</delay><duration>0</duration>
<allowgpi>false</allowgpi><allowremotetriggering>false</allowremotetriggering><remotetriggerid></remotetriggerid>
<storyid></storyid><flashlayer>1</flashlayer><invoke></invoke><usestoreddata>false</usestoreddata>
<useuppercasedata>false</useuppercasedata><triggeronnext>false</triggeronnext><sendasjson>true</sendasjson>
<templatedata>
'''.replace('\n','')

FIELD='''<componentdata><id>%id%</id><value>%value%</value></componentdata>'''

ITEMTAIL = '''
</templatedata>
<color>Transparent</color>
</item>
'''.replace('\n','')

TAIL='''</items>'''

print(HEAD)
for i in items:
    it = ITEMHEAD
    it = it.replace('%DEVICE%', DEVICE)
    it = it.replace('%TEMPLATE%', TEMPLATE)
    it = it.replace('%LAYER%', str(LAYER))
    title = i[0] or 'Template'
    it = it.replace('%label%', i[0])
    print(it)

    for k,v in zip(fields,i[1:]):
        it = FIELD
        it = it.replace('%id%', k)
        it = it.replace('%value%', str(v))
        print(it)
    print(ITEMTAIL)
print(TAIL)
