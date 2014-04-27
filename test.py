#!/usr/bin/python

import os, sys

def updateElement(element_name, affected_element_id, risk):

	dbName = 'prueba1'
	sqlUpdateTable = ' UPDATE ' + element_name + ' SET risk="'+str(risk)+'" WHERE id="'+affected_element_id+'";'
	sqlUseDB = 'USE ' + dbName + ';'

	print sqlUpdateTable



updateElement('web_server', 'h1', 0.8)













"""
import ds
gedraPath = '/home/genesis/Desktop/GeDRA/model.xml'

def getElements():
	with open(gedraPath, 'r') as model:
		temp = model.readlines()
		i = 0
		elements = []
		
		for line in temp:
			if '<instance' in line:
				data_name = temp[i-1]
				data_id = temp[i]
				data_rating = temp[i+4]

				# Element Name
				temp_name = data_name.split(None)
				temp2_name = temp_name[0]
				element_name = temp2_name.lstrip('<')

				# Element ID
				temp_id = data_id.split('name=')
				temp2_id = temp_id[1]
				element_id = temp2_id.strip('">\n')

				# Element Rating
				temp_rating = data_rating.split('>')
				temp2_rating = temp_rating[1]
				element_rating = temp2_rating.rstrip('</rating')

				# Update elements
				info = element_name + ':' + element_id + ':' + element_rating
				elements.append(info)

			elif '<software>' in line:
				return elements
			i+=1


system_risk_dict = {}


def init():
	elements = getElements()
	for element in elements:
		info = element.split(':')

		element_name = info[0]
		element_id = info[1]
		element_rating = info[2]

		temp = element_name + '-' + element_id
		params = [0,0,0,0,0,0,0,0]
		data = ds.calculateParams(params ,element_name , element_rating, 0)
		# system_risk_dict['element_name - element_id'] = element_risk
		system_risk_dict[temp] = ds.calculateRisk(data)
	print system_risk_dict

init()

"""

"""
import MySQLdb as mdb


def formatLine(line, incidentTime):
	# Data structure to retrieve info
	params = ['' for i in range(8)]
	# Remove unnecessary info & get only relevant info
	splitWhite = line.split(None,2)
	isIds = splitWhite[0]
	if not 'snort' in isIds:
		params[7] = 'notRelevant'
		return params
	else:
		temp1 = splitWhite[2]

		# Split the desired info
		temp2 = temp1.split('[')

		# Attack step?
		step = temp2[0].strip()

		# Classification
		temp21 = temp2[1].rstrip()
		temp22 = temp21.rstrip(']')
		temp23 = temp22.split(None,1)
		classification = temp23[1]
		# Priority
		temp3 = temp2[2]
		temp4 = temp3.split(']')
		priority = temp4[0].strip()

		# Protocol & ip directions
		temp5 = temp4[1].lstrip(':')
		temp6 = temp5.lstrip()
		temp7 = temp6.split()
		temp7.pop(2)

		protocol = temp7[0]
		sourceIp = temp7[1]
		destinationIp = temp7[2]

		# Data structure to be returned
		params[0],params[1],params[2],params[3],params[4],params[5],params[6], params[7] = incidentTime, step, classification, priority, protocol, sourceIp, destinationIp, isIds
		print params
		return params

def decideElement(attack_name):
	attack_dict = {"Attempted Administrator Privilege Gain": '',
						"Attempted User Privilege Gain": '',
						"SCORE! Get the lotion!": '',
						"Potential Corporate Privacy Violation": '',
						"Executable code was detected": '',
						"Successful Administrator Priviledge Gain": '',
						"Successful User Priviledge Gain": '',
						"A Network Trojan was Detected": 5,
						"Unsuccessful User Privilege Gain": '',
						"Web Application Attack": '',
						"Attempted Denial of Service": '',
						"Attempted Information Leak": '',
						"Potentially Bad Traffic": '',
						"Attempt to login by a default username and password": '',
						"Detection of a Denial of Service Attack": '',
						"Misc Attack": '',
						"Detection of a non-standard protocol or event": '',
						"Decode of an RPC query": '',
						"Denial of Service": '',
						"Large Scale Information Leak": '',
						"Information Leak": '',
						"A suspicious filename was detected": '',
						"An attempted login using a suspicious user-name was detected": '',
						"A system call was detected": '',
						"A client was using an unusual port": '',
						"Access to a potentially vulnerable web application": '',
						"Generic ICMP event": '',
						"Misc activity": '',
						"Detection of a Network Scan": '',
						"Not Suspicious Traffic": '',
						"Generic Protocol Command Decode": '',
						"A suspicious string was detected": '',
						"Unknown Traffic= -": '',
						"A TCP connection was detected= -": '',
	}
	attack_name = 'A Network Trojan was Detected'
	return attack_dict[attack_name]



line = '<38>snort: [1:100852:1] UPD FLOOD. [Classification: A Network Trojan was detected] [Priority: 2]: {UDP} 172.16.20.128:15874 -> 10.0.0.100:111'
data = formatLine(line,5)
asd = decideElement(data[2])
print asd


con = mdb.connect('localhost', 'root', 'root')
cursor = con.cursor()

def getFromTable(dbName, tableName, info, query):
		sqlUseDB = 'USE %s ;' % dbName
		cursor.execute(sqlUseDB)

		sqlSearchData = 'SELECT %s FROM %s WHERE %s' % (info, tableName, query)

		cursor.execute(sqlUseDB)
		cursor.execute(sqlSearchData)
		row = str(cursor.fetchone())
		temp =  row.strip("'(,)'")
		return temp

asd = getFromTable('prueba1','web_server','rating','id="h11"')
print asd

alert_num_dict = { 'web_server': 0,
						'database_server': 0,
						'voip_server': 0,
						'router': 0,
						'switch': 0,
						'computer': 0,
						'firewall': 0,
						'printer': 0,
	}
#############################
#	Function "calculateParams"
#		Given some information about the attack, computes it and
#		decides the factors to compute the risk index.
#############################
def calculateParams(params, affected_element, affected_element_relevance, attack_rating):
	IDS_name = 'snort'
	priority_IDS = params
	
	
	print alert_num_dict

	alert_num_dict[affected_element] = alert_num_dict[affected_element]+1

	print alert_num_dict
	# AK : alert amount of an alert thread (not only attack strength but also attack confidence).
	# Calculate AK
	alert_number = alert_num_dict[affected_element]
	AK = alert_number * 3.0 + affected_element_relevance + attack_rating
	
	# CK0 : updated alert confidence [0,1] ; probability that an abnormal activity is a true attack. 
	# Calculate CK0
	if alert_number >=2:
		CK0 = 0.7
	else:
		CK0 = 0.5
	
	# BK : attack confident situation & severity of the corresponding intrusion.
	# Calculate BK
	BK = alert_number*2 + affected_element_relevance
	
	# RS0 : likelihood of a sucessful intrusion. Updated alert in an alert thread. [0,1]
	# Calculate RS0
	if alert_number <=3:
		RS0 = CK0 + alert_number/10.0
	else:
		RS0 = 1.0

	data = [0.0 for i in range(6)]
	data[0], data[1], data[2], data[3], data[4], data[5] = AK, CK0, BK, RS0, priority_IDS, IDS_name
	print data
	return data
	
	



#calculateParams(3, 'web_server', 5, 4)
#calculateParams(3, 'web_server', 5, 4)

#calculateParams(3, 'web_server', 5, 4)






gedraPath = '/home/genesis/Desktop/GeDRA/model.xml'

def parseSystemFile(affected_element_ip):
	with open(gedraPath, 'r') as model:
		temp = model.readlines()
		i = 0
		for line in temp:
			if affected_element_ip in line:
				data = temp[i-3]
			i+=1
		temp = data.split(None)
		temp2 = temp[0]
		element = temp2.lstrip('<')
		return element

asd = parseSystemFile('192.168.1.1')
print asd






import MySQLdb as mdb
con = mdb.connect('localhost', 'root', 'root')
cursor = con.cursor()

def getFromTable(dbName, tableName, info, query):
		sqlUseDB = 'USE %s ;' % dbName
		cursor.execute(sqlUseDB)

		sqlSearchData = 'SELECT %s FROM %s WHERE %s' % (info, tableName, query)

		cursor.execute(sqlUseDB)
		cursor.execute(sqlSearchData)
		row = str(cursor.fetchone())
		print row
		return row

asd = getFromTable('prueba1','web_server','specifications','id="h11"')
print asd




# attack_name: affected_element
attack = {"Attempted Administrator Privilege Gain": "pc",
	"Attempted User Privilege Gain": "router",
}

def zero():
	print 'Algo'

print attack['Attempted User Privilege Gain']


Attempted Administrator Privilege Gain
Attempted User Privilege Gain



params = ['' for i in range(7)]
params[0], params[1], params[2] = 1,2,3

print params


input_string = '<38>snort: [1:100852:1] UPD FLOOD. [Classification: A Network Trojan was detected] [Priority: 2]: {UDP} 172.16.20.128:15874 -> 10.0.0.100:111'

splitBlank = input_string.split(None,2)

temp1 = splitBlank[2]

temp2 = temp1.split('[')
wat = temp2[0].strip()
temp21 = temp2[1].rstrip()
classification = temp21.rstrip(']')
temp3 = temp2[2]
temp4 = temp3.split(']')
priority = temp4[0].strip()
temp5 = temp4[1].lstrip(':')
temp6 = temp5.lstrip()
temp7 = temp6.split()
temp7.pop(2)
protocol = temp7[0]
direccionIpOrigen = temp7[1]
direccionIpDestino = temp7[2]

print '********'
print wat
print classification
print priority
print protocol
print direccionIpOrigen
print direccionIpDestino
print '********'



print '********'
for i in splitTwoDot:
	print i
print '********'


print '********'
for i in splitCorchete:
	print i
print '********'
"""
"""
def computeRiskState(priority,AK, CK0, BK, RS0, priority_IDS, IDS_name):
#	Risk state = Risk Index [+] Risk Dristribution
		
	riskIndex = computeRiskIndex(AK, CK0, BK, RS0, priority_IDS, IDS_name)
	riskState = computeRiskDistribution(priority,riskIndex)
	print riskState 
	return riskState

def computeRiskDistribution(priority, riskIndex):
#	Risk Distribution = Target Importance
#
#	medium = [0,0.5][0.5,0.8][0.8,1.0]
#	high = [0,0.4][0.4,0.7][0.7,1.0]

	if priority <= 3:
		if riskIndex <= 0.5:
			return 0.3
		elif riskIndex <=0.8:
			return 0.6
		else:
			return 1.0
	else:
		if riskIndex <= 0.4:
			return 0.3
		elif riskIndex <=0.7:
			return 0.6
		else:
			return 1.0

def computeRiskIndex(AK, CK0, BK, RS0, priority_IDS, IDS_name): 
#	Risk Index = Alert Amount [+] Alert Confidence [+] Alter Type Number
#					[+] Alert Severity [+] Alert Relevance Score
#
	if IDS_name == "Snort":
		PIDS0 = 3
	else:
		PIDS0 = 1
	
	mu = calculateMu(AK, CK0, BK, RS0, priority_IDS)
	mk = calculateMk(mu,PIDS0)

		
	prob = mk[0][1] + mk[1][1] + mk[2][1] + mk[3][1] + mk[4][1]
	tmp = mk[0][0] + mk[1][0] + mk[2][0] + mk[3][0] + mk[4][0]
	
	conflict = tmp + prob
	result = prob/conflict
	print result
	return result


def calculateMk(mu, PIDS0):
	mk = [[0]*2 for i in range(5A Network Trojan was Detected)]
	w = [0,0.1,0.2,0.3,0.4]

	for i in range(5):
		for j in range(2):
			if j == 0:
				mk[i][j] = mu[i][j] / ( mu[i][j] + mu[i][j+1] + 1 - w[i] * PIDS0)
			else:
				mk[i][j] = mu[i][j] / ( mu[i][j] + mu[i][j-1] + 1 - w[i] * PIDS0)

	return mk

#############################
#	Function "calculateMu"
#		Given the parameters of the system, it will return the factors of risk/no risk
#
#		AK : alert amount of an alert thread (not only attack strength but also attack confidence).
#
#		CK0 : updated alert confidence [0,1] ; probability that an abnormal activity is a true attack. 
#
#		BK : attack confident situation & severity of the corresponding intrusion.
#
#		RS0 : likelihood of a sucessful intrusion. Updated alert in an alert thread. [0,1]
#
#############################

def calculateMu(AK, CK0, BK, RS0, priority_IDS):
	# alpha1 [5,15]  ; alpha2 [10,20]  ; alpha3 [15,30]
	mu = [[0.0]*2 for i in range(5)]
	
	#----------------
	alpha1 = 5
	alpha2 = 10
	alpha3 = 15
	#----------------
	if AK <= alpha2:
		mu[0][0] = float((alpha2-AK) / alpha2)
	else:
		mu[0][0] = 0.0

	if alpha1 >= AK:
		mu[0][1] = 0.0
	elif alpha3 < AK:
		mu[0][1] = 1.0	
	else:
		mu[0][1] = float((AK - alpha1) / (alpha3 - alpha1))
	

	# CK0 [0,1]
	mu[1][0] = 1.0 - CK0
	mu[1][1] = float(CK0)

	# lambda1 [1,5] ; lambda2 [5,9] ; lambda3 [6,10]

	#--------------
	lambda1 = 1
	lambda2 = 5
	lambda3 = 6
	#--------------
	if BK <= lambda2:
		mu[2][0] = float((lambda2 - BK) / lambda2)
	else:
		mu[2][0] = 0.0

	if lambda1 >= BK:
		mu[2][1] = 0.0
	elif lambda3 < BK:
		mu[2][1] = 1.0
	else: 
		mu[2][1] = float((BK - lambda1) / (lambda3 - lambda1))


	# phi = 3 ; PR0 = 4 - priority_IDS
	PR0 = 4.0 - priority_IDS
	phi = 3.0

	if PR0 <= phi:
		mu[3][0] = float((phi - PR0) / phi)
		mu[3][1] = float(PR0 / phi)
	else:
		mu[3][0] = 0.0
		mu[3][1] = 1.0

	# RS0 relevance score

	mu[4][0] = 1.0 - RS0
	mu[4][1] = float(RS0)

	return mu


#computeRiskIndex(AK, CK0, BK, RS0, priority_IDS, IDS_name)
#computeRiskIndex(12.0, 0.6, 6.0, 0.7, 3, "Snort")

computeRiskState(4,12.0, 0.6, 6.0, 0.7, 3, "Snort")

computeRiskState(4,15.0, 0.6, 10.0, 0.8, 3, "Snort")

computeRiskState(4,16.0, 0.6, 11.0, 0.9, 3, "Snort")




mu = [[0]*2 for i in range(5)]
w  = [0]*5
mk = [[0]*2 for i in range(5)]


mu = [[0.6,0.3],[0.55,0.40],[0.7,0.1],[0.9,0.05],[0.61,0.38]]
w = [0,0.1,0.2,0.3,0.4]
mk = [[0.0]*2 for i in range(5)]
PIDS0 = 2

print '----------------------'
print mu
print '----------------------'
print w
print '----------------------'
print mk
print '----------------------'

for i in range(5):
	for j in range(2):
		if j == 0:
			
			mk[i][j] = mu[i][j] / ( mu[i][j] + mu[i][j+1] + 1 - w[i] * PIDS0)
			print '*********'
			print mk[i][j]
			print '*********'
		else:
			
			mk[i][j] = mu[i][j] / ( mu[i][j] + mu[i][j-1] + 1 - w[i] * PIDS0)

print mk



from PIL import Image

def createImage(systemName):
	imagesPath = str(os.getcwd()) + '/images/'
	print imagesPath

def loadImage():
	imagesList = []
	imagesPath = str(os.getcwd()) + '/images/'
	
	for image in os.listdir(imagesPath):
		temp = imagesPath + image
		imageName = Image.open(temp)
		imagesList.append(imageName)


loadImage()

from PIL import Image
#
#	Por defecto se usa el programa 'xv'. 
#	Si no se tiene instalado se puede usar 
#	"Eye of Gnome" (por defecto presente en Ubuntu).
#	Necesario hacer un alias:
#		"sudo ln -s /usr/bin/eog /usr/bin/xv"
#
im = Image.open("pruebaIm.jpg")
im.show()
print (im.format, im.size, im.mode)


def addToTable(dbName, tableName, data, ident, part_name):

	sqlCheckData = 'SELECT * FROM ' + tableName + ' WHERE id="' + ident + '";'
	cursor.execute(sqlCheckData)
	row = str(cursor.fetchone())
	print '+++++++'
	print row
	if row == 'None':
		if part_name == 'hardware':
			sqlInsertIntoTable = 'INSERT INTO ' + tableName + ' VALUES ('+data+');'
		else:
			print 'Metiendo software'
			sqlInsertIntoTable = 'INSERT INTO ' + tableName + ' VALUES ('+data+');'
			print '*********'
			print sqlInsertIntoTable
			print '*********'
		
		cursor.execute(sqlInsertIntoTable)
		con.commit()

		print 'Successfully inserted data. Query: %s' % sqlInsertIntoTable
	else:
		pass


con = mdb.connect('localhost', 'root', 'mysqlpass')
cursor = con.cursor()


sqlUseDB = 'USE prueba1;'

cursor.execute(sqlUseDB)

addToTable('prueba1','ftp_client','"s81","None","None","None"','s81','software')
"""