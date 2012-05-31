import datetime
from os.path import basename
import re
import sqlite3
import sys

if (len(sys.argv) > 1):
	fileWithPath = sys.argv[1];
else:
	print "ERROR: Filename required"
	sys.exit(1)

fileName = basename(fileWithPath)
m        = re.match(r'phone_log_(\d+?)-(\d+?)-(\d+?)\.log', fileName)
logYear  = int(m.group(1))
logMonth = int(m.group(2))
logDay   = int(m.group(3))

conn = sqlite3.connect('sqdatabase')
c    = conn.cursor()

f    = open(fileWithPath)

for line in f:
	# Empty line?
	if (line == '\n'):
		continue
	m = re.match(r'Station', line)
	# Footer?
	if (m is not None):
		continue
	m = re.match(r'TYP', line)
	# Other footer?
	if (m is not None):
		continue

	m = re.match(r'([\w\s/]+?)([\d\*]+?)\s+?(\d{5})\s+?[RING\s\.]*?([\d\-]+?)\s+?(\d*?)\s+?(\d\d):(\d\d)\s+?S=(\d+?)\s', line)
	print "Line: " + line
	type = m.group(1)
	if (re.match(r'\s', type) is not None):
		type = 'RG'
	
	if (m.group(2) == '*****'):
		ext = 0
	else:
		ext = int(m.group(2))

	trunk = int(m.group(3))

	# Strip hyphens from phone number
	phone_number = int(m.group(4).replace('-', ''))

	if (m.group(5) is not ''):
		incoming_ext = int(m.group(5))
	else:
		incoming_ext = 0

	start_time_hh = int(m.group(6))
	start_time_mm = int(m.group(7))
	duration = int(m.group(8))

	start_time = datetime.datetime.combine(
		datetime.date(logYear, logMonth, logDay),
		datetime.time(hour=start_time_hh, minute=start_time_mm))

	# Print record to console for debugging
	print "Type: "             + type
	print "Ext: "              + str(ext)
	print "Trunk: "            + str(trunk)
	print "Number and stuff: " + str(phone_number)
	#print "Incoming ext: "    + str(incoming_ext)
	print "Start time: "       + str(start_time)
	print "Duration: "         + str(duration)

	c.execute(
		"INSERT INTO logviewer_phonerecord
		 VALUES (NULL,'%s',%d,%d,%d,%d,%d,'%s','%s')"
		% (type, ext, trunk, 0, phone_number, incoming_ext, start_time,
			datetime.timedelta(seconds=duration)))

f.close()

conn.commit()
conn.close()

