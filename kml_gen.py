



def displayKML(kmlContents):

	kmlContentsList = kmlContents.split('\n')

	for line in kmlContentsList:
		print(line)



def main():

	import os
	import sys

	print('*******************************************************************************')


	keyword = input('Please enter a keyword to help identify input files:\n')

	files = os.listdir()

	matchFiles = []

	for file in files:
		if keyword in file:
			matchFiles.append(file)

	print('\nThe following files match the keyword you entered:\n')
	for index, file in enumerate(matchFiles):
		line = '> {0}, {1}'.format(index, file)
		print(line)

	fileChoice = input('\nPlease select a file by entering the number listed next to your filename:\n')
	print('')

	inputFileName = matchFiles[int(fileChoice)]

	outputFileName = inputFileName.replace('.txt','.kml')




	#=================================================================
	#	Open input file and read contents

	inputFile = open(inputFileName,'r')

	inputData = inputFile.read()

	inputFile.close()
	#=================================================================


	inputDataList = inputData.split('\n')


	

	#Create a string to hold all the contents of the KML document. The entire string can then be written to file.
	kmlContents = ''

	#=================================================================
	#	Write the header tags.
	kmlContents += ('\t' * 0) + '<?xml version="1.0" encoding="UTF-8"?>'
	kmlContents += '\n'
	kmlContents += ('\t' * 0) + '<kml xmlns="http://www.opengis.net/kml/2.2">'
	kmlContents += '\n'
	kmlContents += ('\t' * 1) + '<Document>'
	kmlContents += '\n'



	for line in inputDataList:

		lineItems = line.split(',')

		name = ''
		description = ''


		lat = lineItems[0]
		lng = lineItems[1]
		alt = '0'


		kmlContents += ('\t' * 2) + '<Placemark>'
		kmlContents += '\n'
		kmlContents += ('\t' * 3) + '<name>' + name + '</name>'
		kmlContents += '\n'
		kmlContents += ('\t' * 3) + '<description>' + description + '</description>'
		kmlContents += '\n'
		kmlContents += ('\t' * 3) + '<Point>'
		kmlContents += '\n'
		kmlContents += ('\t' * 4) + '<coordinates>' + lng + ',' + lat + ',' + alt + '</coordinates>'
		kmlContents += '\n'
		kmlContents += ('\t' * 3) + '</Point>'
		kmlContents += '\n'
		kmlContents += ('\t' * 2) + '</Placemark>'
		kmlContents += '\n'


	#=================================================================
	#	Write the footer tags.
	kmlContents += ('\t' * 1) + '</Document>'
	kmlContents += '\n'
	kmlContents += ('\t' * 0) + '</kml>'

	
	#=================================================================
	#	Open output file ready to be written.

	outputFile = open(outputFileName, 'w')
	outputFile.write(kmlContents)
	outputFile.close()
	#=================================================================


	#displayKML(kmlContents)

	



	








