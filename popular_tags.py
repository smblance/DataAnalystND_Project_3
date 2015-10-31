from collections import defaultdict
import pprint, json, operator, re
pp = pprint.PrettyPrinter()

def read_json(file):
	'''Read json'''
	with open(file,'rb+') as f:
		data = json.load(f)
	return data

def freq_of_tags(data):
	'''Make a dict: {tag : number of entries containing it} '''
	tags = defaultdict(lambda: 0)
	for elem in data:
	    for key in elem:
	        tags.update({key : tags[key]+1})
	return tags


data = read_json('data.json')
tags = freq_of_tags(data)
with open('Tag_frequencies.json','wb') as f:
	json.dump(sorted(tags.items(), key=operator.itemgetter(1), reverse = True), f, indent = 4)
