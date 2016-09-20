#!/usr/bin/python

import sys, time, os, datetime

############## CLASSes ###############
class PropFile:

    def __init__(self, fileName):
        self.propFile = 0
        self.propsDict = dict()
        self.fileName = ''
        self.fileName = fileName
        try:
            self.propFile=open('./' + fileName)
            print ('### File ' + fileName + ' is opened')
            self.readProperties()
        except:
            print ('!!!!! cannot open the file ' + fileName)
            exit()    
    
    def readProperties(self):
        count=0
        propCount=0
        for line in self.propFile:
            count = count + 1
            if (( line[0] != '#') and ( line.find('=') > 0 )):
                self.propsDict[line.strip().split('=')[0]] = (line.strip().split('=')[1])
                propCount = propCount + 1
        #print ("line count", count)
        print ('### Found ' + str(propCount) + ' properties from file ' + self.fileName + ' of total ' + str(count) + ' lines.')

        #for property in self.propsDict:
        #    print (property + ' = ' + self.propsDict[property])

    def closeFile(self):
        try:
            self.propFile.close()
            print ('### File ' + self.fileName + ' is closed.')
        except:
            print ('!!!!! Cannot close file ' + self.fileName + '.')

################ Comparer ################

def Comparer(propFile1, propFile2):

    print ('### Comparing propFile1: ' + propFile1.fileName + 'and propFile2: ' + propFile2.fileName)

    uniqPropsFile1 = {}
    uniqPropsFile2 = {}
    overlapProp = {}

    try: input ('!!!!! Press enter to continue')
    except SyntaxError: pass

    global diffTxtfileName
    fileOutput = open(diffTxtfileName,"a")
    
    fileOutput.write ('\n\n##### Comparison results for properties files - ' + propFile1.fileName + ', ' + propFile2.fileName + ':\n\n')

    fileOutput.write ('##### Non-equal Properties:' + '\n\n')
    

    for keyProp in propFile1.propsDict:
        #print ('-----------------------------------')
        if keyProp in propFile2.propsDict:
            #print ('----- the Property - ' + keyProp + ' - exists in both files' )
            if propFile1.propsDict[keyProp] == propFile2.propsDict[keyProp]:
                #print ('----- the Property - ' + keyProp + ' - is equal for both files' )
                overlapProp[keyProp] = propFile1.propsDict[keyProp]
            else: 
                #print ('----- the Property - ' + keyProp + ' - is NOT equal for both files' )
                fileOutput.write ('----- the Property - ' + keyProp + ' - is NOT equal for both files:\n')
                fileOutput.write (' file ' + propFile1.fileName + ': ' + keyProp + '=' + propFile1.propsDict[keyProp] + '\n')
                fileOutput.write (' file ' + propFile2.fileName + ': ' + keyProp + '=' + propFile2.propsDict[keyProp] + '\n\n')
        else: 
            #print ( '----- the Property - ' + keyProp + ' - is unique for the file ' + propFile1.fileName )
            uniqPropsFile1[keyProp] = propFile1.propsDict[keyProp]

    for keyProp in propFile2.propsDict:
        #print ('-----------------------------------')
        if keyProp not in propFile1.propsDict:
            #print ( '----- the Property - ' + keyProp + ' - is unique for the file ' + propFile2.fileName )
            uniqPropsFile2[keyProp] = propFile2.propsDict[keyProp]

    fileOutput.close()

    DictToTxt(txtfileName = diffTxtfileName, dictToTxt = overlapProp, description = 'Equal Properties for the both properties files - ' + propFile1.fileName + ', ' + propFile2.fileName + ':')
    DictToTxt(txtfileName = diffTxtfileName, dictToTxt = uniqPropsFile1, description = 'Unique Properties for the properties file - ' + propFile1.fileName + ':')
    DictToTxt(txtfileName = diffTxtfileName, dictToTxt = uniqPropsFile2, description = 'Unique Properties for the properties file - ' + propFile2.fileName + ':')

    #DictToTxt(txtfileName = diffCSVfileName, dictToTxt = propFile2.propsDict, description = 'Properties of the file ' + propFile2.fileName)

    #print ('### propFile1 is: ' + propFile2.fileName)

################ DictToTxt ################

def DictToTxt(txtfileName, dictToTxt, description):
    fileOutput = open(txtfileName,"a")
    fileOutput.write ('\n\n##### ' + description + '\n')
    for key in dictToTxt:
        fileOutput.write (key + '=' + "'" + dictToTxt[key] + "'" +'\n')
    fileOutput.write ('\n\n\n\n\n')
    fileOutput.close()
    

################ Usage ################    

def Usage():
    print ('!!!!! The usage is wrong. Or cannot open properties files.\nUsage example:\npython propsComparer.py optserver.properties1 optserver.properties2')
    exit()

################ MAIN ##################

if __name__ == '__main__':

    #print ('Number of arguments:', len(sys.argv), 'arguments.')

    #print ('Argument List:', str(sys.argv))
    #for arg in sys.argv:
    #	print (arg)

    try:
        propFile1 = PropFile(sys.argv[1])
        propFile2 = PropFile(sys.argv[2])
    except:
        Usage()
    
    #propFile1.readProperties()
    #propFile2.readProperties()

    

    diffTxtfileName = 'PropertiesDiff_' + str(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")) + ".txt"
    print ('### The Properties difference file is ' + diffTxtfileName)

    Comparer (propFile1, propFile2)

    #DictToCSV(CSVfileName = diffCSVfileName, dictToCSV = propFile1.propsDict, description = 'Properties of the file ' + propFile1.fileName)
    #DictToCSV(CSVfileName = diffCSVfileName, dictToCSV = propFile2.propsDict, description = 'Properties of the file ' + propFile2.fileName)



    propFile1.closeFile()
    propFile2.closeFile()
