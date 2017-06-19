def kml_convert():

	"""I made this script to make use of the WK flight paths Chris Skinner gave me.
	
	The flight paths were in a KML format but the data had some odd fields. This
	script conditions the data so there aren't any strange things, then puts it back
	into a KML file.
	
	"""
	
	#Opens the kml file to read, reads the data and puts it into a Python list.
	fileName = 'fly.kml'
	file = open(fileName)
	data = file.read()
	dataList = data.split('\n')
	
	#Opens a new file to contain the modified data.
	newFileName = 'Fly_Modified.kml'
	newFile = open(newFileName,'w')
	
	#Opens another file to contain simple text data (hopefully can use this to generate a vector line in Global Mapper).
	newFileName1 = 'Simple_Text_version.txt'
	newFile1 = open(newFileName1,'w')
	
	#Defines a new, empty, list.
	dataListMod = []
	
	for x in dataList:
		if '<altitudeMode>' in x:
			q = x[:]
			dataListMod.append(q.replace('clampToGround','absolute'))
		else:
			dataListMod.append(x)
	
	for x in dataListMod:
		
		if '<description>' in x:
			y = x[:]
			y = y.replace('<description><![CDATA[','')
			y = y.replace(']]></description>','')
			y = y.lstrip(' ')
			
		if '<coordinates>' in x:
			#Writes a modified coordinates line to the new file.
			g = x[:]
			altitude = ',' + y + '</coordinates>\n'
			g = g.replace('</coordinates>',altitude)
			newFile.write(g)
			
			#Writes only the coordinates (comma delimited) to a basic text file.
			basicCoords = g[:]
			basicCoords = basicCoords.replace('<coordinates>','')
			basicCoords = basicCoords.replace('</coordinates>','')
			basicCoords = basicCoords.replace(' ','')
			newFile1.write(basicCoords)
			
		else:
			newFile.write(x)
			newFile.write('\n')
		
	file.close()
	newFile.close()
	newFile1.close()

def coord_conv():
	
	"""Convert coordinates in degrees, minutes, seconds to decimal degrees.
	
	Takes in a set of latitude/longitude coordinates in degree minutes seconds
	and converts them to decimal degree coordinates.
	
	The input coordinates are expected to be in the same format as the following
	data:
	
	530300N 0053000W - 530300N 0045319W - 524500N 0045319W - 524500N 0044018W
	
	If there are any new lines in the data it should not interfere with the pattern.
	The latitudes and longitudes should always be separated by a space, and the
	pairs should be separated by ' - ' (space hyphen space).
	
	"""
	import os
	import common
	
	fileName = common.file_select_single()

	#Get a list of all the files in the directory and show the user the files which they are likely to want to use.
	#files = os.listdir()
	#smartFiles = []
	#for x in files:
	#		if 'EG' in x and not 'decimal' in x:
	#		smartFiles.append(x)

	#print(' ')
	#n = 0
	#for x in smartFiles:
	#	print(str(n) + ' - ' + x)
	#	n+=1
	
	#Prompt the user the enter the number associated with the file they want to use.
	#fileNumber = input('\nPlease enter the number of the file you wish to use:\n')
	#fileName = smartFiles[int(fileNumber)]
	
	#Prompt the user the specify what type of shape to create.
	protoMode = input('\nPlease specify the mode to use (0 = lat, long. 1 = long, lat.):\n')
	mode = int(protoMode)
	
	#Opens the text file containing the coordinates in degree, minute, second format.
	file = open(fileName,'r')
	data = file.read()
	file.close()
	
	#Conditions data into a useful list.
	data1 = data.replace('\n', '')
	dataList = data1.split(' - ')
	
	NorthCoords = []
	WestCoords = []
	
	for pair in dataList:
		a = pair.split(' ')
		NorthCoords.append(a[0])
		WestCoords.append(a[1])
	
	#Some optional debug to check if lists of coordinates look okay.
	#for x, y in zip(NorthCoords, WestCoords):
	#	print(x + ' ' + y)
	
	#Opens a new file to contain the coordinates in decimal degrees.
	newFileName = fileName.replace('.txt','_decimal.txt')
	newFile = open(newFileName,'w')
	
	for x, y in zip(NorthCoords,WestCoords):
		
		#Calculates the longitudinal data.
		x1 = x.replace('N','')
		#print(x1)
		northDeg = int(x1[0:2])
		northMin = int(x1[2:4])/60
		northSec = int(x1[4:6])/3600
		northDec = round(northDeg + northMin + northSec,5)
		northStr = str(northDec)
		
		#Calculates the latitudinal data.
		y1 = y.replace('W','')
		#print(y1)
		westDeg = int(y1[0:3])
		westMin = int(y1[3:5])/60
		westSec = int(y1[5:7])/3600
		westDec = round(westDeg + westMin + westSec,5)
		westStr = '-' + str(westDec)
		
		#Mode decides which way around information is written.
		if mode == 0:
			newFile.write(northStr + ', ' + westStr + '\n')
		elif mode == 1:
			newFile.write(westStr + ', ' + northStr + '\n')
		
	newFile.close()
	
def kml_create():

	"""Used to create a KML file from a list of coordinates.
	
	I made this script to help me convert the coordinates for the EG D201 danger areas
	into KML files which could be loaded into various GIS software like Global Mapper
	and SOCET etc.
	
	The script can generate the following KML types:
		- points		IN PROGRESS
		- line			COMPLETE
		- circle		IN PROGRESS
		- 2D polygon	COMPLETE
		- 3D polygon	STATUS UNKNOWN
	
	The script expects decimal degree input data in the same format
	as is output by the 'co-conv' script i.e. "latitude, longitude".
	
	"""
	#-----------------------------------------------------------------------------------------------------------------------------------------------
	#	Output program details to screen.
	
	programTitle = 'KML CREATOR'
	programAuthor = 'C Reed'
	programDateCreated = '26/10/2016'
	programDescription = 'This program generates various KML files using a list of coordinates as an input.'
	
	functionMessageParts = 	[
							'********************************************************************************',
							'\n\t' + programTitle + '\n\n'
							'********************************************************************************',
							'Author: ' + programAuthor + '\n',
							'Date: ' + programDateCreated + '\n',
							'Description: ' + programDescription + '\n',
							'********************************************************************************',
							]

	functionMessage = ''
	for x in functionMessageParts:
		functionMessage += x
	print(functionMessage)
	#-----------------------------------------------------------------------------------------------------------------------------------------------
	#	Import required Python libraries.
	import os
	import sys
	import math
	
	#-----------------------------------------------------------------------------------------------------------------------------------------------
	#	Notice about input file format.
	print('NOTICE: This program can only accept coordinates in the following format:\n')
	print('    {0}, {1} e.g...\n    {2}, {3}\n    {4}, {5}'.format('Latitude', 'Longitude', 52.13916658, -4.558604992, 31.13967891, -8.558468137))
	#input('\nPlease press enter to continue...')
	
	#-----------------------------------------------------------------------------------------------------------------------------------------------
	#	Choose KML type.
	#Define an object to hold valid KML types.
	kmlTypes = ['line','circle','2D','3D','3D2']
	kmlTypesString = ''
	
	for x in range(0,len(kmlTypes)):
	
		if x == (len(kmlTypes) -1):
			kmlTypesString += kmlTypes[x]
		elif x == (len(kmlTypes) -2):
			kmlTypesString += kmlTypes[x] + ' or '
		else:
			kmlTypesString += kmlTypes[x] + ', '
	
	#Prompt the user to specify what type of shape to create.
	shape = input('\nPlease specify the type of shape (' + kmlTypesString + '):\n')
	
	#Check that a valid kml type choice was made, otherwise exit the program.
	if shape in kmlTypes:
		kmlChoice = True
	else:
		raise NameError('Invalid KML type chosen!')
	
	#The circle KMLs only need a single coordinate which is typed into the command prompt, don't need to open a file.
	#Otherwise open a file to read input coordinates.
	if shape != 'circle':
		#-----------------------------------------------------------------------------------------------------------------------------------------------
		#	Find input file.
		#Keywords to look for in file name.
		keyWord = input('\nPlease enter a keyword to help identify input files:\n')

		#Get a list of all the files in the directory and show the user the files which they are likely to want to use.
		files = os.listdir()
		smartFiles = []
		for x in files:
			if keyWord in x :
				smartFiles.append(x)

		print(' ')
		n = 0
		for x in smartFiles:
			print(str(n) + ' - ' + x)
			n+=1
		
		#Prompt the user the enter the number associated with the file they want to use.
		fileNumber = input('\nPlease select a file by entering the number listed next to your filename:\n')
		fileName = smartFiles[int(fileNumber)]
		shapeName = fileName.replace('_decimal.txt','')
	
		file = open(fileName,'r')
		data = file.read()
		
		#Put data into list format.
		rawDataList = data.split('\n')
		dataList = []
		for item in rawDataList:
			if item != '':
				dataList.append(item)
		
		#Create two separate lists, one for Longitude and one for Latitude.
		FirstCoords = []
		SecondCoords = []
		for pair in dataList:
			a = pair.split(', ')
			FirstCoords.append(a[0])
			SecondCoords.append(a[1])
	
	
	
		
	#=====================================================================================
	#	CONFIGURATION AND STYLING
	#=====================================================================================
	#	This sections is used to define the various static options.
	
	#PARAMETERS
	#Single altitude setter. This is now deprecated for circle and needs to be deprecated for other types.
	simpleAltitude = 12500
	
	#Altitude mode selector.
	altitudeMode = 'relativeToGround'
    #Altitude modes:
	# absolute
    # clampToGround
    # clampToSeaFloor
    # relativeToGround
    # relativeToSeaFloor
	
	#STYLE
	LineWidth = 2
	LineColour = 'ff3644DB'
	AreaColour = '6B3644DB'#Not yet implemented.
	
	#=====================================================================================
	#	CONFIGURATION AND STYLING	
	#=====================================================================================
	
	if shape == 'circle':
		#========================================================================================================================================================================
		#Creates an empty KML file from the coordinate information.
		
		#========================================================================================================================================================================
		#Get the centre of the circle from the user.
		centerCircleCoordsStr = input('\nPlease enter the coordinates for the center of the circle in the\nfollowing format:\n\nlatitude, longitude:\n')
		centerCircleCoords = centerCircleCoordsStr.split(', ')
		
		centerCircleLat = float(centerCircleCoords[0])
		centerCircleLng = float(centerCircleCoords[1])
		
		circleRadiusString = input('\n - RADIUS - Please enter the radius of the circle:\nkm = Kilometers\nnm = Nautical Miles\nm = Meters\nM = Miles\n\n> ')
		
		if 'km' in circleRadiusString:
			a = circleRadiusString.replace('km','')
			circleRadiusKm = int(a)
		elif 'nm' in circleRadiusString:
			a = circleRadiusString.replace('nm','')
			circleRadiusKm = int(a) * 1.852
		elif 'M' in circleRadiusString:
			a = circleRadiusString.replace('M','')
			circleRadiusKm = int(a) * 1.60934
		elif 'm' in circleRadiusString:
			a = circleRadiusString.replace('m','')
			circleRadiusKm = int(a) / 1000
		
		circleRadiusM = circleRadiusKm * 1000
		
		#========================================================================================================================================================================
		#Get altitude value.
		circleAltitudeString = input('\n - ALTITUDE - Please enter an altitude for the KML:\nkm = Kilometers\nm = Meters\nM = Miles\nft = Feet\nnm = Nautical Miles\n\n> ')
		
		if 'km' in circleAltitudeString:
			a = circleAltitudeString.replace('km','')
			circleAltitudeKm = int(a)
			
		elif 'nm' in circleAltitudeString:
			a = circleAltitudeString.replace('nm','')
			circleAltitudeKm = int(a) * 1.852
			
		elif 'ft' in circleAltitudeString:
			a = circleAltitudeString.replace('ft','')
			circleAltitudeKm = int(a) / (3.28084*1000)
			
		elif 'M' in circleAltitudeString:
			a = circleAltitudeString.replace('M','')
			circleAltitudeKm = int(a) * 1.60934
			
		elif 'm' in circleAltitudeString:
			a = circleAltitudeString.replace('m','')
			circleAltitudeKm = int(a) / 1000
			
		#Altitude must be entered in meters.
		circleAltitudeM = circleAltitudeKm * 1000
		
		#========================================================================================================================================================================
		#Get name for KML and output file.
		outputFileNameStart = input('\nPlease enter a name for the shape file:\n')
		outputFileName = outputFileNameStart + '_circle.kml'
		shapeName = outputFileNameStart
		kmlName = outputFileName
		
		#========================================================================================================================================================================
		#Specify if the circle should have a place mark in the centre.
		placemark = input('\nAdd placemark to centre of circle? [y/n]:\n')
		
		#========================================================================================================================================================================
		#Choose whether the circle should be a ring or a disk.
		circleStyle = input('\nSpecify if the circle should be shaded (disk) or empty (ring) [disk/ring]:\n')
		
		#========================================================================================================================================================================
		#Mean Earth radius
		earthRadius_km = 6371
		earthRadius_m = earthRadius_km * 1000
		
		#Distance is entered in km, convert to meters.
		dist = circleRadiusM
		
		#Convert coordinates to numbers.
		latDeg = centerCircleLat
		lngDeg = centerCircleLng
		
		#Convert coordinates from degrees to radians.
		latRad = math.radians(latDeg)
		lngRad = math.radians(lngDeg)
		
		#Create a list of angles at which to create points (how many points will the circle consist of).
		numPoints = range(0,360,int(360/36))
		angles = []
		for x in numPoints:
			angles.append(float(x))
		angles.append(float(0))
		
		#circleCoordinates = ''
		circleCoordinatesList = []
		
		#Loop through bearings and create a coordinate pair at each angle.
		for x in angles:
		
			bearing = math.radians(x)
		
			newLat = math.asin(math.sin(latRad) * math.cos(dist/earthRadius_m) + math.cos(latRad) * math.sin(dist/earthRadius_m) * math.cos(bearing))
			
			newLng = lngRad + math.atan2(math.sin(bearing) * math.sin(dist/earthRadius_m) * math.cos(latRad), math.cos(dist/earthRadius_m) - math.sin(latRad) * math.sin(newLat))
			
			newLatDeg = math.degrees(newLat)
			newLngDeg = math.degrees(newLng)
			
			#print('{0}, {1}'.format(str(newLatDeg), str(newLngDeg)))
			
			#outputFile.write('{0}, {1}\n'.format(str(newLatDeg), str(newLngDeg)))
			
			#circleCoordinates += '{0}, {1}\n'.format(str(newLatDeg), str(newLngDeg))
			
			circleCoordinatesList.append([str(newLatDeg), str(newLngDeg)])
		
		
		#========================================================================================================================================================================	
		#Output to describe what is being made.
		print('\n=================================================================')
		print('Creating a circle KML.')
		print("The KML shape's name will be >> "+ kmlName)
		print('KML circle radius: ' + str(circleRadiusKm) + ' km.')
		print('KML circle altitude: ' + str(circleAltitudeKm) + ' km.')
		print('Generating...')
			
		kmlFile = open(kmlName,'w')
	
		#Defines all the heading information of the KML file.
		kmlFileStart1 = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
		kmlFileStart2 = '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n'
		lowerFaceStart1 = '\t<Document>\n'
		lowerFaceStart2 = '\t\t<name>Layer 1</name>\n'
		
		#If the user has specified to put a placemark in the middle of the circle.
		if placemark == 'y':
			lowerFaceStart3 = '\t\t<Placemark>\n'
			lowerFaceStart4 = '\t\t\t<name>' + shapeName + '</name>\n'
			lowerFaceStart5 = '\t\t\t<description>Insert description here.</description>\n'
			lowerFaceStart6 = '\t\t\t<Point>\n'
			lowerFaceStart7 = '\t\t\t\t<coordinates>' + str(centerCircleLng) + ',' + str(centerCircleLat) + ',' + str(circleAltitudeM) + '</coordinates>\n'
			lowerFaceStart8 = '\t\t\t</Point>\n'
			lowerFaceStart9 = '\t\t</Placemark>\n'
		else:
			lowerFaceStart3 = ''
			lowerFaceStart4 = ''
			lowerFaceStart5 = ''
			lowerFaceStart6 = ''
			lowerFaceStart7 = ''
			lowerFaceStart8 = ''
			lowerFaceStart9 = ''
		
		lowerFaceStart10 = '\t\t<Placemark>\n'
		lowerFaceStart11 = '\t\t\t<name>' + shapeName + ' ' + str(circleRadiusKm) + 'km ring' + '</name>\n'
		lowerFaceStart12 = '\t\t\t<description>Insert description here.</description>\n'
		lowerFaceStart13 = '\t\t\t<Style>\n'
		lowerFaceStart14 = '\t\t\t\t<LineStyle>\n'
		lowerFaceStart15 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
		lowerFaceStart16 = '\t\t\t\t\t<width>' + str(LineWidth) + '</width>\n'
		lowerFaceStart17 = '\t\t\t\t</LineStyle>\n'
		lowerFaceStart18 = '\t\t\t\t<PolyStyle>\n'
		lowerFaceStart19 = '\t\t\t\t\t<color>6B3644DB</color>\n'
		lowerFaceStart20 = '\t\t\t\t\t<fill>1</fill>\n'
		lowerFaceStart21 = '\t\t\t\t\t<outline>1</outline>\n'
		lowerFaceStart22 = '\t\t\t\t</PolyStyle>\n'
		lowerFaceStart23 = '\t\t\t\t<BalloonStyle>\n'
		lowerFaceStart24 = '\t\t\t\t\t<text>Insert text here.</text>\n'
		lowerFaceStart25 = '\t\t\t\t</BalloonStyle>\n'
		lowerFaceStart26 = '\t\t\t</Style>\n'
		
		#If the circle is just a ring.
		if circleStyle == 'ring':
			lowerFaceStart27 = '\t\t\t<LineString>\n'
			lowerFaceStart28 = '\t\t\t\t<extrude>1</extrude>\n'
			lowerFaceStart29 = '\t\t\t\t<tessellate>1</tessellate>\n'
			lowerFaceStart30 = '\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
			lowerFaceStart31 = '\t\t\t\t<coordinates>\n'
			
			#Writes all the heading information of the KML file.
			kmlFile.write(kmlFileStart1)
			kmlFile.write(kmlFileStart2)
			for x in range(1,32):
				exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
			
			
			
			#Write the coordinates to the file.
			for x in range(0, len(circleCoordinatesList)):
				#Format the output string.
				outputDataFormatted = formatCoordOutput(circleCoordinatesList[x][0],circleCoordinatesList[x][1],circleAltitudeM)
				if x == 0:
					kmlFile.write('\t\t\t\t\t\t\t' + outputDataFormatted)
				else:
					kmlFile.write('\t\t\t\t\t\t\t' + outputDataFormatted)
					
			lowerFaceEnd1 = '\t\t\t\t</coordinates>\n'
			lowerFaceEnd2 = '\t\t\t</LineString>\n'
			lowerFaceEnd3 = '\t\t</Placemark>\n'
			lowerFaceEnd4 = '\t</Document>\n'
			lowerFaceEnd5 = '</kml>\n'
			
			#Writes all the footer information of the KML file.
			for x in range(1,6):
				exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')
			
		#If the circle is shaded in like a disk.
		if circleStyle == 'disk':	
			lowerFaceStart27 = '\t\t\t<Polygon>\n'
			lowerFaceStart28 = '\t\t\t\t<outerBoundaryIs>\n'
			lowerFaceStart29 = '\t\t\t\t\t<LinearRing>\n'
			lowerFaceStart30 = '\t\t\t\t\t\t<tessellate>1</tessellate>\n'
			lowerFaceStart31 = '\t\t\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
			lowerFaceStart32 = '\t\t\t\t\t\t\t<coordinates>\n'
			
			#Writes all the heading information of the KML file.
			kmlFile.write(kmlFileStart1)
			kmlFile.write(kmlFileStart2)
			for x in range(1,33):
				exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
			
			#Write the coordinates to the file.
			for x in range(0, len(circleCoordinatesList)):
				#Format the output string.
				outputDataFormatted = formatCoordOutput(circleCoordinatesList[x][0],circleCoordinatesList[x][1],circleAltitudeM)
				if x == 0:
					kmlFile.write('\t\t\t\t\t\t\t' + outputDataFormatted)
				else:
					kmlFile.write('\t\t\t\t\t\t\t' + outputDataFormatted)
					
			lowerFaceEnd1 = '\t\t\t\t\t\t\t</coordinates>\n'
			lowerFaceEnd2 = '\t\t\t\t\t</LinearRing>\n'
			lowerFaceEnd3 = '\t\t\t\t</outerBoundaryIs>\n'
			lowerFaceEnd4 = '\t\t\t</Polygon>\n'
			lowerFaceEnd5 = '\t\t</Placemark>\n'
			lowerFaceEnd6 = '\t</Document>\n'
			lowerFaceEnd7 = '</kml>\n'
			
			#Writes all the footer information of the KML file.
			for x in range(1,8):
				exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')
		#========================================================================================================================================================================
	
	if shape == 'line':
		#========================================================================================================================================================================
		#Creates an empty KML file from the coordinate information.
		
		fileNameParts = fileName.split('.')
		inputFileExtension = fileNameParts[-1]
		nameModConfirm = input('\nThe input file extension is .' + inputFileExtension + '? [y/n]:\n')
		
		if(nameModConfirm == 'y'):
			kmlName = fileName.replace('.' + inputFileExtension,'_line.kml')
			
		#Output to describe what is being made.
		input('\n=================================================================\nCreating a '
		+ shape + ' KML from:\n\n> ' + smartFiles[int(fileNumber)] + "\n\nThe KML shape's name will be:\n\n> "
		+ kmlName + '\n\nPlease press enter to continue...')
			
		kmlFile = open(kmlName,'w')
	
		#Defines all the heading information of the KML file.
		kmlFileStart1 = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
		kmlFileStart2 = '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n'
		lowerFaceStart1 = '\t<Document>\n'
		lowerFaceStart2 = '\t\t<name>Layer 1</name>\n'
		lowerFaceStart3 = '\t\t<Placemark>\n'
		lowerFaceStart4 = '\t\t\t<name>' + shapeName + '</name>\n'
		lowerFaceStart5 = '\t\t\t<description>Insert description here.</description>\n'
		lowerFaceStart6 = '\t\t\t<Style>\n'
		lowerFaceStart7 = '\t\t\t\t<LineStyle>\n'
		lowerFaceStart8 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
		lowerFaceStart9 = '\t\t\t\t\t<width>' + str(LineWidth) + '</width>\n'
		lowerFaceStart10 = '\t\t\t\t</LineStyle>\n'
		lowerFaceStart11 = '\t\t\t\t<PolyStyle>\n'
		lowerFaceStart12 = '\t\t\t\t\t<color>6B3644DB</color>\n'
		lowerFaceStart13 = '\t\t\t\t\t<fill>1</fill>\n'
		lowerFaceStart14 = '\t\t\t\t\t<outline>1</outline>\n'
		lowerFaceStart15 = '\t\t\t\t</PolyStyle>\n'
		lowerFaceStart16 = '\t\t\t\t<BalloonStyle>\n'
		lowerFaceStart17 = '\t\t\t\t\t<text>Insert text here.</text>\n'
		lowerFaceStart18 = '\t\t\t\t</BalloonStyle>\n'
		lowerFaceStart19 = '\t\t\t</Style>\n'
		lowerFaceStart20 = '\t\t\t<LineString>\n'
		lowerFaceStart21 = '\t\t\t\t<extrude>1</extrude>\n'
		lowerFaceStart22 = '\t\t\t\t<tessellate>1</tessellate>\n'
		lowerFaceStart23 = '\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
		lowerFaceStart24 = '\t\t\t\t<coordinates>'
		
		#Writes all the heading information of the KML file.
		kmlFile.write(kmlFileStart1)
		kmlFile.write(kmlFileStart2)
		for x in range(1,25):
			exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
		
		
		spacingCount = 1
		for x, y in zip(FirstCoords, SecondCoords):
			
			northStr = str(x)
			
			westStr = str(y)
				
			#Writes coordinate information to kml file.
			if spacingCount == 1:
				kmlFile.write('\t' + westStr + ', ' + northStr + ', ' + str(simpleAltitude) + '\n')
				spacingCount+=1
				
			else:
				kmlFile.write('\t\t\t\t\t\t\t\t' + westStr + ', ' + northStr + ', ' + str(simpleAltitude) + '\n')
				
		lowerFaceEnd1 = '\t\t\t\t</coordinates>\n'
		lowerFaceEnd2 = '\t\t\t</LineString>\n'
		lowerFaceEnd3 = '\t\t</Placemark>\n'
		lowerFaceEnd4 = '\t</Document>\n'
		lowerFaceEnd5 = '</kml>\n'
		
		for x in range(1,6):
			exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')
		#========================================================================================================================================================================
	
	if shape == '2D':
		#========================================================================================================================================================================
		#Get altitude value.
		circleAltitudeString = input('\nPlease enter an altitude for the KML:\nkm = Kilometers\nm = Meters\nM = Miles\nft = Feet\nnm = Nautical Miles\n\n> ')
		
		if 'km' in circleAltitudeString:
			a = circleAltitudeString.replace('km','')
			circleAltitudeKm = int(a)
			
		elif 'nm' in circleAltitudeString:
			a = circleAltitudeString.replace('nm','')
			circleAltitudeKm = int(a) * 1.852
			
		elif 'ft' in circleAltitudeString:
			a = circleAltitudeString.replace('ft','')
			circleAltitudeKm = int(a) / (3.28084*1000)
			
		elif 'M' in circleAltitudeString:
			a = circleAltitudeString.replace('M','')
			circleAltitudeKm = int(a) * 1.60934
			
		elif 'm' in circleAltitudeString:
			a = circleAltitudeString.replace('m','')
			circleAltitudeKm = int(a) / 1000
			
		#Altitude must be entered in meters.
		circleAltitudeM = circleAltitudeKm * 1000
		
		#Creates an empty KML file from the coordinate information.
		kmlName = fileName.replace('.txt','_2DPolygon.kml')
		kmlFile = open(kmlName,'w')
	
		#Defines all the heading information of the KML file.
		kmlFileStart1 = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
		kmlFileStart2 = '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n'
		lowerFaceStart1 = '\t<Document>\n'
		lowerFaceStart2 = '\t\t<name>Layer 1</name>\n'
		lowerFaceStart3 = '\t\t<Placemark>\n'
		lowerFaceStart4 = '\t\t\t<name>' + shapeName + '</name>\n'
		lowerFaceStart5 = '\t\t\t<description>Insert description here.</description>\n'
		lowerFaceStart6 = '\t\t\t<Style>\n'
		lowerFaceStart7 = '\t\t\t\t<LineStyle>\n'
		lowerFaceStart8 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
		lowerFaceStart9 = '\t\t\t\t\t<width>' + str(LineWidth) + '</width>\n'
		lowerFaceStart10 = '\t\t\t\t</LineStyle>\n'
		lowerFaceStart11 = '\t\t\t\t<PolyStyle>\n'
		lowerFaceStart12 = '\t\t\t\t\t<color>6B3644DB</color>\n'
		lowerFaceStart13 = '\t\t\t\t\t<fill>1</fill>\n'
		lowerFaceStart14 = '\t\t\t\t\t<outline>1</outline>\n'
		lowerFaceStart15 = '\t\t\t\t</PolyStyle>\n'
		lowerFaceStart16 = '\t\t\t\t<BalloonStyle>\n'
		lowerFaceStart17 = '\t\t\t\t\t<text>Insert text here.</text>\n'
		lowerFaceStart18 = '\t\t\t\t</BalloonStyle>\n'
		lowerFaceStart19 = '\t\t\t</Style>\n'
		lowerFaceStart20 = '\t\t\t<Polygon>\n'
		lowerFaceStart21 = '\t\t\t\t<outerBoundaryIs>\n'
		lowerFaceStart22 = '\t\t\t\t\t<LinearRing>\n'
		lowerFaceStart23 = '\t\t\t\t\t\t<tessellate>1</tessellate>\n'
		lowerFaceStart24 = '\t\t\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
		lowerFaceStart25 = '\t\t\t\t\t\t\t<coordinates>'
		
		#Writes all the heading information of the KML file.
		kmlFile.write(kmlFileStart1)
		kmlFile.write(kmlFileStart2)
		for x in range(1,26):
			exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
		
		
		spacingCount = 1
		for x, y in zip(FirstCoords, SecondCoords):
			
			northStr = str(x)
			
			westStr = str(y)
				
			#Writes coordinate information to kml file.
			if spacingCount == 1:
				kmlFile.write('\t' + westStr + ', ' + northStr + ', ' + str(circleAltitudeM) + '\n')
				spacingCount+=1
				
			else:
				kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + westStr + ', ' + northStr + ', ' + str(circleAltitudeM) + '\n')
				
		lowerFaceEnd1 = '\t\t\t\t\t\t\t</coordinates>\n'
		lowerFaceEnd2 = '\t\t\t\t\t</LinearRing>\n'
		lowerFaceEnd3 = '\t\t\t\t</outerBoundaryIs>\n'
		lowerFaceEnd4 = '\t\t\t</Polygon>\n'
		lowerFaceEnd5 = '\t\t</Placemark>\n'
		lowerFaceEnd6 = '\t</Document>\n'
		lowerFaceEnd7 = '</kml>\n'
		
		for x in range(1,8):
			exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')
		#========================================================================================================================================================================
		
	
		
	if shape == '3D':
		#========================================================================================================================================================================
		#3D Configuration.
		#This has been modified so that it formats the coordinates of the horizontal areas in the official KML standard thus allowing GXP Xplorer to display the KML files.
		
		#I have made the script request the altitudes so that the program doesn't have to be modified each time I run it.
		topAltitude = input('Please enter the top altitude (meters): ')
		bottomAltitude = input('Please enter the bottom altitude (meters): ')
		#topAltitude = 23000
		#bottomAltitude = 0
		
		#Creates an empty KML file from the coordinate information.
		kmlName = fileName.replace('.txt','_3DPolygon.kml')
		kmlFile = open(kmlName,'w')
		
		shapeName = fileName.replace('.txt','')
		shapeDesc = ''
	
		#---HORIZONTAL POLYGON 1---
		#Defines all the heading information of the KML file.
		kmlFileStart1 = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
		kmlFileStart2 = '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n'
		lowerFaceStart1 = '\t<Document>\n'
		lowerFaceStart2 = '\t\t<name>Layer 1</name>\n'
		lowerFaceStart3 = '\t\t<Placemark>\n'
		lowerFaceStart4 = '\t\t\t<name>' + shapeName + '</name>\n'
		lowerFaceStart5 = '\t\t\t<description>' + shapeDesc + '</description>\n'
		lowerFaceStart6 = '\t\t\t<Style>\n'
		lowerFaceStart7 = '\t\t\t\t<LineStyle>\n'
		lowerFaceStart8 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
		lowerFaceStart9 = '\t\t\t\t\t<width>6</width>\n'
		lowerFaceStart10 = '\t\t\t\t</LineStyle>\n'
		lowerFaceStart11 = '\t\t\t\t<PolyStyle>\n'
		lowerFaceStart12 = '\t\t\t\t\t<color>6B3644DB</color>\n'
		lowerFaceStart13 = '\t\t\t\t\t<fill>1</fill>\n'
		lowerFaceStart14 = '\t\t\t\t\t<outline>1</outline>\n'
		lowerFaceStart15 = '\t\t\t\t</PolyStyle>\n'
		lowerFaceStart16 = '\t\t\t\t<BalloonStyle>\n'
		lowerFaceStart17 = '\t\t\t\t\t<text></text>\n'
		lowerFaceStart18 = '\t\t\t\t</BalloonStyle>\n'
		lowerFaceStart19 = '\t\t\t</Style>\n'
		lowerFaceStart20 = '\t\t\t<Polygon>\n'
		lowerFaceStart21 = '\t\t\t\t<outerBoundaryIs>\n'
		lowerFaceStart22 = '\t\t\t\t\t<LinearRing>\n'
		lowerFaceStart23 = '\t\t\t\t\t\t<tessellate>1</tessellate>\n'
		lowerFaceStart24 = '\t\t\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
		lowerFaceStart25 = '\t\t\t\t\t\t\t<coordinates>'
		
		#Writes all the heading information of the KML file.
		kmlFile.write(kmlFileStart1)
		kmlFile.write(kmlFileStart2)
		for x in range(1,26):
			exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
		
		
		spacingCount = 1
		for x in dataList:
			
			y = x.replace(' - ','')
			
			#Calculates the longitudinal data.
			northDeg = int(y[0:2])
			northMin = int(y[2:4])/60
			northSec = int(y[4:6])/3600
			northDec = round(northDeg + northMin + northSec,5)
			northStr = str(northDec)
			
			#Calculates the latitudinal data.
			westDeg = int(y[8:11])
			westMin = int(y[11:13])/60
			westSec = int(y[13:15])/3600
			westDec = round(westDeg + westMin + westSec,5)
			westStr = '-' + str(westDec)
				
			#Writes coordinate information to kml file.
			#if spacingCount == 1:
			#	kmlFile.write('\t' + westStr + ', ' + northStr + ', ' + str(bottomAltitude) + '\n')
			#	
			#	spacingCount+=1
			#	
			#else:
			#	kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + westStr + ', ' + northStr + ', ' + str(bottomAltitude) + '\n')
				
			
			#Writes coordinate information to kml file.
			if spacingCount == 1:
				kmlFile.write(westStr + ',' + northStr + ',' + str(bottomAltitude))
				spacingCount+=1
				
			else:
				kmlFile.write(' ' + westStr + ',' + northStr + ',' + str(bottomAltitude))
				
		lowerFaceEnd1 = '</coordinates>\n'
		lowerFaceEnd2 = '\t\t\t\t\t</LinearRing>\n'
		lowerFaceEnd3 = '\t\t\t\t</outerBoundaryIs>\n'
		lowerFaceEnd4 = '\t\t\t</Polygon>\n'
		lowerFaceEnd5 = '\t\t</Placemark>\n'
		lowerFaceEnd6 = '\t</Document>\n'
		lowerFaceEnd7 = '</kml>\n'
		
		for x in range(1,6):
			exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')

		
		#---HORIZONTAL POLYGON 2---
		#This writes the second 2D polygon which is at the higher altitude.
		#Defines all the heading information of the KML file.
		kmlFileStart1 = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
		kmlFileStart2 = '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n'
		lowerFaceStart1 = '\t<Document>\n'
		lowerFaceStart2 = '\t\t<name>Layer 1</name>\n'
		lowerFaceStart3 = '\t\t<Placemark>\n'
		lowerFaceStart4 = '\t\t\t<name></name>\n'
		lowerFaceStart5 = '\t\t\t<description></description>\n'
		lowerFaceStart6 = '\t\t\t<Style>\n'
		lowerFaceStart7 = '\t\t\t\t<LineStyle>\n'
		lowerFaceStart8 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
		lowerFaceStart9 = '\t\t\t\t\t<width>6</width>\n'
		lowerFaceStart10 = '\t\t\t\t</LineStyle>\n'
		lowerFaceStart11 = '\t\t\t\t<PolyStyle>\n'
		lowerFaceStart12 = '\t\t\t\t\t<color>6B3644DB</color>\n'
		lowerFaceStart13 = '\t\t\t\t\t<fill>1</fill>\n'
		lowerFaceStart14 = '\t\t\t\t\t<outline>1</outline>\n'
		lowerFaceStart15 = '\t\t\t\t</PolyStyle>\n'
		lowerFaceStart16 = '\t\t\t\t<BalloonStyle>\n'
		lowerFaceStart17 = '\t\t\t\t\t<text></text>\n'
		lowerFaceStart18 = '\t\t\t\t</BalloonStyle>\n'
		lowerFaceStart19 = '\t\t\t</Style>\n'
		lowerFaceStart20 = '\t\t\t<Polygon>\n'
		lowerFaceStart21 = '\t\t\t\t<outerBoundaryIs>\n'
		lowerFaceStart22 = '\t\t\t\t\t<LinearRing>\n'
		lowerFaceStart23 = '\t\t\t\t\t\t<tessellate>1</tessellate>\n'
		lowerFaceStart24 = '\t\t\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
		lowerFaceStart25 = '\t\t\t\t\t\t\t<coordinates>'
		
		#Writes all the heading information of the KML file.
		#kmlFile.write(kmlFileStart1)
		#kmlFile.write(kmlFileStart2)
		for x in range(3,26):
			exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
		
		
		spacingCount = 1
		for x in dataList:
			
			y = x.replace(' - ','')
			
			#Calculates the longitudinal data.
			northDeg = int(y[0:2])
			northMin = int(y[2:4])/60
			northSec = int(y[4:6])/3600
			northDec = round(northDeg + northMin + northSec,5)
			northStr = str(northDec)
			
			#Calculates the latitudinal data.
			westDeg = int(y[8:11])
			westMin = int(y[11:13])/60
			westSec = int(y[13:15])/3600
			westDec = round(westDeg + westMin + westSec,5)
			westStr = '-' + str(westDec)
				
			#Writes coordinate information to kml file.
			#if spacingCount == 1:
			#	kmlFile.write('\t' + westStr + ', ' + northStr + ', ' + str(topAltitude) + '\n')
			#	spacingCount+=1
			#	
			#else:
			#	kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + westStr + ', ' + northStr + ', ' + str(topAltitude) + '\n')
			
			#Writes coordinate information to kml file.
			if spacingCount == 1:
				kmlFile.write(westStr + ',' + northStr + ',' + str(topAltitude))
				spacingCount+=1
				
			else:
				kmlFile.write(' ' + westStr + ',' + northStr + ',' + str(topAltitude))
			
			
		lowerFaceEnd1 = '</coordinates>\n'
		lowerFaceEnd2 = '\t\t\t\t\t</LinearRing>\n'
		lowerFaceEnd3 = '\t\t\t\t</outerBoundaryIs>\n'
		lowerFaceEnd4 = '\t\t\t</Polygon>\n'
		lowerFaceEnd5 = '\t\t</Placemark>\n'
		lowerFaceEnd6 = '\t</Document>\n'
		lowerFaceEnd7 = '</kml>\n'
		
		for x in range(1,6):
			exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')
		
		
		
		#---VERTICAL FACES---
		#This loop writes all of the vertical faces which make the shape look like a sealed box.
		#Create a list of decimal degree points.
		decimalDegreePoints = []
		for x in dataList:
			y = x.replace(' - ','')
			#Calculates the longitudinal data.
			northDeg = int(y[0:2])
			northMin = int(y[2:4])/60
			northSec = int(y[4:6])/3600
			northDec = round(northDeg + northMin + northSec,5)
			northStr = str(northDec)
			#Calculates the latitudinal data.
			westDeg = int(y[8:11])
			westMin = int(y[11:13])/60
			westSec = int(y[13:15])/3600
			westDec = round(westDeg + westMin + westSec,5)
			westStr = '-' + str(westDec)
			decimalDegreePoints.append(westStr + ', ' + northStr)
		#print(decimalDegreePoints)
		vFaceCount = len(dataList) - 1
		
		#Defines all the heading information of the KML file.
		lowerFaceStart3 = '\t\t<Placemark>\n'
		lowerFaceStart4 = '\t\t\t<name></name>\n'
		lowerFaceStart5 = '\t\t\t<description></description>\n'
		lowerFaceStart6 = '\t\t\t<Style>\n'
		lowerFaceStart7 = '\t\t\t\t<LineStyle>\n'
		lowerFaceStart8 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
		lowerFaceStart9 = '\t\t\t\t\t<width>6</width>\n'
		lowerFaceStart10 = '\t\t\t\t</LineStyle>\n'
		lowerFaceStart11 = '\t\t\t\t<PolyStyle>\n'
		lowerFaceStart12 = '\t\t\t\t\t<color>6B3644DB</color>\n'
		lowerFaceStart13 = '\t\t\t\t\t<fill>1</fill>\n'
		lowerFaceStart14 = '\t\t\t\t\t<outline>1</outline>\n'
		lowerFaceStart15 = '\t\t\t\t</PolyStyle>\n'
		lowerFaceStart16 = '\t\t\t\t<BalloonStyle>\n'
		lowerFaceStart17 = '\t\t\t\t\t<text></text>\n'
		lowerFaceStart18 = '\t\t\t\t</BalloonStyle>\n'
		lowerFaceStart19 = '\t\t\t</Style>\n'
		lowerFaceStart20 = '\t\t\t<Polygon>\n'
		lowerFaceStart21 = '\t\t\t\t<outerBoundaryIs>\n'
		lowerFaceStart22 = '\t\t\t\t\t<LinearRing>\n'
		lowerFaceStart23 = '\t\t\t\t\t\t<tessellate>1</tessellate>\n'
		lowerFaceStart24 = '\t\t\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
		lowerFaceStart25 = '\t\t\t\t\t\t\t<coordinates>'
		
		
		
		#This loop writes the vertical faces to file.
		for n in range(0,vFaceCount):
		
			for x in range(3,26):
				exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
			
			kmlFile.write('\t' + decimalDegreePoints[n] + ', ' + str(bottomAltitude) + '\n')
			kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + decimalDegreePoints[n+1] + ', ' + str(bottomAltitude) + '\n')
			kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + decimalDegreePoints[n+1] + ', ' + str(topAltitude) + '\n')
			kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + decimalDegreePoints[n] + ', ' + str(topAltitude) + '\n')
			kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + decimalDegreePoints[n] + ', ' + str(bottomAltitude) + '\n')
			
			lowerFaceEnd1 = '\t\t\t\t\t\t\t</coordinates>\n'
			lowerFaceEnd2 = '\t\t\t\t\t</LinearRing>\n'
			lowerFaceEnd3 = '\t\t\t\t</outerBoundaryIs>\n'
			lowerFaceEnd4 = '\t\t\t</Polygon>\n'
			lowerFaceEnd5 = '\t\t</Placemark>\n'
			
			for x in range(1,6):
				exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')

		lowerFaceEnd6 = '\t</Document>\n'
		lowerFaceEnd7 = '</kml>\n'
		kmlFile.write(lowerFaceEnd6)
		kmlFile.write(lowerFaceEnd7)
	
	#========================================================================================================================================================================

	#========================================================================================================================================================================
	
	if shape == '3D2':
		
		#I made this alternate 3D version for the EG_D202_WW zone. Since it was difficult to create the 2D area, the easiest way to make it 3D was to start from the decimal
		#degrees. So I made a modified version of the 3D option which reads in a list of decimal degree coordinates instead of calculating them on the fly. The format for the
		#decimal degrees need to be the two values with a comma (no spaces) separating them.
		
		#====================================================================================================================================================================
		#This part is the main difference, the coordinates are already converted so they are read in instead of converted on the fly.
		#Read in a list of pre-converted decimal degree coordinates.
		#decimalCoordFileName = input('Please enter the name of the file containing the pre-converted decimal coordinates:\n')
		decimalCoordFileName = fileName[:]
		decimalCoordFile = open(decimalCoordFileName,'r')
		decimalCoords = decimalCoordFile.read()
		decimalCoords = decimalCoords.split('\n')
		decimalCoordFile.close()
		
		
		northCoords = []
		westCoords = []
		for x in decimalCoords:
			
			if x != '':
				currentCoords = x.split(', ')
				northCoords.append(currentCoords[1])
				westCoords.append(currentCoords[0])
			
		dataList = northCoords[:]
		#====================================================================================================================================================================
		#====================================================================================================================================================================
		#3D2 Configuration
		
		#I have made the script request the altitudes so that the program doesn't have to be modified each time I run it.
		topAltitude = input('\nPlease enter the top altitude (meters):\n')
		bottomAltitude = input('\nPlease enter the bottom altitude (meters):\n')
		#topAltitude = 12500
		#bottomAltitude = 0
		
		shapeName = fileName.replace('.txt','')
		shapeDesc = ''
		
		
		
		#Creates an empty KML file from the coordinate information.
		kmlName = fileName.replace('.txt','_3DPolygon.kml')
		kmlFile = open(kmlName,'w')
		#====================================================================================================================================================================
		#====================================================================================================================================================================
		#---HORIZONTAL POLYGON 1---
		#Defines all the heading information of the KML file.
		kmlFileStart1 = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
		kmlFileStart2 = '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n'
		lowerFaceStart1 = '\t<Document>\n'
		lowerFaceStart2 = '\t\t<name>Layer 1</name>\n'
		lowerFaceStart3 = '\t\t<Placemark>\n'
		lowerFaceStart4 = '\t\t\t<name>' + shapeName + '</name>\n'
		lowerFaceStart5 = '\t\t\t<description>' + shapeDesc + '</description>\n'
		lowerFaceStart6 = '\t\t\t<Style>\n'
		lowerFaceStart7 = '\t\t\t\t<LineStyle>\n'
		lowerFaceStart8 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
		lowerFaceStart9 = '\t\t\t\t\t<width>6</width>\n'
		lowerFaceStart10 = '\t\t\t\t</LineStyle>\n'
		lowerFaceStart11 = '\t\t\t\t<PolyStyle>\n'
		lowerFaceStart12 = '\t\t\t\t\t<color>6B3644DB</color>\n'
		lowerFaceStart13 = '\t\t\t\t\t<fill>1</fill>\n'
		lowerFaceStart14 = '\t\t\t\t\t<outline>1</outline>\n'
		lowerFaceStart15 = '\t\t\t\t</PolyStyle>\n'
		lowerFaceStart16 = '\t\t\t\t<BalloonStyle>\n'
		lowerFaceStart17 = '\t\t\t\t\t<text></text>\n'
		lowerFaceStart18 = '\t\t\t\t</BalloonStyle>\n'
		lowerFaceStart19 = '\t\t\t</Style>\n'
		lowerFaceStart20 = '\t\t\t<Polygon>\n'
		lowerFaceStart21 = '\t\t\t\t<outerBoundaryIs>\n'
		lowerFaceStart22 = '\t\t\t\t\t<LinearRing>\n'
		lowerFaceStart23 = '\t\t\t\t\t\t<tessellate>1</tessellate>\n'
		lowerFaceStart24 = '\t\t\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
		lowerFaceStart25 = '\t\t\t\t\t\t\t<coordinates>'
		
		#Writes all the heading information of the KML file.
		kmlFile.write(kmlFileStart1)
		kmlFile.write(kmlFileStart2)
		for x in range(1,26):
			exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
		
		#Spacing count is only used to make sure the white space padding the front of the coordinates is consistent.
		spacingCount = 1		
		#Writes coordinate information to kml file.
		#for nc,wc in zip(northCoords,westCoords):
		#	if spacingCount == 1:
		#		kmlFile.write('\t' + wc + ', ' + nc + ', ' + str(bottomAltitude) + '\n')
		#		spacingCount+=1
		#		
		#	else:
		#		kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + wc + ', ' + nc + ', ' + str(bottomAltitude) + '\n')
				
		#Writes coordinate information to kml file.
		for nc,wc in zip(northCoords,westCoords):
			if spacingCount == 1:
				kmlFile.write(wc + ',' + nc + ',' + str(bottomAltitude))
				spacingCount+=1
				
			else:
				kmlFile.write(' ' + wc + ',' + nc + ',' + str(bottomAltitude))
		
		
		lowerFaceEnd1 = '</coordinates>\n'
		lowerFaceEnd2 = '\t\t\t\t\t</LinearRing>\n'
		lowerFaceEnd3 = '\t\t\t\t</outerBoundaryIs>\n'
		lowerFaceEnd4 = '\t\t\t</Polygon>\n'
		lowerFaceEnd5 = '\t\t</Placemark>\n'
		lowerFaceEnd6 = '\t</Document>\n'
		lowerFaceEnd7 = '</kml>\n'
		
		for x in range(1,6):
			exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')
		#====================================================================================================================================================================
		#---HORIZONTAL POLYGON 2---
		#This writes the second 2D polygon which is at the higher altitude.
		#Defines all the heading information of the KML file.
		kmlFileStart1 = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
		kmlFileStart2 = '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n'
		lowerFaceStart1 = '\t<Document>\n'
		lowerFaceStart2 = '\t\t<name>Layer 1</name>\n'
		lowerFaceStart3 = '\t\t<Placemark>\n'
		lowerFaceStart4 = '\t\t\t<name></name>\n'
		lowerFaceStart5 = '\t\t\t<description></description>\n'
		lowerFaceStart6 = '\t\t\t<Style>\n'
		lowerFaceStart7 = '\t\t\t\t<LineStyle>\n'
		lowerFaceStart8 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
		lowerFaceStart9 = '\t\t\t\t\t<width>6</width>\n'
		lowerFaceStart10 = '\t\t\t\t</LineStyle>\n'
		lowerFaceStart11 = '\t\t\t\t<PolyStyle>\n'
		lowerFaceStart12 = '\t\t\t\t\t<color>6B3644DB</color>\n'
		lowerFaceStart13 = '\t\t\t\t\t<fill>1</fill>\n'
		lowerFaceStart14 = '\t\t\t\t\t<outline>1</outline>\n'
		lowerFaceStart15 = '\t\t\t\t</PolyStyle>\n'
		lowerFaceStart16 = '\t\t\t\t<BalloonStyle>\n'
		lowerFaceStart17 = '\t\t\t\t\t<text></text>\n'
		lowerFaceStart18 = '\t\t\t\t</BalloonStyle>\n'
		lowerFaceStart19 = '\t\t\t</Style>\n'
		lowerFaceStart20 = '\t\t\t<Polygon>\n'
		lowerFaceStart21 = '\t\t\t\t<outerBoundaryIs>\n'
		lowerFaceStart22 = '\t\t\t\t\t<LinearRing>\n'
		lowerFaceStart23 = '\t\t\t\t\t\t<tessellate>1</tessellate>\n'
		lowerFaceStart24 = '\t\t\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
		lowerFaceStart25 = '\t\t\t\t\t\t\t<coordinates>'
		
		#Writes all the heading information of the KML file.
		#kmlFile.write(kmlFileStart1)
		#kmlFile.write(kmlFileStart2)
		for x in range(3,26):
			exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
		
		#Spacing count is only used to make sure the white space padding the front of the coordinates is consistent.
		spacingCount = 1		
		#Writes coordinate information to kml file.
		for nc,wc in zip(northCoords,westCoords):
			if spacingCount == 1:
				kmlFile.write(wc + ',' + nc + ',' + str(topAltitude))
				spacingCount+=1
				
			else:
				kmlFile.write(' ' + wc + ',' + nc + ',' + str(topAltitude))
		
		
		lowerFaceEnd1 = '</coordinates>\n'
		lowerFaceEnd2 = '\t\t\t\t\t</LinearRing>\n'
		lowerFaceEnd3 = '\t\t\t\t</outerBoundaryIs>\n'
		lowerFaceEnd4 = '\t\t\t</Polygon>\n'
		lowerFaceEnd5 = '\t\t</Placemark>\n'
		lowerFaceEnd6 = '\t</Document>\n'
		lowerFaceEnd7 = '</kml>\n'
		
		for x in range(1,6):
			exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')
		#====================================================================================================================================================================
		#====================================================================================================================================================================
		vFaceCount = len(dataList) - 1
		decimalDegreePoints = decimalCoords[:]
		
		#This loop creates the vertical faces.
		for n in range(0,vFaceCount):
			
			kmlFileStart1 = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
			kmlFileStart2 = '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n'
			lowerFaceStart1 = '\t<Document>\n'
			lowerFaceStart2 = '\t\t<name>Layer 1</name>\n'
			lowerFaceStart3 = '\t\t<Placemark>\n'
			lowerFaceStart4 = '\t\t\t<name></name>\n'
			lowerFaceStart5 = '\t\t\t<description></description>\n'
			lowerFaceStart6 = '\t\t\t<Style>\n'
			lowerFaceStart7 = '\t\t\t\t<LineStyle>\n'
			lowerFaceStart8 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
			lowerFaceStart9 = '\t\t\t\t\t<width>6</width>\n'
			lowerFaceStart10 = '\t\t\t\t</LineStyle>\n'
			lowerFaceStart11 = '\t\t\t\t<PolyStyle>\n'
			lowerFaceStart12 = '\t\t\t\t\t<color>6B3644DB</color>\n'
			lowerFaceStart13 = '\t\t\t\t\t<fill>1</fill>\n'
			lowerFaceStart14 = '\t\t\t\t\t<outline>1</outline>\n'
			lowerFaceStart15 = '\t\t\t\t</PolyStyle>\n'
			lowerFaceStart16 = '\t\t\t\t<BalloonStyle>\n'
			lowerFaceStart17 = '\t\t\t\t\t<text></text>\n'
			lowerFaceStart18 = '\t\t\t\t</BalloonStyle>\n'
			lowerFaceStart19 = '\t\t\t</Style>\n'
			lowerFaceStart20 = '\t\t\t<Polygon>\n'
			lowerFaceStart21 = '\t\t\t\t<outerBoundaryIs>\n'
			lowerFaceStart22 = '\t\t\t\t\t<LinearRing>\n'
			lowerFaceStart23 = '\t\t\t\t\t\t<tessellate>1</tessellate>\n'
			lowerFaceStart24 = '\t\t\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
			lowerFaceStart25 = '\t\t\t\t\t\t\t<coordinates>'
			
			#Writes all the heading information of the KML file.
			#kmlFile.write(kmlFileStart1)
			#kmlFile.write(kmlFileStart2)
			for x in range(3,26):
				exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
		
			
			#kmlFile.write('\t' + (decimalDegreePoints[n].split(',')[0]) + ', ' (decimalDegreePoints[n].split(',')[1]) + ', ' + str(bottomAltitude) + '\n')
			#kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + (decimalDegreePoints[n+1].split(',')[0]) + ', ' (decimalDegreePoints[n+1].split(',')[1]) + ', ' + str(bottomAltitude) + '\n')
			#kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + (decimalDegreePoints[n+1].split(',')[0]) + ', ' (decimalDegreePoints[n+1].split(',')[1]) + ', ' + str(topAltitude) + '\n')
			#kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + (decimalDegreePoints[n].split(',')[0]) + ', ' (decimalDegreePoints[n].split(',')[1]) + ', ' + str(topAltitude) + '\n')
			#kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + (decimalDegreePoints[n].split(',')[0]) + ', ' (decimalDegreePoints[n].split(',')[1]) + ', ' + str(bottomAltitude) + '\n')
			
			kmlFile.write('\t' + decimalDegreePoints[n] + ', ' + str(bottomAltitude) + '\n')
			kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + decimalDegreePoints[n+1] + ', ' + str(bottomAltitude) + '\n')
			kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + decimalDegreePoints[n+1] + ', ' + str(topAltitude) + '\n')
			kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + decimalDegreePoints[n] + ', ' + str(topAltitude) + '\n')
			kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + decimalDegreePoints[n] + ', ' + str(bottomAltitude) + '\n')
			
			
			
			#print(decimalDegreePoints[n].split(',')[0])
			
			lowerFaceEnd1 = '\t\t\t\t\t\t\t</coordinates>\n'
			lowerFaceEnd2 = '\t\t\t\t\t</LinearRing>\n'
			lowerFaceEnd3 = '\t\t\t\t</outerBoundaryIs>\n'
			lowerFaceEnd4 = '\t\t\t</Polygon>\n'
			lowerFaceEnd5 = '\t\t</Placemark>\n'
			lowerFaceEnd6 = '\t</Document>\n'
			lowerFaceEnd7 = '</kml>\n'
			
			for x in range(1,6):
				exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')
		#====================================================================================================================================================================
		kmlFileEnd1 = '\t</Document>\n'
		kmlFileEnd2 = '</kml>'
		kmlFile.write(kmlFileEnd1)
		kmlFile.write(kmlFileEnd2)
		
	#file.close()
	kmlFile.close()
	print('Done')


def kml_create1():

	"""Used to create a KML file from a list of coordinates.
	
	I made this script to help me convert the coordinates for the EG D201 danger areas
	into KML files which could be loaded into various GIS software like Global Mapper
	and SOCET etc.
	
	The script can generate the following KML types:
		- points		IN PROGRESS
		- line			COMPLETE
		- circle		IN PROGRESS
		- 2D polygon	COMPLETE
		- 3D polygon	STATUS UNKNOWN
	
	The script expects decimal degree input data in the same format
	as is output by the 'co-conv' script i.e. "latitude, longitude".
	
	"""
	
	#	Import required Python libraries.
	import os
	import sys
	import math
	
	#-----------------------------------------------------------------------------------------------------------------------------------------------
	#	Notice about input file format.
	print('NOTICE: This program can only accept coordinates in the following format:\n')
	print('    {0}, {1} e.g...\n    {2}, {3}\n    {4}, {5}'.format('Latitude', 'Longitude', 52.13916658, -4.558604992, 31.13967891, -8.558468137))
	#input('\nPlease press enter to continue...')
	
	#-----------------------------------------------------------------------------------------------------------------------------------------------
	#	Choose KML type.
	#Define an object to hold valid KML types.
	kmlTypes = ['line','circle','2D','3D','3D2']
	kmlTypesString = ''
	
	for x in range(0,len(kmlTypes)):
	
		if x == (len(kmlTypes) -1):
			kmlTypesString += kmlTypes[x]
		elif x == (len(kmlTypes) -2):
			kmlTypesString += kmlTypes[x] + ' or '
		else:
			kmlTypesString += kmlTypes[x] + ', '
	
	#Prompt the user to specify what type of shape to create.
	shape = input('\nPlease specify the type of shape (' + kmlTypesString + '):\n')
	
	#Check that a valid kml type choice was made, otherwise exit the program.
	if shape in kmlTypes:
		kmlChoice = True
	else:
		raise NameError('Invalid KML type chosen!')
	
	#The circle KMLs only need a single coordinate which is typed into the command prompt, don't need to open a file.
	#Otherwise open a file to read input coordinates.
	if shape != 'circle':
		#-----------------------------------------------------------------------------------------------------------------------------------------------
		#	Find input file.
		#Keywords to look for in file name.
		keyWord = input('\nPlease enter a keyword to help identify input files:\n')

		#Get a list of all the files in the directory and show the user the files which they are likely to want to use.
		files = os.listdir()
		smartFiles = []
		for x in files:
			if keyWord in x :
				smartFiles.append(x)

		print(' ')
		n = 0
		for x in smartFiles:
			print(str(n) + ' - ' + x)
			n+=1
		
		#Prompt the user the enter the number associated with the file they want to use.
		fileNumber = input('\nPlease select a file by entering the number listed next to your filename:\n')
		fileName = smartFiles[int(fileNumber)]
		shapeName = fileName.replace('_decimal.txt','')
	
		file = open(fileName,'r')
		data = file.read()
		
		#Put data into list format.
		rawDataList = data.split('\n')
		dataList = []
		for item in rawDataList:
			if item != '':
				dataList.append(item)
		
		#Create two separate lists, one for Longitude and one for Latitude.
		FirstCoords = []
		SecondCoords = []
		for pair in dataList:
			a = pair.split(', ')
			FirstCoords.append(a[0])
			SecondCoords.append(a[1])
	
	
	
		
	#=====================================================================================
	#	CONFIGURATION AND STYLING
	#=====================================================================================
	#	This sections is used to define the various static options.
	
	#PARAMETERS
	#Single altitude setter. This is now deprecated for circle and needs to be deprecated for other types.
	simpleAltitude = 12500
	
	#Altitude mode selector.
	altitudeMode = 'relativeToGround'
    #Altitude modes:
	# absolute
    # clampToGround
    # clampToSeaFloor
    # relativeToGround
    # relativeToSeaFloor
	
	#STYLE
	LineWidth = 2
	LineColour = 'ff3644DB'
	AreaColour = '6B3644DB'#Not yet implemented.
	
	#=====================================================================================
	#	CONFIGURATION AND STYLING	
	#=====================================================================================
	
	if shape == 'circle':
		#========================================================================================================================================================================
		#Creates an empty KML file from the coordinate information.
		
		#========================================================================================================================================================================
		#Get the centre of the circle from the user.
		centerCircleCoordsStr = input('\nPlease enter the coordinates for the center of the circle in the\nfollowing format:\n\nlatitude, longitude:\n')
		centerCircleCoords = centerCircleCoordsStr.split(', ')
		
		centerCircleLat = float(centerCircleCoords[0])
		centerCircleLng = float(centerCircleCoords[1])
		
		circleRadiusString = input('\n - RADIUS - Please enter the radius of the circle:\nkm = Kilometers\nnm = Nautical Miles\nm = Meters\nM = Miles\n\n> ')
		
		if 'km' in circleRadiusString:
			a = circleRadiusString.replace('km','')
			circleRadiusKm = int(a)
		elif 'nm' in circleRadiusString:
			a = circleRadiusString.replace('nm','')
			circleRadiusKm = int(a) * 1.852
		elif 'M' in circleRadiusString:
			a = circleRadiusString.replace('M','')
			circleRadiusKm = int(a) * 1.60934
		elif 'm' in circleRadiusString:
			a = circleRadiusString.replace('m','')
			circleRadiusKm = int(a) / 1000
		
		circleRadiusM = circleRadiusKm * 1000
		
		#========================================================================================================================================================================
		#Get altitude value.
		circleAltitudeString = input('\n - ALTITUDE - Please enter an altitude for the KML:\nkm = Kilometers\nm = Meters\nM = Miles\nft = Feet\nnm = Nautical Miles\n\n> ')
		
		if 'km' in circleAltitudeString:
			a = circleAltitudeString.replace('km','')
			circleAltitudeKm = int(a)
			
		elif 'nm' in circleAltitudeString:
			a = circleAltitudeString.replace('nm','')
			circleAltitudeKm = int(a) * 1.852
			
		elif 'ft' in circleAltitudeString:
			a = circleAltitudeString.replace('ft','')
			circleAltitudeKm = int(a) / (3.28084*1000)
			
		elif 'M' in circleAltitudeString:
			a = circleAltitudeString.replace('M','')
			circleAltitudeKm = int(a) * 1.60934
			
		elif 'm' in circleAltitudeString:
			a = circleAltitudeString.replace('m','')
			circleAltitudeKm = int(a) / 1000
			
		#Altitude must be entered in meters.
		circleAltitudeM = circleAltitudeKm * 1000
		
		#========================================================================================================================================================================
		#Get name for KML and output file.
		outputFileNameStart = input('\nPlease enter a name for the shape file:\n')
		outputFileName = outputFileNameStart + '_circle.kml'
		shapeName = outputFileNameStart
		kmlName = outputFileName
		
		#========================================================================================================================================================================
		#Specify if the circle should have a place mark in the centre.
		placemark = input('\nAdd placemark to centre of circle? [y/n]:\n')
		
		#========================================================================================================================================================================
		#Choose whether the circle should be a ring or a disk.
		circleStyle = input('\nSpecify if the circle should be shaded (disk) or empty (ring) [disk/ring]:\n')
		
		#========================================================================================================================================================================
		#Mean Earth radius
		earthRadius_km = 6371
		earthRadius_m = earthRadius_km * 1000
		
		#Distance is entered in km, convert to meters.
		dist = circleRadiusM
		
		#Convert coordinates to numbers.
		latDeg = centerCircleLat
		lngDeg = centerCircleLng
		
		#Convert coordinates from degrees to radians.
		latRad = math.radians(latDeg)
		lngRad = math.radians(lngDeg)
		
		#Create a list of angles at which to create points (how many points will the circle consist of).
		numPoints = range(0,360,int(360/36))
		angles = []
		for x in numPoints:
			angles.append(float(x))
		angles.append(float(0))
		
		#circleCoordinates = ''
		circleCoordinatesList = []
		
		#Loop through bearings and create a coordinate pair at each angle.
		for x in angles:
		
			bearing = math.radians(x)
		
			newLat = math.asin(math.sin(latRad) * math.cos(dist/earthRadius_m) + math.cos(latRad) * math.sin(dist/earthRadius_m) * math.cos(bearing))
			
			newLng = lngRad + math.atan2(math.sin(bearing) * math.sin(dist/earthRadius_m) * math.cos(latRad), math.cos(dist/earthRadius_m) - math.sin(latRad) * math.sin(newLat))
			
			newLatDeg = math.degrees(newLat)
			newLngDeg = math.degrees(newLng)
			
			#print('{0}, {1}'.format(str(newLatDeg), str(newLngDeg)))
			
			#outputFile.write('{0}, {1}\n'.format(str(newLatDeg), str(newLngDeg)))
			
			#circleCoordinates += '{0}, {1}\n'.format(str(newLatDeg), str(newLngDeg))
			
			circleCoordinatesList.append([str(newLatDeg), str(newLngDeg)])
		
		
		#========================================================================================================================================================================	
		#Output to describe what is being made.
		print('\n=================================================================')
		print('Creating a circle KML.')
		print("The KML shape's name will be >> "+ kmlName)
		print('KML circle radius: ' + str(circleRadiusKm) + ' km.')
		print('KML circle altitude: ' + str(circleAltitudeKm) + ' km.')
		print('Generating...')
			
		kmlFile = open(kmlName,'w')
	
		#Defines all the heading information of the KML file.
		kmlFileStart1 = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
		kmlFileStart2 = '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n'
		lowerFaceStart1 = '\t<Document>\n'
		lowerFaceStart2 = '\t\t<name>Layer 1</name>\n'
		
		#If the user has specified to put a placemark in the middle of the circle.
		if placemark == 'y':
			lowerFaceStart3 = '\t\t<Placemark>\n'
			lowerFaceStart4 = '\t\t\t<name>' + shapeName + '</name>\n'
			lowerFaceStart5 = '\t\t\t<description>Insert description here.</description>\n'
			lowerFaceStart6 = '\t\t\t<Point>\n'
			lowerFaceStart7 = '\t\t\t\t<coordinates>' + str(centerCircleLng) + ',' + str(centerCircleLat) + ',' + str(circleAltitudeM) + '</coordinates>\n'
			lowerFaceStart8 = '\t\t\t</Point>\n'
			lowerFaceStart9 = '\t\t</Placemark>\n'
		else:
			lowerFaceStart3 = ''
			lowerFaceStart4 = ''
			lowerFaceStart5 = ''
			lowerFaceStart6 = ''
			lowerFaceStart7 = ''
			lowerFaceStart8 = ''
			lowerFaceStart9 = ''
		
		lowerFaceStart10 = '\t\t<Placemark>\n'
		lowerFaceStart11 = '\t\t\t<name>' + shapeName + ' ' + str(circleRadiusKm) + 'km ring' + '</name>\n'
		lowerFaceStart12 = '\t\t\t<description>Insert description here.</description>\n'
		lowerFaceStart13 = '\t\t\t<Style>\n'
		lowerFaceStart14 = '\t\t\t\t<LineStyle>\n'
		lowerFaceStart15 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
		lowerFaceStart16 = '\t\t\t\t\t<width>' + str(LineWidth) + '</width>\n'
		lowerFaceStart17 = '\t\t\t\t</LineStyle>\n'
		lowerFaceStart18 = '\t\t\t\t<PolyStyle>\n'
		lowerFaceStart19 = '\t\t\t\t\t<color>6B3644DB</color>\n'
		lowerFaceStart20 = '\t\t\t\t\t<fill>1</fill>\n'
		lowerFaceStart21 = '\t\t\t\t\t<outline>1</outline>\n'
		lowerFaceStart22 = '\t\t\t\t</PolyStyle>\n'
		lowerFaceStart23 = '\t\t\t\t<BalloonStyle>\n'
		lowerFaceStart24 = '\t\t\t\t\t<text>Insert text here.</text>\n'
		lowerFaceStart25 = '\t\t\t\t</BalloonStyle>\n'
		lowerFaceStart26 = '\t\t\t</Style>\n'
		
		#If the circle is just a ring.
		if circleStyle == 'ring':
			lowerFaceStart27 = '\t\t\t<LineString>\n'
			lowerFaceStart28 = '\t\t\t\t<extrude>1</extrude>\n'
			lowerFaceStart29 = '\t\t\t\t<tessellate>1</tessellate>\n'
			lowerFaceStart30 = '\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
			lowerFaceStart31 = '\t\t\t\t<coordinates>\n'
			
			#Writes all the heading information of the KML file.
			kmlFile.write(kmlFileStart1)
			kmlFile.write(kmlFileStart2)
			for x in range(1,32):
				exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
			
			
			
			#Write the coordinates to the file.
			for x in range(0, len(circleCoordinatesList)):
				#Format the output string.
				outputDataFormatted = formatCoordOutput(circleCoordinatesList[x][0],circleCoordinatesList[x][1],circleAltitudeM)
				if x == 0:
					kmlFile.write('\t\t\t\t\t\t\t' + outputDataFormatted)
				else:
					kmlFile.write('\t\t\t\t\t\t\t' + outputDataFormatted)
					
			lowerFaceEnd1 = '\t\t\t\t</coordinates>\n'
			lowerFaceEnd2 = '\t\t\t</LineString>\n'
			lowerFaceEnd3 = '\t\t</Placemark>\n'
			lowerFaceEnd4 = '\t</Document>\n'
			lowerFaceEnd5 = '</kml>\n'
			
			#Writes all the footer information of the KML file.
			for x in range(1,6):
				exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')
			
		#If the circle is shaded in like a disk.
		if circleStyle == 'disk':	
			lowerFaceStart27 = '\t\t\t<Polygon>\n'
			lowerFaceStart28 = '\t\t\t\t<outerBoundaryIs>\n'
			lowerFaceStart29 = '\t\t\t\t\t<LinearRing>\n'
			lowerFaceStart30 = '\t\t\t\t\t\t<tessellate>1</tessellate>\n'
			lowerFaceStart31 = '\t\t\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
			lowerFaceStart32 = '\t\t\t\t\t\t\t<coordinates>\n'
			
			#Writes all the heading information of the KML file.
			kmlFile.write(kmlFileStart1)
			kmlFile.write(kmlFileStart2)
			for x in range(1,33):
				exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
			
			#Write the coordinates to the file.
			for x in range(0, len(circleCoordinatesList)):
				#Format the output string.
				outputDataFormatted = formatCoordOutput(circleCoordinatesList[x][0],circleCoordinatesList[x][1],circleAltitudeM)
				if x == 0:
					kmlFile.write('\t\t\t\t\t\t\t' + outputDataFormatted)
				else:
					kmlFile.write('\t\t\t\t\t\t\t' + outputDataFormatted)
					
			lowerFaceEnd1 = '\t\t\t\t\t\t\t</coordinates>\n'
			lowerFaceEnd2 = '\t\t\t\t\t</LinearRing>\n'
			lowerFaceEnd3 = '\t\t\t\t</outerBoundaryIs>\n'
			lowerFaceEnd4 = '\t\t\t</Polygon>\n'
			lowerFaceEnd5 = '\t\t</Placemark>\n'
			lowerFaceEnd6 = '\t</Document>\n'
			lowerFaceEnd7 = '</kml>\n'
			
			#Writes all the footer information of the KML file.
			for x in range(1,8):
				exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')
		#========================================================================================================================================================================
	
	if shape == 'line':
		#========================================================================================================================================================================
		#Creates an empty KML file from the coordinate information.
		
		fileNameParts = fileName.split('.')
		inputFileExtension = fileNameParts[-1]
		nameModConfirm = input('\nThe input file extension is .' + inputFileExtension + '? [y/n]:\n')
		
		if(nameModConfirm == 'y'):
			kmlName = fileName.replace('.' + inputFileExtension,'_line.kml')
			
		#Output to describe what is being made.
		input('\n=================================================================\nCreating a '
		+ shape + ' KML from:\n\n> ' + smartFiles[int(fileNumber)] + "\n\nThe KML shape's name will be:\n\n> "
		+ kmlName + '\n\nPlease press enter to continue...')
			
		kmlFile = open(kmlName,'w')
	
		#Defines all the heading information of the KML file.
		kmlFileStart1 = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
		kmlFileStart2 = '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n'
		lowerFaceStart1 = '\t<Document>\n'
		lowerFaceStart2 = '\t\t<name>Layer 1</name>\n'
		lowerFaceStart3 = '\t\t<Placemark>\n'
		lowerFaceStart4 = '\t\t\t<name>' + shapeName + '</name>\n'
		lowerFaceStart5 = '\t\t\t<description>Insert description here.</description>\n'
		lowerFaceStart6 = '\t\t\t<Style>\n'
		lowerFaceStart7 = '\t\t\t\t<LineStyle>\n'
		lowerFaceStart8 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
		lowerFaceStart9 = '\t\t\t\t\t<width>' + str(LineWidth) + '</width>\n'
		lowerFaceStart10 = '\t\t\t\t</LineStyle>\n'
		lowerFaceStart11 = '\t\t\t\t<PolyStyle>\n'
		lowerFaceStart12 = '\t\t\t\t\t<color>6B3644DB</color>\n'
		lowerFaceStart13 = '\t\t\t\t\t<fill>1</fill>\n'
		lowerFaceStart14 = '\t\t\t\t\t<outline>1</outline>\n'
		lowerFaceStart15 = '\t\t\t\t</PolyStyle>\n'
		lowerFaceStart16 = '\t\t\t\t<BalloonStyle>\n'
		lowerFaceStart17 = '\t\t\t\t\t<text>Insert text here.</text>\n'
		lowerFaceStart18 = '\t\t\t\t</BalloonStyle>\n'
		lowerFaceStart19 = '\t\t\t</Style>\n'
		lowerFaceStart20 = '\t\t\t<LineString>\n'
		lowerFaceStart21 = '\t\t\t\t<extrude>1</extrude>\n'
		lowerFaceStart22 = '\t\t\t\t<tessellate>1</tessellate>\n'
		lowerFaceStart23 = '\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
		lowerFaceStart24 = '\t\t\t\t<coordinates>'
		
		#Writes all the heading information of the KML file.
		kmlFile.write(kmlFileStart1)
		kmlFile.write(kmlFileStart2)
		for x in range(1,25):
			exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
		
		
		spacingCount = 1
		for x, y in zip(FirstCoords, SecondCoords):
			
			northStr = str(x)
			
			westStr = str(y)
				
			#Writes coordinate information to kml file.
			if spacingCount == 1:
				kmlFile.write('\t' + westStr + ', ' + northStr + ', ' + str(simpleAltitude) + '\n')
				spacingCount+=1
				
			else:
				kmlFile.write('\t\t\t\t\t\t\t\t' + westStr + ', ' + northStr + ', ' + str(simpleAltitude) + '\n')
				
		lowerFaceEnd1 = '\t\t\t\t</coordinates>\n'
		lowerFaceEnd2 = '\t\t\t</LineString>\n'
		lowerFaceEnd3 = '\t\t</Placemark>\n'
		lowerFaceEnd4 = '\t</Document>\n'
		lowerFaceEnd5 = '</kml>\n'
		
		for x in range(1,6):
			exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')
		#========================================================================================================================================================================
	
	if shape == '2D':
		#========================================================================================================================================================================
		#Get altitude value.
		circleAltitudeString = input('\nPlease enter an altitude for the KML:\nkm = Kilometers\nm = Meters\nM = Miles\nft = Feet\nnm = Nautical Miles\n\n> ')
		
		if 'km' in circleAltitudeString:
			a = circleAltitudeString.replace('km','')
			circleAltitudeKm = int(a)
			
		elif 'nm' in circleAltitudeString:
			a = circleAltitudeString.replace('nm','')
			circleAltitudeKm = int(a) * 1.852
			
		elif 'ft' in circleAltitudeString:
			a = circleAltitudeString.replace('ft','')
			circleAltitudeKm = int(a) / (3.28084*1000)
			
		elif 'M' in circleAltitudeString:
			a = circleAltitudeString.replace('M','')
			circleAltitudeKm = int(a) * 1.60934
			
		elif 'm' in circleAltitudeString:
			a = circleAltitudeString.replace('m','')
			circleAltitudeKm = int(a) / 1000
			
		#Altitude must be entered in meters.
		circleAltitudeM = circleAltitudeKm * 1000
		
		#Creates an empty KML file from the coordinate information.
		kmlName = fileName.replace('.txt','_2DPolygon.kml')
		kmlFile = open(kmlName,'w')
	
		#Defines all the heading information of the KML file.
		kmlFileStart1 = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
		kmlFileStart2 = '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n'
		lowerFaceStart1 = '\t<Document>\n'
		lowerFaceStart2 = '\t\t<name>Layer 1</name>\n'
		lowerFaceStart3 = '\t\t<Placemark>\n'
		lowerFaceStart4 = '\t\t\t<name>' + shapeName + '</name>\n'
		lowerFaceStart5 = '\t\t\t<description>Insert description here.</description>\n'
		lowerFaceStart6 = '\t\t\t<Style>\n'
		lowerFaceStart7 = '\t\t\t\t<LineStyle>\n'
		lowerFaceStart8 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
		lowerFaceStart9 = '\t\t\t\t\t<width>' + str(LineWidth) + '</width>\n'
		lowerFaceStart10 = '\t\t\t\t</LineStyle>\n'
		lowerFaceStart11 = '\t\t\t\t<PolyStyle>\n'
		lowerFaceStart12 = '\t\t\t\t\t<color>6B3644DB</color>\n'
		lowerFaceStart13 = '\t\t\t\t\t<fill>1</fill>\n'
		lowerFaceStart14 = '\t\t\t\t\t<outline>1</outline>\n'
		lowerFaceStart15 = '\t\t\t\t</PolyStyle>\n'
		lowerFaceStart16 = '\t\t\t\t<BalloonStyle>\n'
		lowerFaceStart17 = '\t\t\t\t\t<text>Insert text here.</text>\n'
		lowerFaceStart18 = '\t\t\t\t</BalloonStyle>\n'
		lowerFaceStart19 = '\t\t\t</Style>\n'
		lowerFaceStart20 = '\t\t\t<Polygon>\n'
		lowerFaceStart21 = '\t\t\t\t<outerBoundaryIs>\n'
		lowerFaceStart22 = '\t\t\t\t\t<LinearRing>\n'
		lowerFaceStart23 = '\t\t\t\t\t\t<tessellate>1</tessellate>\n'
		lowerFaceStart24 = '\t\t\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
		lowerFaceStart25 = '\t\t\t\t\t\t\t<coordinates>'
		
		#Writes all the heading information of the KML file.
		kmlFile.write(kmlFileStart1)
		kmlFile.write(kmlFileStart2)
		for x in range(1,26):
			exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
		
		
		spacingCount = 1
		for x, y in zip(FirstCoords, SecondCoords):
			
			northStr = str(x)
			
			westStr = str(y)
				
			#Writes coordinate information to kml file.
			if spacingCount == 1:
				kmlFile.write('\t' + westStr + ', ' + northStr + ', ' + str(circleAltitudeM) + '\n')
				spacingCount+=1
				
			else:
				kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + westStr + ', ' + northStr + ', ' + str(circleAltitudeM) + '\n')
				
		lowerFaceEnd1 = '\t\t\t\t\t\t\t</coordinates>\n'
		lowerFaceEnd2 = '\t\t\t\t\t</LinearRing>\n'
		lowerFaceEnd3 = '\t\t\t\t</outerBoundaryIs>\n'
		lowerFaceEnd4 = '\t\t\t</Polygon>\n'
		lowerFaceEnd5 = '\t\t</Placemark>\n'
		lowerFaceEnd6 = '\t</Document>\n'
		lowerFaceEnd7 = '</kml>\n'
		
		for x in range(1,8):
			exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')
		#========================================================================================================================================================================
		
	
		
	if shape == '3D':
		#========================================================================================================================================================================
		#3D Configuration.
		#This has been modified so that it formats the coordinates of the horizontal areas in the official KML standard thus allowing GXP Xplorer to display the KML files.
		
		#I have made the script request the altitudes so that the program doesn't have to be modified each time I run it.
		topAltitude = input('Please enter the top altitude (meters): ')
		bottomAltitude = input('Please enter the bottom altitude (meters): ')
		#topAltitude = 23000
		#bottomAltitude = 0
		
		#Creates an empty KML file from the coordinate information.
		kmlName = fileName.replace('.txt','_3DPolygon.kml')
		kmlFile = open(kmlName,'w')
		
		shapeName = fileName.replace('.txt','')
		shapeDesc = ''
	
		#---HORIZONTAL POLYGON 1---
		#Defines all the heading information of the KML file.
		kmlFileStart1 = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
		kmlFileStart2 = '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n'
		lowerFaceStart1 = '\t<Document>\n'
		lowerFaceStart2 = '\t\t<name>Layer 1</name>\n'
		lowerFaceStart3 = '\t\t<Placemark>\n'
		lowerFaceStart4 = '\t\t\t<name>' + shapeName + '</name>\n'
		lowerFaceStart5 = '\t\t\t<description>' + shapeDesc + '</description>\n'
		lowerFaceStart6 = '\t\t\t<Style>\n'
		lowerFaceStart7 = '\t\t\t\t<LineStyle>\n'
		lowerFaceStart8 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
		lowerFaceStart9 = '\t\t\t\t\t<width>6</width>\n'
		lowerFaceStart10 = '\t\t\t\t</LineStyle>\n'
		lowerFaceStart11 = '\t\t\t\t<PolyStyle>\n'
		lowerFaceStart12 = '\t\t\t\t\t<color>6B3644DB</color>\n'
		lowerFaceStart13 = '\t\t\t\t\t<fill>1</fill>\n'
		lowerFaceStart14 = '\t\t\t\t\t<outline>1</outline>\n'
		lowerFaceStart15 = '\t\t\t\t</PolyStyle>\n'
		lowerFaceStart16 = '\t\t\t\t<BalloonStyle>\n'
		lowerFaceStart17 = '\t\t\t\t\t<text></text>\n'
		lowerFaceStart18 = '\t\t\t\t</BalloonStyle>\n'
		lowerFaceStart19 = '\t\t\t</Style>\n'
		lowerFaceStart20 = '\t\t\t<Polygon>\n'
		lowerFaceStart21 = '\t\t\t\t<outerBoundaryIs>\n'
		lowerFaceStart22 = '\t\t\t\t\t<LinearRing>\n'
		lowerFaceStart23 = '\t\t\t\t\t\t<tessellate>1</tessellate>\n'
		lowerFaceStart24 = '\t\t\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
		lowerFaceStart25 = '\t\t\t\t\t\t\t<coordinates>'
		
		#Writes all the heading information of the KML file.
		kmlFile.write(kmlFileStart1)
		kmlFile.write(kmlFileStart2)
		for x in range(1,26):
			exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
		
		
		spacingCount = 1
		for x in dataList:
			
			y = x.replace(' - ','')
			
			#Calculates the longitudinal data.
			northDeg = int(y[0:2])
			northMin = int(y[2:4])/60
			northSec = int(y[4:6])/3600
			northDec = round(northDeg + northMin + northSec,5)
			northStr = str(northDec)
			
			#Calculates the latitudinal data.
			westDeg = int(y[8:11])
			westMin = int(y[11:13])/60
			westSec = int(y[13:15])/3600
			westDec = round(westDeg + westMin + westSec,5)
			westStr = '-' + str(westDec)
				
			#Writes coordinate information to kml file.
			#if spacingCount == 1:
			#	kmlFile.write('\t' + westStr + ', ' + northStr + ', ' + str(bottomAltitude) + '\n')
			#	
			#	spacingCount+=1
			#	
			#else:
			#	kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + westStr + ', ' + northStr + ', ' + str(bottomAltitude) + '\n')
				
			
			#Writes coordinate information to kml file.
			if spacingCount == 1:
				kmlFile.write(westStr + ',' + northStr + ',' + str(bottomAltitude))
				spacingCount+=1
				
			else:
				kmlFile.write(' ' + westStr + ',' + northStr + ',' + str(bottomAltitude))
				
		lowerFaceEnd1 = '</coordinates>\n'
		lowerFaceEnd2 = '\t\t\t\t\t</LinearRing>\n'
		lowerFaceEnd3 = '\t\t\t\t</outerBoundaryIs>\n'
		lowerFaceEnd4 = '\t\t\t</Polygon>\n'
		lowerFaceEnd5 = '\t\t</Placemark>\n'
		lowerFaceEnd6 = '\t</Document>\n'
		lowerFaceEnd7 = '</kml>\n'
		
		for x in range(1,6):
			exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')

		
		#---HORIZONTAL POLYGON 2---
		#This writes the second 2D polygon which is at the higher altitude.
		#Defines all the heading information of the KML file.
		kmlFileStart1 = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
		kmlFileStart2 = '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n'
		lowerFaceStart1 = '\t<Document>\n'
		lowerFaceStart2 = '\t\t<name>Layer 1</name>\n'
		lowerFaceStart3 = '\t\t<Placemark>\n'
		lowerFaceStart4 = '\t\t\t<name></name>\n'
		lowerFaceStart5 = '\t\t\t<description></description>\n'
		lowerFaceStart6 = '\t\t\t<Style>\n'
		lowerFaceStart7 = '\t\t\t\t<LineStyle>\n'
		lowerFaceStart8 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
		lowerFaceStart9 = '\t\t\t\t\t<width>6</width>\n'
		lowerFaceStart10 = '\t\t\t\t</LineStyle>\n'
		lowerFaceStart11 = '\t\t\t\t<PolyStyle>\n'
		lowerFaceStart12 = '\t\t\t\t\t<color>6B3644DB</color>\n'
		lowerFaceStart13 = '\t\t\t\t\t<fill>1</fill>\n'
		lowerFaceStart14 = '\t\t\t\t\t<outline>1</outline>\n'
		lowerFaceStart15 = '\t\t\t\t</PolyStyle>\n'
		lowerFaceStart16 = '\t\t\t\t<BalloonStyle>\n'
		lowerFaceStart17 = '\t\t\t\t\t<text></text>\n'
		lowerFaceStart18 = '\t\t\t\t</BalloonStyle>\n'
		lowerFaceStart19 = '\t\t\t</Style>\n'
		lowerFaceStart20 = '\t\t\t<Polygon>\n'
		lowerFaceStart21 = '\t\t\t\t<outerBoundaryIs>\n'
		lowerFaceStart22 = '\t\t\t\t\t<LinearRing>\n'
		lowerFaceStart23 = '\t\t\t\t\t\t<tessellate>1</tessellate>\n'
		lowerFaceStart24 = '\t\t\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
		lowerFaceStart25 = '\t\t\t\t\t\t\t<coordinates>'
		
		#Writes all the heading information of the KML file.
		#kmlFile.write(kmlFileStart1)
		#kmlFile.write(kmlFileStart2)
		for x in range(3,26):
			exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
		
		
		spacingCount = 1
		for x in dataList:
			
			y = x.replace(' - ','')
			
			#Calculates the longitudinal data.
			northDeg = int(y[0:2])
			northMin = int(y[2:4])/60
			northSec = int(y[4:6])/3600
			northDec = round(northDeg + northMin + northSec,5)
			northStr = str(northDec)
			
			#Calculates the latitudinal data.
			westDeg = int(y[8:11])
			westMin = int(y[11:13])/60
			westSec = int(y[13:15])/3600
			westDec = round(westDeg + westMin + westSec,5)
			westStr = '-' + str(westDec)
				
			#Writes coordinate information to kml file.
			#if spacingCount == 1:
			#	kmlFile.write('\t' + westStr + ', ' + northStr + ', ' + str(topAltitude) + '\n')
			#	spacingCount+=1
			#	
			#else:
			#	kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + westStr + ', ' + northStr + ', ' + str(topAltitude) + '\n')
			
			#Writes coordinate information to kml file.
			if spacingCount == 1:
				kmlFile.write(westStr + ',' + northStr + ',' + str(topAltitude))
				spacingCount+=1
				
			else:
				kmlFile.write(' ' + westStr + ',' + northStr + ',' + str(topAltitude))
			
			
		lowerFaceEnd1 = '</coordinates>\n'
		lowerFaceEnd2 = '\t\t\t\t\t</LinearRing>\n'
		lowerFaceEnd3 = '\t\t\t\t</outerBoundaryIs>\n'
		lowerFaceEnd4 = '\t\t\t</Polygon>\n'
		lowerFaceEnd5 = '\t\t</Placemark>\n'
		lowerFaceEnd6 = '\t</Document>\n'
		lowerFaceEnd7 = '</kml>\n'
		
		for x in range(1,6):
			exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')
		
		
		
		#---VERTICAL FACES---
		#This loop writes all of the vertical faces which make the shape look like a sealed box.
		#Create a list of decimal degree points.
		decimalDegreePoints = []
		for x in dataList:
			y = x.replace(' - ','')
			#Calculates the longitudinal data.
			northDeg = int(y[0:2])
			northMin = int(y[2:4])/60
			northSec = int(y[4:6])/3600
			northDec = round(northDeg + northMin + northSec,5)
			northStr = str(northDec)
			#Calculates the latitudinal data.
			westDeg = int(y[8:11])
			westMin = int(y[11:13])/60
			westSec = int(y[13:15])/3600
			westDec = round(westDeg + westMin + westSec,5)
			westStr = '-' + str(westDec)
			decimalDegreePoints.append(westStr + ', ' + northStr)
		#print(decimalDegreePoints)
		vFaceCount = len(dataList) - 1
		
		#Defines all the heading information of the KML file.
		lowerFaceStart3 = '\t\t<Placemark>\n'
		lowerFaceStart4 = '\t\t\t<name></name>\n'
		lowerFaceStart5 = '\t\t\t<description></description>\n'
		lowerFaceStart6 = '\t\t\t<Style>\n'
		lowerFaceStart7 = '\t\t\t\t<LineStyle>\n'
		lowerFaceStart8 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
		lowerFaceStart9 = '\t\t\t\t\t<width>6</width>\n'
		lowerFaceStart10 = '\t\t\t\t</LineStyle>\n'
		lowerFaceStart11 = '\t\t\t\t<PolyStyle>\n'
		lowerFaceStart12 = '\t\t\t\t\t<color>6B3644DB</color>\n'
		lowerFaceStart13 = '\t\t\t\t\t<fill>1</fill>\n'
		lowerFaceStart14 = '\t\t\t\t\t<outline>1</outline>\n'
		lowerFaceStart15 = '\t\t\t\t</PolyStyle>\n'
		lowerFaceStart16 = '\t\t\t\t<BalloonStyle>\n'
		lowerFaceStart17 = '\t\t\t\t\t<text></text>\n'
		lowerFaceStart18 = '\t\t\t\t</BalloonStyle>\n'
		lowerFaceStart19 = '\t\t\t</Style>\n'
		lowerFaceStart20 = '\t\t\t<Polygon>\n'
		lowerFaceStart21 = '\t\t\t\t<outerBoundaryIs>\n'
		lowerFaceStart22 = '\t\t\t\t\t<LinearRing>\n'
		lowerFaceStart23 = '\t\t\t\t\t\t<tessellate>1</tessellate>\n'
		lowerFaceStart24 = '\t\t\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
		lowerFaceStart25 = '\t\t\t\t\t\t\t<coordinates>'
		
		
		
		#This loop writes the vertical faces to file.
		for n in range(0,vFaceCount):
		
			for x in range(3,26):
				exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
			
			kmlFile.write('\t' + decimalDegreePoints[n] + ', ' + str(bottomAltitude) + '\n')
			kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + decimalDegreePoints[n+1] + ', ' + str(bottomAltitude) + '\n')
			kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + decimalDegreePoints[n+1] + ', ' + str(topAltitude) + '\n')
			kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + decimalDegreePoints[n] + ', ' + str(topAltitude) + '\n')
			kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + decimalDegreePoints[n] + ', ' + str(bottomAltitude) + '\n')
			
			lowerFaceEnd1 = '\t\t\t\t\t\t\t</coordinates>\n'
			lowerFaceEnd2 = '\t\t\t\t\t</LinearRing>\n'
			lowerFaceEnd3 = '\t\t\t\t</outerBoundaryIs>\n'
			lowerFaceEnd4 = '\t\t\t</Polygon>\n'
			lowerFaceEnd5 = '\t\t</Placemark>\n'
			
			for x in range(1,6):
				exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')

		lowerFaceEnd6 = '\t</Document>\n'
		lowerFaceEnd7 = '</kml>\n'
		kmlFile.write(lowerFaceEnd6)
		kmlFile.write(lowerFaceEnd7)
	
	#========================================================================================================================================================================

	#========================================================================================================================================================================
	
	if shape == '3D2':
		
		#I made this alternate 3D version for the EG_D202_WW zone. Since it was difficult to create the 2D area, the easiest way to make it 3D was to start from the decimal
		#degrees. So I made a modified version of the 3D option which reads in a list of decimal degree coordinates instead of calculating them on the fly. The format for the
		#decimal degrees need to be the two values with a comma (no spaces) separating them.
		
		#====================================================================================================================================================================
		#This part is the main difference, the coordinates are already converted so they are read in instead of converted on the fly.
		#Read in a list of pre-converted decimal degree coordinates.
		#decimalCoordFileName = input('Please enter the name of the file containing the pre-converted decimal coordinates:\n')
		decimalCoordFileName = fileName[:]
		decimalCoordFile = open(decimalCoordFileName,'r')
		decimalCoords = decimalCoordFile.read()
		decimalCoords = decimalCoords.split('\n')
		decimalCoordFile.close()
		
		
		northCoords = []
		westCoords = []
		for x in decimalCoords:
			
			if x != '':
				currentCoords = x.split(', ')
				northCoords.append(currentCoords[1])
				westCoords.append(currentCoords[0])
			
		dataList = northCoords[:]
		#====================================================================================================================================================================
		#====================================================================================================================================================================
		#3D2 Configuration
		
		#I have made the script request the altitudes so that the program doesn't have to be modified each time I run it.
		topAltitude = input('\nPlease enter the top altitude (meters):\n')
		bottomAltitude = input('\nPlease enter the bottom altitude (meters):\n')
		#topAltitude = 12500
		#bottomAltitude = 0
		
		shapeName = fileName.replace('.txt','')
		shapeDesc = ''
		
		
		
		#Creates an empty KML file from the coordinate information.
		kmlName = fileName.replace('.txt','_3DPolygon.kml')
		kmlFile = open(kmlName,'w')
		#====================================================================================================================================================================
		#====================================================================================================================================================================
		#---HORIZONTAL POLYGON 1---
		#Defines all the heading information of the KML file.
		kmlFileStart1 = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
		kmlFileStart2 = '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n'
		lowerFaceStart1 = '\t<Document>\n'
		lowerFaceStart2 = '\t\t<name>Layer 1</name>\n'
		lowerFaceStart3 = '\t\t<Placemark>\n'
		lowerFaceStart4 = '\t\t\t<name>' + shapeName + '</name>\n'
		lowerFaceStart5 = '\t\t\t<description>' + shapeDesc + '</description>\n'
		lowerFaceStart6 = '\t\t\t<Style>\n'
		lowerFaceStart7 = '\t\t\t\t<LineStyle>\n'
		lowerFaceStart8 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
		lowerFaceStart9 = '\t\t\t\t\t<width>6</width>\n'
		lowerFaceStart10 = '\t\t\t\t</LineStyle>\n'
		lowerFaceStart11 = '\t\t\t\t<PolyStyle>\n'
		lowerFaceStart12 = '\t\t\t\t\t<color>6B3644DB</color>\n'
		lowerFaceStart13 = '\t\t\t\t\t<fill>1</fill>\n'
		lowerFaceStart14 = '\t\t\t\t\t<outline>1</outline>\n'
		lowerFaceStart15 = '\t\t\t\t</PolyStyle>\n'
		lowerFaceStart16 = '\t\t\t\t<BalloonStyle>\n'
		lowerFaceStart17 = '\t\t\t\t\t<text></text>\n'
		lowerFaceStart18 = '\t\t\t\t</BalloonStyle>\n'
		lowerFaceStart19 = '\t\t\t</Style>\n'
		lowerFaceStart20 = '\t\t\t<Polygon>\n'
		lowerFaceStart21 = '\t\t\t\t<outerBoundaryIs>\n'
		lowerFaceStart22 = '\t\t\t\t\t<LinearRing>\n'
		lowerFaceStart23 = '\t\t\t\t\t\t<tessellate>1</tessellate>\n'
		lowerFaceStart24 = '\t\t\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
		lowerFaceStart25 = '\t\t\t\t\t\t\t<coordinates>'
		
		#Writes all the heading information of the KML file.
		kmlFile.write(kmlFileStart1)
		kmlFile.write(kmlFileStart2)
		for x in range(1,26):
			exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
		
		#Spacing count is only used to make sure the white space padding the front of the coordinates is consistent.
		spacingCount = 1		
		#Writes coordinate information to kml file.
		#for nc,wc in zip(northCoords,westCoords):
		#	if spacingCount == 1:
		#		kmlFile.write('\t' + wc + ', ' + nc + ', ' + str(bottomAltitude) + '\n')
		#		spacingCount+=1
		#		
		#	else:
		#		kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + wc + ', ' + nc + ', ' + str(bottomAltitude) + '\n')
				
		#Writes coordinate information to kml file.
		for nc,wc in zip(northCoords,westCoords):
			if spacingCount == 1:
				kmlFile.write(wc + ',' + nc + ',' + str(bottomAltitude))
				spacingCount+=1
				
			else:
				kmlFile.write(' ' + wc + ',' + nc + ',' + str(bottomAltitude))
		
		
		lowerFaceEnd1 = '</coordinates>\n'
		lowerFaceEnd2 = '\t\t\t\t\t</LinearRing>\n'
		lowerFaceEnd3 = '\t\t\t\t</outerBoundaryIs>\n'
		lowerFaceEnd4 = '\t\t\t</Polygon>\n'
		lowerFaceEnd5 = '\t\t</Placemark>\n'
		lowerFaceEnd6 = '\t</Document>\n'
		lowerFaceEnd7 = '</kml>\n'
		
		for x in range(1,6):
			exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')
		#====================================================================================================================================================================
		#---HORIZONTAL POLYGON 2---
		#This writes the second 2D polygon which is at the higher altitude.
		#Defines all the heading information of the KML file.
		kmlFileStart1 = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
		kmlFileStart2 = '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n'
		lowerFaceStart1 = '\t<Document>\n'
		lowerFaceStart2 = '\t\t<name>Layer 1</name>\n'
		lowerFaceStart3 = '\t\t<Placemark>\n'
		lowerFaceStart4 = '\t\t\t<name></name>\n'
		lowerFaceStart5 = '\t\t\t<description></description>\n'
		lowerFaceStart6 = '\t\t\t<Style>\n'
		lowerFaceStart7 = '\t\t\t\t<LineStyle>\n'
		lowerFaceStart8 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
		lowerFaceStart9 = '\t\t\t\t\t<width>6</width>\n'
		lowerFaceStart10 = '\t\t\t\t</LineStyle>\n'
		lowerFaceStart11 = '\t\t\t\t<PolyStyle>\n'
		lowerFaceStart12 = '\t\t\t\t\t<color>6B3644DB</color>\n'
		lowerFaceStart13 = '\t\t\t\t\t<fill>1</fill>\n'
		lowerFaceStart14 = '\t\t\t\t\t<outline>1</outline>\n'
		lowerFaceStart15 = '\t\t\t\t</PolyStyle>\n'
		lowerFaceStart16 = '\t\t\t\t<BalloonStyle>\n'
		lowerFaceStart17 = '\t\t\t\t\t<text></text>\n'
		lowerFaceStart18 = '\t\t\t\t</BalloonStyle>\n'
		lowerFaceStart19 = '\t\t\t</Style>\n'
		lowerFaceStart20 = '\t\t\t<Polygon>\n'
		lowerFaceStart21 = '\t\t\t\t<outerBoundaryIs>\n'
		lowerFaceStart22 = '\t\t\t\t\t<LinearRing>\n'
		lowerFaceStart23 = '\t\t\t\t\t\t<tessellate>1</tessellate>\n'
		lowerFaceStart24 = '\t\t\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
		lowerFaceStart25 = '\t\t\t\t\t\t\t<coordinates>'
		
		#Writes all the heading information of the KML file.
		#kmlFile.write(kmlFileStart1)
		#kmlFile.write(kmlFileStart2)
		for x in range(3,26):
			exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
		
		#Spacing count is only used to make sure the white space padding the front of the coordinates is consistent.
		spacingCount = 1		
		#Writes coordinate information to kml file.
		for nc,wc in zip(northCoords,westCoords):
			if spacingCount == 1:
				kmlFile.write(wc + ',' + nc + ',' + str(topAltitude))
				spacingCount+=1
				
			else:
				kmlFile.write(' ' + wc + ',' + nc + ',' + str(topAltitude))
		
		
		lowerFaceEnd1 = '</coordinates>\n'
		lowerFaceEnd2 = '\t\t\t\t\t</LinearRing>\n'
		lowerFaceEnd3 = '\t\t\t\t</outerBoundaryIs>\n'
		lowerFaceEnd4 = '\t\t\t</Polygon>\n'
		lowerFaceEnd5 = '\t\t</Placemark>\n'
		lowerFaceEnd6 = '\t</Document>\n'
		lowerFaceEnd7 = '</kml>\n'
		
		for x in range(1,6):
			exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')
		#====================================================================================================================================================================
		#====================================================================================================================================================================
		vFaceCount = len(dataList) - 1
		decimalDegreePoints = decimalCoords[:]
		
		#This loop creates the vertical faces.
		for n in range(0,vFaceCount):
			
			kmlFileStart1 = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
			kmlFileStart2 = '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n'
			lowerFaceStart1 = '\t<Document>\n'
			lowerFaceStart2 = '\t\t<name>Layer 1</name>\n'
			lowerFaceStart3 = '\t\t<Placemark>\n'
			lowerFaceStart4 = '\t\t\t<name></name>\n'
			lowerFaceStart5 = '\t\t\t<description></description>\n'
			lowerFaceStart6 = '\t\t\t<Style>\n'
			lowerFaceStart7 = '\t\t\t\t<LineStyle>\n'
			lowerFaceStart8 = '\t\t\t\t\t<color>' + LineColour + '</color>\n'
			lowerFaceStart9 = '\t\t\t\t\t<width>6</width>\n'
			lowerFaceStart10 = '\t\t\t\t</LineStyle>\n'
			lowerFaceStart11 = '\t\t\t\t<PolyStyle>\n'
			lowerFaceStart12 = '\t\t\t\t\t<color>6B3644DB</color>\n'
			lowerFaceStart13 = '\t\t\t\t\t<fill>1</fill>\n'
			lowerFaceStart14 = '\t\t\t\t\t<outline>1</outline>\n'
			lowerFaceStart15 = '\t\t\t\t</PolyStyle>\n'
			lowerFaceStart16 = '\t\t\t\t<BalloonStyle>\n'
			lowerFaceStart17 = '\t\t\t\t\t<text></text>\n'
			lowerFaceStart18 = '\t\t\t\t</BalloonStyle>\n'
			lowerFaceStart19 = '\t\t\t</Style>\n'
			lowerFaceStart20 = '\t\t\t<Polygon>\n'
			lowerFaceStart21 = '\t\t\t\t<outerBoundaryIs>\n'
			lowerFaceStart22 = '\t\t\t\t\t<LinearRing>\n'
			lowerFaceStart23 = '\t\t\t\t\t\t<tessellate>1</tessellate>\n'
			lowerFaceStart24 = '\t\t\t\t\t\t<altitudeMode>' + altitudeMode + '</altitudeMode>\n'
			lowerFaceStart25 = '\t\t\t\t\t\t\t<coordinates>'
			
			#Writes all the heading information of the KML file.
			#kmlFile.write(kmlFileStart1)
			#kmlFile.write(kmlFileStart2)
			for x in range(3,26):
				exec('kmlFile.write(lowerFaceStart' + str(x) + ')')
		
			
			#kmlFile.write('\t' + (decimalDegreePoints[n].split(',')[0]) + ', ' (decimalDegreePoints[n].split(',')[1]) + ', ' + str(bottomAltitude) + '\n')
			#kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + (decimalDegreePoints[n+1].split(',')[0]) + ', ' (decimalDegreePoints[n+1].split(',')[1]) + ', ' + str(bottomAltitude) + '\n')
			#kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + (decimalDegreePoints[n+1].split(',')[0]) + ', ' (decimalDegreePoints[n+1].split(',')[1]) + ', ' + str(topAltitude) + '\n')
			#kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + (decimalDegreePoints[n].split(',')[0]) + ', ' (decimalDegreePoints[n].split(',')[1]) + ', ' + str(topAltitude) + '\n')
			#kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + (decimalDegreePoints[n].split(',')[0]) + ', ' (decimalDegreePoints[n].split(',')[1]) + ', ' + str(bottomAltitude) + '\n')
			
			kmlFile.write('\t' + decimalDegreePoints[n] + ', ' + str(bottomAltitude) + '\n')
			kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + decimalDegreePoints[n+1] + ', ' + str(bottomAltitude) + '\n')
			kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + decimalDegreePoints[n+1] + ', ' + str(topAltitude) + '\n')
			kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + decimalDegreePoints[n] + ', ' + str(topAltitude) + '\n')
			kmlFile.write('\t\t\t\t\t\t\t\t\t\t\t' + decimalDegreePoints[n] + ', ' + str(bottomAltitude) + '\n')
			
			
			
			#print(decimalDegreePoints[n].split(',')[0])
			
			lowerFaceEnd1 = '\t\t\t\t\t\t\t</coordinates>\n'
			lowerFaceEnd2 = '\t\t\t\t\t</LinearRing>\n'
			lowerFaceEnd3 = '\t\t\t\t</outerBoundaryIs>\n'
			lowerFaceEnd4 = '\t\t\t</Polygon>\n'
			lowerFaceEnd5 = '\t\t</Placemark>\n'
			lowerFaceEnd6 = '\t</Document>\n'
			lowerFaceEnd7 = '</kml>\n'
			
			for x in range(1,6):
				exec('kmlFile.write(lowerFaceEnd' + str(x) + ')')
		#====================================================================================================================================================================
		kmlFileEnd1 = '\t</Document>\n'
		kmlFileEnd2 = '</kml>'
		kmlFile.write(kmlFileEnd1)
		kmlFile.write(kmlFileEnd2)
		
	#file.close()
	kmlFile.close()
	print('Done')



def formatCoordOutput(lat,lng,alt):
	#0 = Lng, 1 = Lat, 2 = Alt
	outputString = '{0},{1},{2}\n'.format(lng,lat,alt)
	return(outputString)
	
	
def coord_conv1(fileName,mode):
	
	"""Convert coordinates in degrees, minutes, seconds to decimal degrees.
	
	This script takes a specific format of degree, minute second date. The format is shown below:
	
	Description|Latitude Degs|Latitude Mins|Latitude Secs|Longitude Degs|Longitude Mins|Longitude Secs|Extra Information
	
	If the data is already decimal then mode 1 should be used. If not mode 0 should be used.
	
	"""
	
	#Opens the text file containing the coordinates in degree, minute, second format.
	file = open(fileName,'r')
	data = file.read()
	file.close()
	
	dataList = data.split('\n')
	
	#Opens a new file to contain the coordinates in decimal degrees.
	newFileName = fileName.replace('.csv','_decimal.csv')
	newFile = open(newFileName,'w')
	
	del dataList[0]
	del dataList[-1]
	
	for x in dataList:
		
		y = x.split(',')
		
		y1 = y[1:7]
		
		if mode == 0:
			northDeg = int(y1[0])
			northMin = int(y1[1])/60
			northSec = int(y1[2])/3600
			northDec = round(northDeg + northMin + northSec,5)
			northStr = str(northDec)
			
			westDeg = int(y1[3])
			westMin = int(y1[4])/60
			westSec = int(y1[5])/3600
			westDec = round(westDeg + westMin + westSec,5)
			westStr = '-' + str(westDec)
			
			final = y[0] + ', ' + northStr + ', ' + westStr + ', ' + y[7]
			print(final)
			newFile.write(final + '\n')
			
		if mode == 1:
			northDeg = float(y1[0])
			northMin = float(y1[1])/60
			northSec = float(y1[2])/3600
			northDec = round(northDeg + northMin + northSec,5)
			northStr = str(northDec)
			
			westDeg = float(y1[3])
			westMin = float(y1[4])/60
			westSec = float(y1[5])/3600
			westDec = round(westDeg + westMin + westSec,5)
			westStr = '-' + str(westDec)
			
			final = y[0] + ', ' + northStr + ', ' + westStr + ', ' + y[7]
			print(final)
			newFile.write(final + '\n')
		
	
	newFile.close()
	print(len(dataList))