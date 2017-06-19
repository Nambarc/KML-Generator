

def kml_create(kmlType, coordList):

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

	-------------------------------------------------------------------------------------
	
	inputs =	Type of KML
				List of Lat and Long coordinates in the format {'lat':LAT,'lon':LON}

	"""

	#Verify that the input KML type is valid.
	validKMLTypes = ['Polyline']
	if not(kmlType in validKMLTypes):
		return('Invalid KML type chosen')



	#Set other KML settings.
	shapeName = 'My KML'
	LineColour = '501400FF'
	LineWidth = 5
	altitudeMode = 'relativeToGround'
	simpleAltitude = 0

	#Output string to be written to file.
	outputString = ''

	#========================================================================================================================================================================
	#KML Polyline
	if kmlType == 'Polyline':
	
		#Defines all the heading information of the KML file.
		kmlComponentsTop = [
						'<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n',
						'<kml xmlns=\'http://www.opengis.net/kml/2.2\'>\n',
						'  <Document>\n',
						'    <name>Layer 1</name>\n',
						'    <Placemark>\n',
						'      <name>{0}</name>\n'.format(shapeName),
						'      <description>Insert description here.</description>\n',
						'      <Style>\n',
						'        <LineStyle>\n',
						'          <color>{0}</color>\n'.format(LineColour),
						'          <width>{0}</width>\n'.format(str(LineWidth)),
						'        </LineStyle>\n',
						'        <PolyStyle>\n',
						'          <color>{0}</color>\n'.format(LineColour),
						'          <fill>1</fill>\n',
						'          <outline>1</outline>\n',
						'        </PolyStyle>\n',
						'        <BalloonStyle>\n',
						'          <text>Insert text here.</text>\n',
						'        </BalloonStyle>\n',
						'      </Style>\n',
						'      <LineString>\n',
						'        <extrude>1</extrude>\n',
						'        <tessellate>1</tessellate>\n',
						'        <altitudeMode>' + altitudeMode + '</altitudeMode>\n',
						'        <coordinates>'
		]
		
		#Writes initial KML data to file (up to coordinates point)
		for line in kmlComponentsTop:
			outputString += line
		
		spacingCount = 1
		#Add coordinates to output string
		for coordPair in coordList:

			#Writes coordinate information to kml file.

			#If spacing count is 1, this is the first coordinate and doesn't need as much indenting.
			if spacingCount == 1:
				outputString += '{0},{1},{2}\n'.format(coordPair['lon'], coordPair['lat'], str(simpleAltitude))
				spacingCount+=1
			else:
				outputString += '                     {0},{1},{2}\n'.format(coordPair['lon'], coordPair['lat'], str(simpleAltitude))

		#Write final section of KML.
		kmlComponentsTop = [
						'        </coordinates>\n',
						'      </LineString>\n',
						'    </Placemark>\n',
						'  </Document>\n',
						'</kml>',
		]
		
		for line in kmlComponentsTop:
			outputString += line
		#========================================================================================================================================================================
	'''
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
	
	'''

	return(outputString)