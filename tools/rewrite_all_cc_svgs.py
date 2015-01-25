import os,sys
import json
from pprint import pprint

ifile = open("../data/e-symbolic/scalable/intl/flag.svg")

cc_repl = 'COUNTRY_CODE'
cc_json = open('country.json')
cc_data = json.load(cc_json)
for cc_new in cc_data:
	ofile = "../data/e-symbolic/scalable/intl/flag-"+cc_new.lower()+".svg"
	print (ofile)
	ofile = open(ofile, 'w')
	ifile.seek(0)
	for line in ifile:
		line = line.replace(cc_repl, cc_new)
		ofile.write(line)

ifile.close()
ofile.close()
