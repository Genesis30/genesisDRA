#!/usr/bin/python

import MySQLdb as mdb

# http://127.0.0.1/phpmyadmin/
# User: gedra
# Pass: gedra
con = mdb.connect('localhost', 'root', 'root')
cursor = con.cursor()

class systemDatabase():
	
	#############################
	#	Function "validateFile"
	#		Checks if there is a provided file, and asks for it otherwise. 
	#		"model_file" stores the path value.
	#############################
	def createDB(self, dbName):
		sqlCheckDB = 'SHOW DATABASES LIKE "'+dbName+'";'
		cursor.execute(sqlCheckDB)
		row = str(cursor.fetchone())

		if row == 'None':
			sqlCreateDB = 'CREATE DATABASE ' + dbName + ';'
			cursor.execute(sqlCreateDB)
			print 'Database "%s" successfully created.' % dbName
		else:
			print 'Database "%s" already exists. Keep going.' % dbName
		
	#############################
	#	Function "validateFile"
	#		Checks if there is a provided file, and asks for it otherwise. 
	#		"model_file" stores the path value.
	#############################
	def createPartTable(self, dbName, tableName):
		sqlUseDB = 'USE ' + dbName + ';' 
		cursor.execute(sqlUseDB)

		sqlCheckTable = 'SELECT * FROM information_schema.tables WHERE table_name = "' + tableName + '";'
		cursor.execute(sqlCheckTable)
		row = str(cursor.fetchone())
		
		if row == 'None': 
			sqlCreateTable = 'CREATE TABLE ' + tableName + '(name varchar(30) PRIMARY KEY);'
			cursor.execute(sqlCreateTable)
			print 'Table "%s" successfully created.' % tableName
		else:
			print 'Table "%s" already exists.' % tableName

	#############################
	#	Function "validateFile"
	#		Checks if there is a provided file, and asks for it otherwise. 
	#		"model_file" stores the path value.
	#############################
	def createElementTable(self, dbName, tableName, part_name):
		sqlUseDB = 'USE ' + dbName + ';' 
		cursor.execute(sqlUseDB)

		sqlCheckTable = 'SELECT * FROM information_schema.tables WHERE table_name = "'+tableName+'"'
		cursor.execute(sqlCheckTable)
		row = str(cursor.fetchone())

		if row == 'None':
			if part_name == 'hardware':
				sqlCreateTable = 'CREATE TABLE ' + tableName + '(id varchar(10) PRIMARY KEY, firmware varchar(20), specifications varchar(20), specific_software varchar(20),rating varchar(20),comments varchar(20));'
			else:
				sqlCreateTable = 'CREATE TABLE ' + tableName + '(id varchar(10) PRIMARY KEY, name varchar(20), version varchar(20), auto_update varchar(20));'
			
			cursor.execute(sqlCreateTable)
			print 'Table "%s" successfully created.' % tableName
		else:
			print 'Table "%s" already exists.' % tableName

	#############################
	#	Function "validateFile"
	#		Checks if there is a provided file, and asks for it otherwise. 
	#		"model_file" stores the path value.
	#############################
	def addToTable(self, dbName, tableName, data, ident, part_name):

		sqlCheckData = 'SELECT * FROM ' + tableName + ' WHERE id="' + ident + '";'
		cursor.execute(sqlCheckData)
		row = str(cursor.fetchone())
		
		if row == 'None':
			if part_name == 'hardware':
				sqlInsertIntoTable = 'INSERT INTO ' + tableName + ' VALUES ('+data+');'
			else:
				sqlInsertIntoTable = 'INSERT INTO ' + tableName + ' VALUES ('+data+');'
			
			cursor.execute(sqlInsertIntoTable)

			print 'Successfully inserted data. Query: %s' % sqlInsertIntoTable
		else:
			print 'That instance already exists. Please, use the add option (gedra -a).'

	#############################
	#	Function "updateDatabase"
	#		Given the data to populate the database, it proceeds to do so. Prompts the user 
	#		for information.
	#############################
	def updateDatabase(self):
		dbName = str(raw_input("Enter the name of the system: "))
		partName = str(raw_input("Is it hardware or software?: "))
		tableName = str(raw_input("Enter the name of the element type: "))

		tmp = str(raw_input("Enter the data to add ['FieldName1: new_value , FieldName2: new_value']: "))
			
		campos = validateData(tmp)

		sqlInsertIntoTable = ' INSERT INTO ' + tableName + ' ('+campos[0]+') VALUES ('+campos[1]+');'
		sqlUseDB = 'USE ' + dbName + ';'

		cursor.execute(sqlUseDB)
		cursor.execute(sqlInsertIntoTable)

	#############################
	#	Function "getFromTable"
	#		Search the table for the desired "info" given a "query"
	#############################
	def getFromTable(self, dbName, tableName, info, query):
		sqlUseDB = 'USE %s ;' % dbName
		cursor.execute(sqlUseDB)

		sqlSearchData = 'SELECT %s FROM %s WHERE %s' % (info, tableName, query)

		cursor.execute(sqlUseDB)
		cursor.execute(sqlSearchData)

	#############################
	#	Function "closeDatabase"
	#		Commits & closes the database
	#############################
	def closeDatabase(self):
		con.commit()
		con.close()

	#############################
	#	Function "validateData"
	#		Given the data, returns it with the correct formatting
	#
	#		@param tmp : the string to format
	#		@return validated: the string formatted
	#############################
	def validateData(tmp):
		# String magic
		campos = tmp.split(',')
		columnas = ''
		valores = ''
		for i in range(len(campos)):
			h = campos[i].split(':')
			columnas += ',' + h[0]
			valores += ',"' + h[1].lstrip() +'"'

		col = columnas.lstrip(',')	
		val = valores.lstrip(',')
		validated = [col,val]
		return validated