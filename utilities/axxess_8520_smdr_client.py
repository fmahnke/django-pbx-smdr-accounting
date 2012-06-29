import datetime
import re
import sqlite3
import string

import simple_socket

def insert_line_to_db(line, cursor):

    # Cleanup incoming line
    line = string.lstrip(line, '\0')

    if (line == '\n'):
        return
    m = re.match(r'Station', line)

    # Footer?
    if (m is not None):
        return
    m = re.match(r'TYP', line)

    # Other footer?
    if (m is not None):
        return

    print "Line: " + line
    m = re.match(r'([\w/]*?)\s+?([\d\*]+?)\s+?(\d{5})\s+?[RING\s\.]*?([\d\-]+?)\s+?(\d*?)\s+?(\d\d):(\d\d)\s+?S=(\d+?)\s', line)
    print "Line: " + line
    if (m is None):
        return
    # Type field returned an empty string?
    if (not m.group(1)):
        type = 'RG'
    else:
        type = m.group(1)

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
        datetime.date.today(),
        datetime.time(hour=start_time_hh, minute=start_time_mm))

    # Print record to console for debugging
    print "Type: "             + type
    print "Ext: "              + str(ext)
    print "Trunk: "            + str(trunk)
    print "Number and stuff: " + str(phone_number)
    #print "Incoming ext: "    + str(incoming_ext)
    print "Start time: "       + str(start_time)
    print "Duration: "         + str(duration)

    cursor.execute("INSERT INTO logviewer_phonerecord VALUES (NULL,'%s',%d,%d,%d,%d,'%s','%s')" % (type, ext, trunk, phone_number, incoming_ext, start_time, datetime.timedelta(seconds=duration)))

    return True

DATABASE_NAME = 'sqdatabase2.db'
RECORD_LENGTH = 86
AXXESS_IP = "192.168.128.220"
AXXESS_PORT = 4000

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

s = simple_socket.SimpleSocket()
s.connect(AXXESS_IP, AXXESS_PORT)

# Introduce ourselves
s.send("02000000".decode("hex"))
s.send("8400".decode("hex"))

while (1):
    line = s.receive(RECORD_LENGTH)
    print "Sock recv: " + line
    status = insert_line_to_db(line, cursor)
    if (status is True):
        conn.commit()

#s.close()
conn.close()


