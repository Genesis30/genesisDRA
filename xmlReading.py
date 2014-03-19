#!/usr/bin/python
import os, sys
import xml.etree.ElementTree as et
from createDB import *

# -------------- Functions --------------
#############################
#	Function "validateFile"
#		Checks if there is a provided file, and asks for it otherwise. 
#		"model_file" stores the path value.
#############################
def validateFile():
	# If no file is provided, ask for it
	if len(sys.argv) == 1:
		model_file = str(raw_input("Enter the name of the xml file descriptor: "))
	# If a file is provided, check if it is valid
	elif len(sys.argv) == 2:
		filePath = sys.argv[1]
		if os.path.exists(filePath):
			model_file = filePath
		# Else, ask for a new path
		else:
			model_file = str(raw_input("The file does not exist. Enter a valid path: "))
	return model_file

#############################
#	Function "updateDatabase"
#		Given the data to populate the database, it proceeds to do so.
#
#	@param: data, the information to build/update the database
#############################
def updateDatabase(data):
	return


#############################
#	Function "readFile"
#		Given a valid file, proceeds to read it and to organize it in order to provide
#		info to build the database.
#
#	@param: model_file
#############################
def readFile(model_file):
	tree = et.parse(model_file)
	root = tree.getroot()

	dbName = root.attrib.get('name')
	createDB(dbName)
	# Building up the system structure
	for part in root:
		# Crea HW y SW
		createPartTable(dbName,part.tag)
		for element in part:
			# Crea tabla de cada elemento
			print '********'
			print 'USANDO ELEMENTOS'
			createElementTable(dbName,element.tag)
			for instance in element:
				ident = instance.attrib.get('name')	
				data = 'algo'
				addToTable(dbName,element.tag,ident,data)

# -------------- Program --------------

model_file = validateFile()
readFile(model_file)


"""
{'hardware': 
	{'voip-server': 
		{'h3': 
			{'h31': [['firmware', None], ['specifications', None], ['specific-software', None], ['rating', None], ['comments', None]]}
		}, 

createDB(name=system)

for part in root:

	createTable( name = part) # Part = hw, sw

	for element in part:
		
		createTable(name = element) # Element = web-server ; voip-server ; 

		for instance in element:

			for charac in instance:
				addToTable(tableName=part , id = instance, data = charac.tag, charac.text)





	for part in root:
		for element in part:
			for charac in element:
				system[part.tag][element.tag].append(charac.text)

	print system
	#updateDatabase(data)
	return system

"""
# print et.tostring(root, encoding="us-ascii", method="xml")