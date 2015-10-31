import xml.etree.ElementTree as ET
tree = ET.parse('Moscow - SW.osm')
root = tree.getroot()

import json
data = []
#Parse XML into python dictionary
for elem in root:
	entry = {}
	bad_tags = set()
	entry.update({'type' : elem.tag})
	for attrib in elem.attrib:
		entry.update({attrib : elem.get(attrib)})
	for tag in elem:
		if tag.tag == 'tag':
			entry.update({tag.get('k') : tag.get('v')})
		elif tag.tag == 'nd':
			if 'ref' in entry:
				entry['ref'].append(tag.get('ref'))
			else:
				entry.update({'ref' : [tag.get('ref')]})
		elif tag.tag == 'member':
			if 'members' not in entry:
				entry.update({'members' : {}})
			for attrib in tag.attrib:
				entry['members'].update({attrib : tag.get(attrib)})
		else:
			bad_tags.add(tag.tag)
	data.append(entry)

if bad_tags != set([]):
	print 'Invalid tags: ', bad_tags

with open('data.json','wb') as f:
	json.dump(data,f)