#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import pprint, json, re, sys

reload(sys)
sys.setdefaultencoding('utf-8')
pp = pprint.PrettyPrinter()

def read_json(file):
	"""Read file as json."""
	with open(file,'rb+') as f:
		data = json.load(f)
	return data

def write_json(obj, file):
	"""Write obj to (emptied) file as json."""
	with open(file,'rb+') as f:
		f.seek(0)
		f.truncate()
		json.dump(obj, f, ensure_ascii=False)

def remove_dot_from_tags(data):
	"""Substitute '.' with '(dot)' in keys"""
	for entry in data:
		for key in entry:
			entry[key.replace('.','(dot)')] = entry.pop(key)

def freq_of_values(tag, tags, data):
	"""Make a dict: {value of tag : number of entries that have this value}."""
	freq = defaultdict(lambda: 0)
	if tag not in tags:
		print "Tag not present."
		return None
	for entry in data:
		if tag in entry:
			freq.update({entry[tag] : freq[entry[tag]]+1})
	return dict(freq)

def audit_coords(data):
	"""Audit coordinates: must be 12.345678."""
	coord_re = re.compile('\d{2}.\d*')
	bad_lat, bad_lon = [],[]
	for entry in data:
		if 'lat' in entry:
			if coord_re.match(entry['lat']) == None:
				bad_lat.append(entry['lat'])
			elif coord_re.match(entry['lat']).end() != len(entry['lat']):
				bad_lat.append(entry['lat'])
			elif float(entry['lat']) > 55.7321 or float(entry['lat']) < 55.6599:
				bad_lat.append(entry['lat'])
			else:
				entry['lat'] = float(entry['lat'])
		if 'lon' in entry:
			if coord_re.match(entry['lon']) == None:
				bad_lon.append(entry['lon'])
			elif coord_re.match(entry['lon']).end() != len(entry['lon']):
				bad_lon.append(entry['lon'])
			elif float(entry['lon']) > 37.6455 or float(entry['lon']) < 37.4583:
				bad_lon.append(entry['lon'])
			else:
				entry['lon'] = float(entry['lon'])
	return bad_lat, bad_lon

def audit_postcode(data, tags):
	"""Audit postcodes - check if present in the valid postcode list.

	Bad postcodes need to be checked manually.
	"""
	bad_postcodes = []
	with open('Moscow_postcodes.txt','rb') as f:
		postcodes = []
		for line in f:
			postcodes.append(int(line))
	for postcode in freq_of_values('addr:postcode', tags, data):
		try:
			if int(postcode) not in postcodes:
				bad_postcodes.append(postcode)
		except:
			bad_postcodes.append(postcode)
	return bad_postcodes

def clean_housenumbers(data):
	"""Clean housenumbers of entries using 'parse_hn' function."""
	a = 1
	for entry in data:
		if 'addr:housenumber' in entry:
			attribs = parse_hn(entry['addr:housenumber'])
			if attribs == (None,)*6:
				del entry['addr:housenumber']
			else:
				hn = {}
				if attribs[0] != '':
					hn.update({'number' : attribs[0]})
				if attribs[1] != '':
					hn.update({'number_2' : attribs[1]})
				if attribs[2] != '':
					hn.update({'bld_type' : attribs[2]})
				if attribs[3] != '':
					hn.update({'bld_num' : attribs[3]})
				if attribs[4] != '':
					hn.update({'bld_type_2' : attribs[4]})
				if attribs[5] != '':
					hn.update({'bld_type_2' : attribs[5]})				
				entry['addr:housenumber'] = hn
	return data

def parse_hn(raw_hn):
	"""Audit one housenumber and return arguments."""
	raw_hn = raw_hn.lower()
	try:
		raw_hn = raw_hn.replace(u'.',u'')
	except:
		print raw_hn, type(raw_hn)
	raw_hn = raw_hn.replace(u' ',u'')
	raw_hn = raw_hn.replace(u',','')
	raw_hn = raw_hn.replace(u'строение',u'с')
	raw_hn = raw_hn.replace(u'корпус',u'к')
	raw_hn = raw_hn.replace(u'корп',u'к')

	digits = [0,1,2,3,4,5,6,7,8,9]
	number, number_2, bld_type, bld_num, bld_type_2, bld_num_2 = [u'']*6
	mode = 'number'
	for c in raw_hn:
		if mode == 'number':
			if c.isdigit() or c in [u'а',u'б',u'г',u'д',u'е',u'ж']:
				number += c
			elif number != u'':
				mode = 'parse'
		if mode == 'number_2':
			if c.isdigit():
				number_2 += c
			else:
				mode = 'parse'
		if mode == 'parse':
			if c in [u'с',u'к',u'в']:
				bld_type = c
				mode = 'bld_num'
			if c == u'/':
				mode = 'number_2'
		if mode == 'bld_num':
			if c.isdigit():
				bld_num += c
			elif c in [u'с',u'к',u'в']:
				bld_type_2 = c
				mode = 'bld_num_2'
			else:
				mode = 'parse'
		if mode == 'bld_num_2':
			if c.isdigit():
				bld_num += c
			elif c in [u'с',u'к',u'в']:
				bld_type_2 = c
				mode = 'bld_num_2'
			else:
				mode = 'parse'
	if bld_type != u'' and bld_num == u'':
		bld_type = u''
	if bld_type_2 != u'' and bld_num_2 == u'':
		bld_type_2 = u''
	return number, number_2, bld_type, bld_num, bld_type_2, bld_num_2

def audit_phone(data):
	"""Print phone numbers that do not have the form of '+7 *** *******', where * is a digit."""
	re_phone = re.compile('\+7 \d{3} \d{7}')
	bad_phones = []
	for entry in data:
		if 'contact:phone' in entry:
			match = re_phone.match(entry['contact:phone'])
			if match == None:
				bad_phones.append(entry['contact:phone'])
			elif match.end() != len(entry['contact:phone']):
				bad_phones.append(entry['contact:phone'])
	return bad_phones

def clean_phone(data):
	"""Regularize the phone numbers to the '+7 *** *******', where * is a digit."""
	phone_codes = set()
	for entry in data:
		if 'contact:phone' in entry:
			num = entry['contact:phone']
			for char in [u'(',u')',u' ',u'-']:
				num = num.replace(char, u'')
			if u',' in num:
				num = num.split(u',')
			elif u';' in num:
				num = num.split(u';')
			else:
				num = [num]
			for n in range(len(num)):
				if num[n][0] != u'+':
					if num[n][0] != u'7':
						num[n]= u'+7' + num[n]
					else:
						num[n] = u'+' + num[n]
				num[n] = num[n][:2] + ' ' + num[n][2:5] + ' ' + num[n][5:len(num[n])]
				phone_codes.add(num[n][2:6])
			entry['contact:phone'] = ','.join(num)
	return data, phone_codes

data = read_json('data.json')
tags = [x[0] for x in read_json('Tag_frequencies.json')] #dictionary: {tag : number of ocurrencies}

if __name__ == '__main__':	
	remove_dot_from_tags(data)
	data = clean_housenumbers(data)
	print "Some of the phones not in form of +7 *** *******:\n", audit_phone(data)[:10]
	data, phone_codes = clean_phone(data)
	print "Bad latitude and longitude:\n", audit_coords(data)
	print "Postcodes not in postcodes list:\n", audit_postcode(data, tags)
	write_json(data, 'data_cleaned.json')



