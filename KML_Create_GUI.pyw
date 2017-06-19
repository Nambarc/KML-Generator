import tkinter as tk
from tkinter import ttk, filedialog
import mapping1

#Started adding functionality to display requirement text as well.
#Realised I would need to completely change the way requirements are loaded
#so that more fields than just the requirement ID are loaded.

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.pack()
		self.create_widgets()

	def create_widgets(self):

		#Geometry of entire window.
		self.windowWidth = '500'
		self.windowHeight = '580'
		self.windowXOffset = '30'
		self.windowYOffset = '30'
		self.windowGeometry = '{0}x{1}+{2}+{3}'.format(self.windowWidth,self.windowHeight,self.windowXOffset,self.windowYOffset)

		#self.master.geometry(self.windowGeometry)

		# Define UI elements.
		textLineWidth = 43

		#Define master frame to contain all other UI elements.
		self.masterFrame = tk.Frame(self)
		self.masterFrame.pack(side='top')


		#Label for input file select textbox.
		self.inputFileL = tk.Label(self.masterFrame, text='Please select input file:', anchor='w')
		self.inputFileL.pack(side='top', fill='x', padx=5)
		#Sub Frame 1
		self.subFrame1 = tk.Frame(self.masterFrame)
		self.subFrame1.pack(side='top', fill='x')
		#Entry box to specify input file path.
		self.inputFileE = tk.Entry(self.subFrame1, width=textLineWidth)
		self.inputFileE.pack(side='left', padx=5)
		#Button to select input file.
		self.inputFileSelectB = tk.Button(self.subFrame1, text='Select', command=self.selectInputFile)
		self.inputFileSelectB.pack(side='left', padx=5)


		#Label for output file select textbox.
		self.outputFileL = tk.Label(self.masterFrame, text='Please select output file:', anchor='w')
		self.outputFileL.pack(side='top', fill='x', padx=5)
		#Sub Frame 2
		self.subFrame2 = tk.Frame(self.masterFrame)
		self.subFrame2.pack(side='top', fill='x')
		#Entry box to specify output file path.
		self.outputFileE = tk.Entry(self.subFrame2, width=textLineWidth)
		self.outputFileE.pack(side='left', padx=5)
		#Button to select output file.
		self.outputFileSelectB = tk.Button(self.subFrame2, text='Select', command=self.selectOutputFile)
		self.outputFileSelectB.pack(side='left', padx=5)


		#Label for KML type select combobox.
		self.kmlTypeL = tk.Label(self.masterFrame, text='Please select the type of KML to generate:', anchor='w')
		self.kmlTypeL.pack(side='top', fill='x', padx=5)
		#Sub Frame 3
		self.subFrame3 = tk.Frame(self.masterFrame)
		self.subFrame3.pack(side='top', fill='x')
		#Combobox to select KML type.
		self.kmlTypeCB = ttk.Combobox(self.subFrame3)
		self.kmlTypeCB['values'] = ('Marker','Polyline','2D Polygon','3D Polygon')
		self.kmlTypeCB.set('Marker')
		self.kmlTypeCB.pack(side='left',padx=10)
		#Button to generate KML.
		self.generateB = tk.Button(self.subFrame3, text='Generate', command=self.generateKML)
		self.generateB.pack(side='left')


		#Output text box.
		self.statusText = tk.Text(self.masterFrame, width=38, height=20)
		self.statusText.pack(side='top', pady=5)


	#==============================================================================================
	
	#DEFINE CLASS FUNCTIONS

	#==============================================================================================
	
	def selectInputFile(self):
		#Open file dialog to select input file.
		inputFileName = filedialog.askopenfilename(initialdir='B:/Users/Chris/Desktop/KML Generator/')
		
		#Clear input file text.
		self.inputFileE.delete(0, 'end')

		#Put input file name into text edit.
		self.inputFileE.insert(0, inputFileName)

	def selectOutputFile(self):
		#Open file dialog to select output file name.
		outputFileName = filedialog.asksaveasfilename(initialdir='B:/Users/Chris/Desktop/KML Generator/',defaultextension='kml', initialfile='output')

		#Clear output file text.
		self.outputFileE.delete(0, 'end')

		#Put output file name into text edit.
		self.outputFileE.insert(0, outputFileName)

	def generateKML(self):

		#Get input filename.
		inputFileName = self.inputFileE.get()

		#Load input file contents.
		with open(inputFileName, 'r') as inputFile:
			inputData = inputFile.read()

		#Get KML type.
		kmlType = self.kmlTypeCB.get()

		#Get properly formatted list of coordinates.
		coordList = self.prepareCoords(inputData)

		#Create KML data.
		kmlString = mapping1.kml_create(kmlType, coordList)

		#Get output file name.
		outputFileName = self.outputFileE.get()

		#Write KML string to file.
		self.writeStringToFile(kmlString,outputFileName)

		

		
	def prepareCoords(self, coordsString):
		'''Function to prepare input coordinate so that they are ready for the KML generation function.

		Input = coordinates as read from file.
		Output = list of coordinate pairs in dictionary.
		'''

		#Define output list.
		outputList = []

		#Split coords by new line
		coordStringSplitNewLine = coordsString.split('\n')

		#Pull coordinate from each line and put into dictionary pair.
		for line in coordStringSplitNewLine:

			#Make sure line isn't empty
			if line != '':

				#Split pair based on comma.
				coordinatePair = line.split(',')

				#Get values for lat and lon.
				lat = coordinatePair[0]
				lon = coordinatePair[1]

				#Create coordinate pair dictionary.
				coordinatePairDict = {'lat':lat, 'lon':lon}

				#Add coordinate pair dictionary to output list.
				outputList.append(coordinatePairDict)

		return(outputList)

	def writeStringToFile(self, outputString, outputFileName):
		with open(outputFileName,'w') as outputFile:
			outputFile.write(outputString)








#==============================================================================================
#Start Application

root = tk.Tk()
root.title('KML Create')
app = Application(master=root)
app.mainloop()