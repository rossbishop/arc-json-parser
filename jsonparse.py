from PIL import Image, ImageDraw
import json
import os
from collections import namedtuple

# Create data types (named tuples) to store grids and pairs of grid input/outputs
Grid = namedtuple('Grid', 'norows nocolumns pixeldata')
GridPair = namedtuple('GridPair', 'input output')

# Pixel colour/RGB data map
colourMap = {0:(0,0,0), 1:(0,116,217), 2:(255,65,54), 3:(46,204,64), 4:(255,220,0), 5:(170,170,170), 6:(240,18,190), 7:(255,133,27), 8:(127,219,255), 9:(135,12,37)} 

# Choose directory to scan
directory = "D:/ARC/ARC/data/training"

# Get directory name for folder
slashCount = directory.count('/')
directorySplit = directory.split("/")
directoryName = directorySplit[slashCount]

# Scan through all files
for filename in os.listdir(directory):
    # Do for all JSON files
    if filename.endswith(".json"): 
    
        # Get path
        fullpath = directory + "/" + filename
        inputFile = open(fullpath, "r")
        
        # Create output directory
        outputNameSplit = filename.split(".")
        outputName = outputNameSplit[0]        
        outputDir = "converted_" + directoryName + "/" + outputName
        os.mkdir(outputDir)
        
        # Create training and test directories
        os.mkdir(outputDir + "/training")
        os.mkdir(outputDir + "/test")
        
        # Dump JSON
        parsedInputFile = json.loads(inputFile.read())

        # Split JSON into training and test data
        trainingData = parsedInputFile['train']
        testData = parsedInputFile['test']

        # Create array (list) of correct size to store training input/output pairs
        trainingPairs = [0] * len(trainingData)

        # Initialize counter for training pairs
        trainCount = 0

        # Iterate over training data and create grid pairs
        for x in trainingData:
            
            # Extract grid data and store in nice variables
            tempNoRows = len(x["input"])
            tempNoCols = len(x["input"][0])
            tempPixelData = x["input"]
            
            # Create input grid
            tempInputGrid = Grid(tempNoRows, tempNoCols, tempPixelData)
            
            # Extract grid data and store in nice variables
            tempNoRows = len(x["output"])
            tempNoCols = len(x["output"][0])
            tempPixelData = x["output"]
            
            # Create output grid
            tempOutputGrid = Grid(tempNoRows, tempNoCols, tempPixelData)
            
            # Create grid pair
            tempPair = GridPair(tempInputGrid, tempOutputGrid)
            
            # Store training pair at current index
            trainingPairs[trainCount] = tempPair
            
            # Increment counter
            trainCount += 1

        # Create array (list) of correct size to store test input/output pairs
        testPairs = [0] * len(testData)

        # Initialize counter for testing pairs
        testCount = 0

        # Iterate over test data and create grid pairs

        for y in testData:

            # Extract grid data and store in nice variables
            tempNoRows = len(y["input"])
            tempNoCols = len(y["input"][0])
            tempPixelData = y["input"]

            # Create input grid
            tempInputGrid = Grid(tempNoRows, tempNoCols, tempPixelData)
            
            # Extract grid data and store in nice variables
            tempNoRows = len(y["output"])
            tempNoCols = len(y["output"][0])
            tempPixelData = y["output"]
            
            # Create output grid
            tempOutputGrid = Grid(tempNoRows, tempNoCols, tempPixelData)
            
            # Create grid pair
            tempPair = GridPair(tempInputGrid, tempOutputGrid)
            
            # Store training pair at current index
            testPairs[testCount] = tempPair
            
            # Increment counter
            testCount += 1   


        # For all training pairs
        for pair in range(len(trainingPairs)):
            
            # Get current training pair
            currentPair = trainingPairs[pair]
            
            # Grab and store input image info, create blank image
            imageX = currentPair.input.nocolumns
            imageY = currentPair.input.norows
            gridImage = Image.new('RGBA', (imageX, imageY), "black")
            numberPixels = imageX * imageY

            # Reset counter
            count = 0

            # Put pixel data into image
            for row in range(imageY):
                for col in range(imageX):
                    pixelClass = currentPair.input.pixeldata[row][col]
                    gridImage.putpixel((col, row), colourMap[pixelClass])

            # Save image to disk
            gridImage.save(outputDir + "/training/input" + str(pair) + ".png")

            # Grab and store input image info, create blank image
            imageX = currentPair.output.nocolumns
            imageY = currentPair.output.norows
            gridImage = Image.new('RGBA', (imageX, imageY), "black")
            numberPixels = imageX * imageY

            # Reset counter
            count = 0
            
            # Put pixel data into image
            for row in range(imageY):
                for col in range(imageX):
                    pixelClass = currentPair.output.pixeldata[row][col]
                    gridImage.putpixel((col, row), colourMap[pixelClass])
            
            # Save image to disk
            gridImage.save(outputDir + "/training/output" + str(pair) + ".png")
            
        for pair in range(len(testPairs)):
    
            # Get current test pair
            currentPair = testPairs[pair]

            # Grab and store input image info, create blank image
            imageX = currentPair.input.nocolumns
            imageY = currentPair.input.norows
            gridImage = Image.new('RGBA', (imageX, imageY), "black")
            numberPixels = imageX * imageY

            # Reset counter
            count = 0

            # Put pixel data into image
            for row in range(imageY):
                for col in range(imageX):
                    pixelClass = currentPair.input.pixeldata[row][col]
                    gridImage.putpixel((col, row), colourMap[pixelClass])

            # Save image to disk
            gridImage.save(outputDir + "/test/input" + str(pair) + ".png")

            # Grab and store input image info, create blank image
            imageX = currentPair.output.nocolumns
            imageY = currentPair.output.norows
            gridImage = Image.new('RGBA', (imageX, imageY), "black")
            numberPixels = imageX * imageY

            # Reset counter
            count = 0

            # Put pixel data into image
            for row in range(imageY):
                for col in range(imageX):
                    pixelClass = currentPair.output.pixeldata[row][col]
                    gridImage.putpixel((col, row), colourMap[pixelClass])
                    
            # Save image to disk
            gridImage.save(outputDir + "/test/output" + str(pair) + ".png")        
            