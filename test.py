#!/usr/bin/python

import os, sys

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

	"""
	print '************************'
	print mk[0][1] 
	print mk[1][1]
	print mk[2][1]
	print mk[3][1]
	print mk[4][1]
	print '************************'

	print '************************'
	print mk[0][0] 
	print mk[1][0]
	print mk[2][0]
	print mk[3][0]
	print mk[4][0]
	print '************************'
	"""
	
	ponderation = mk[0][1] + mk[1][1] + mk[2][1] + mk[3][1] + mk[4][1]
	asd = mk[0][0] + mk[1][0] + mk[2][0] + mk[3][0] + mk[4][0]
	
	result = ponderation/(asd+ponderation)
	
	return result


def calculateMk(mu, PIDS0):
	mk = [[0]*2 for i in range(5)]
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



"""
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