import math
import os
import sys

def test(distStr):
	
	#Input file
	inputFileName = file_select_v1()
	with open(inputFileName,'r') as inputFile:
		data = inputFile.read()
	dataList = data.split(', ')
	
	#Output file name
	outputFileName = inputFileName.replace('.txt',' Circle Points ' + str(distStr) + 'km.txt')
	
	#Mean Earth radius
	earthRadius_km = 6371
	earthRadius_m = earthRadius_km * 1000
	
	#Distance is entered in km, convert to meters.
	dist = int(distStr * 1000)
	
	#Convert coordinates to numbers.
	latDeg = float(dataList[0])
	lngDeg = float(dataList[1])
	
	#Convert coordinates from degrees to radians.
	latRad = math.radians(latDeg)
	lngRad = math.radians(lngDeg)
	
	#Create a list of angles at which to create points (how many points will the circle consist of).
	numPoints = range(0,360,int(360/36))
	angles = []
	for x in numPoints:
		angles.append(float(x))
	angles.append(float(0))
	
	#With the output file open, write the list of circle coordinates.
	with open(outputFileName, 'w') as outputFile:
	
		for x in angles:
		
			bearing = math.radians(x)
		
			newLat = math.asin(math.sin(latRad) * math.cos(dist/earthRadius_m) + math.cos(latRad) * math.sin(dist/earthRadius_m) * math.cos(bearing))
			
			newLng = lngRad + math.atan2(math.sin(bearing) * math.sin(dist/earthRadius_m) * math.cos(latRad), math.cos(dist/earthRadius_m) - math.sin(latRad) * math.sin(newLat))
			
			newLatDeg = math.degrees(newLat)
			newLngDeg = math.degrees(newLng)
			
			#print('{0}, {1}'.format(str(newLatDeg), str(newLngDeg)))
			
			outputFile.write('{0}, {1}\n'.format(str(newLatDeg), str(newLngDeg)))
		
		

def file_select_v1():

	'''Used to intelligently select a single input file.
	'''

	#Allow the user to enter keywords for searching for files.
	keyWord = input('What key word should be used to search for files?\n')
	
	#Keywords to look for in file name.
	excludeWord = 'REDUCED'

	print('\nListed below are the files that match your search criteria...\n')
	
	#Get a list of all the files in the directory and show the user the files which they are likely to want to use.
	files = os.listdir()
	smartFiles = []
	for x in files:
		if(keyWord in x and excludeWord not in x):
			smartFiles.append(x)
	
	if len(smartFiles) == 0:
		input('No files match your search criteria, please exit...')
	
	for idx, file in enumerate(smartFiles):
		print('> ' + str(idx) + ' --- ' + file)
	
	#Prompt the user the enter the number associated with the file they want to use.
	fileNumber = input('\nPlease enter the number of the file you wish to use.\n')
	
	inputFileName = smartFiles[int(fileNumber)]
	
	return(inputFileName)