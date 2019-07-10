import sqlite3
from datetime import datetime

UPC_fulfilled = False

# create database connection
conn = sqlite3.connect("drinkdb")
cursor = conn.cursor()

while (1):
	# this means that a UPC was carried in from the
	# last cycle because someone forgot to scan their name
	if (not UPC_fulfilled):
		# get code as input
		UPC = input("Gib UPC plz: ")
	else:
		UPC_fulfilled = False

	# get submitter name_code
	name_code = input("Gib name code: ")

	# get current time with accuracy to nearest second
	date = datetime.now().replace(microsecond=0)

	if (name_code[0:10].startswith("000000000")):
		# we have obtained both a UPC code and a name code
		# so we're gonna enter normally
		print("ENTERING WITH A NAME PROVIDED")
		insertcmd = "INSERT INTO drink(UPC, name_code, date) VALUES (\"" \
			+ UPC + "\", \"" + name_code + "\", \"" + str(date.isoformat())+ "\");"
		UPC_fulfilled = False
	else:
		# this means that someone didn't put their name in
		# so we're gonna enter UPC without a name
		# and then skip the next cycle's UPC entry
		print("ENTERING WITHOUT NAME")
		insertcmd = "INSERT INTO drink(UPC, date) values (\"" \
			+ UPC + "\", \"" + date.isoformat() + "\");"
		UPC = name_code
		name_code = None
		UPC_fulfilled = True

	cursor.execute(insertcmd)
	conn.commit()
	insertcmd = ""