"""
Implements the xml splitter, split xml file to several small size files
"""

import os
from progressbar import *

class xmlSplitter:
    __oneSheetItems = 50000
    __lastFileItems = 0
    __fileNum = 0
    __fileFullName = ""
    __fileName = ""
    __tabFinished = False
    __splittedFinished = True
    __splittedKeyList = []
    __keyNum = 0
    __subSheetRowList = []
    __rowCount = 0
    __columnNum = 0
    __hashKey = ""
    __hasInvalidData = False
    __tempFileName = ""
    __tempGeneratedName = ""
    __ABAP_CR_LF = '\r\n'
    __itemCount = 0
    __mainSheetRowCount = 0
    __findKeyRow = False
    __fileLines = 0
    __newFileLines = 0

    def __init__(self,fullName:str,fileNum:int):
        """
        Constructor, initialize variables 
        :param fullName: xml file full name, includes the path
        :param fileNum: the count of splitted files
        """
        self.__fileFullName = fullName
        self.__fileNum = fileNum
        self.__fileName = self.__fileFullName.split('.')[0]
        self.__tempFileName = self.__fileName + "_bak" + '.xml' 
        self.__tempGeneratedName = self.__fileName + "_bak"  + "_tmp.xml" 
        if os.path.isfile(self.__tempFileName) == True: 
            raise NameError(self.__tempFileName + " already exists.")
        if os.path.isfile(self.__tempGeneratedName) == True: 
            raise NameError(self.__tempGeneratedName + " already exists.")
        self.__initialize()

    def __createXmlByKey(self,idx:str)->bool:
        """
        Create splitted xml file by keys
        :param idx: the index of splitted xml file
        :return: Splitting files finished or not
        """
        workSheet = 0
        splittedFileName = self.__fileName + idx + '.xml'
        self.__newFileLines = 0
        count = 0
        self.__keyNum = 0
        self.__splittedFinished = True
        self.__hasInvalidData = False
        self.__splittedKeyList = []

        if os.path.isfile(splittedFileName) == True:  
            raise NameError(splittedFileName + " already exists.")
        
        print("Generate file " + splittedFileName + ":" + idx + "/" + str(self.__fileNum))

        if int(idx) == self.__fileNum:
            self.__oneSheetItems = self.__lastFileItems

        originFile = ""
        if os.path.isfile(self.__tempFileName) == True:
            originFile = self.__tempFileName
        else:
            originFile = self.__fileFullName    

        bar = self.__getPercentageProgress(splittedFileName)

        with open(originFile, 'r',encoding='utf-8') as oldFile:
            with open(self.__tempGeneratedName, 'w+',encoding='utf-8') as newFile:
                with open(self.__fileName + idx + '.xml', 'w+',encoding='utf-8') as splittedFile:
                    for line in oldFile:
                        count += 1
                        try:
                            bar.update(int(count*100/self.__fileLines))
                        except Exception as err:
                            print("count:" + str(count))
                            print("fileLines:" + str(self.__fileLines))
                            raise Exception(" dump")
                        line = line.strip() + self.__ABAP_CR_LF 
                        if line.find('<Worksheet ss:Name') != -1:
                            self.__tabFinished = False
                            self.__rowCount = 0
                            self.__columnNum = 0           
                            workSheet = workSheet + 1            
                        if workSheet < 3:
                            self.__newFileLines += 1
                            newFile.write(line)
                            splittedFile.write(line)
                            continue
                        if workSheet == 3:
                            self.__parseMainSheet(line, newFile, splittedFile)
                        else:
                            self.__parseSubSheet(line, newFile, splittedFile)
                splittedFile.close()    
            newFile.close()                                                 
        oldFile.close()
        self.__fileLines = self.__newFileLines

        if os.path.isfile(self.__tempFileName) == True:     
            os.remove(self.__tempFileName)
        os.rename(self.__tempGeneratedName,self.__tempFileName)

        if self.__splittedFinished == True:
            if os.path.isfile(self.__tempFileName) == True:  
                if self.__hasInvalidData == False:
                    os.remove(self.__tempFileName)
                else:
                    os.rename(self.__tempFileName,self.__fileName + '_invalid_data' + '.xml')
        return self.__splittedFinished

    def __initialize(self):
        """
        Scan the original file and get the count of items and the lines of the file.
        """
        print("Prepare to start.")
        workSheet = 0
        rowCount = 0
        scanMainFinished = False
        if os.path.isfile(self.__fileFullName) !=  True:  
            raise NameError(self.__fileFullName + " does not exist")
        with open(self.__fileFullName, 'r',encoding='utf-8') as File:
            for line in File:
                self.__fileLines += 1
                if scanMainFinished is True:
                    continue
                if line.find('<Worksheet ss:Name') != -1:
                    workSheet = workSheet + 1 
                if workSheet < 3:
                    continue
                if workSheet == 3:
                    if line.find('<Row') != -1:
                        rowCount += 1
                    if line.find('</Table>') != -1:
                        scanMainFinished = True
                        continue
        File.close()  

        self.__itemCount = rowCount - 8
        if self.__itemCount < self.__fileNum:
            raise NameError("The number of splitted files is too big")
        if self.__itemCount % self.__fileNum == 0:
            self.__oneSheetItems = self.__itemCount / self.__fileNum 
            self.__lastFileItems = self.__oneSheetItems
        else:
            self.__oneSheetItems = self.__itemCount // self.__fileNum + 1     #Round up 
            self.__lastFileItems = self.__itemCount - self.__oneSheetItems * (self.__fileNum - 1)

    def split(self):
        """
        Start splitting.
        """
        isFinished = False
        idx = 0
        while( isFinished == False ):
            idx += 1
            isFinished = self.__createXmlByKey(str(idx))  
            print("")
        print("Splitting finished")

    def __getPercentageProgress(self,fileName:str)->ProgressBar:
        """
        Get a new process bar.
        :param fileName: the file lines in main sheet
        :return:  progressbar instance
        """
        widgets = [ 
            "Generate file " + str(fileName) + ":",
            Percentage()
        ] 
        bar = ProgressBar(widgets=widgets).start()
        return bar    

    def __parseMainSheet(self,line, newFile, splittedFile):
        """
        Parse the main sheet.
        :param line: the file lines in main sheet
        :param newFile: the new xml file which excludes the splitted items
        :param splittedFile: the splitted xml file
        """
        if self.__tabFinished == True:
            self.__newFileLines += 1
            newFile.write(line)
            splittedFile.write(line)
            return
        if line.find('</Table>') != -1:
            self.__tabFinished = True
            self.__newFileLines += 1
            newFile.write(line)
            splittedFile.write(line)
            return
        if self.__splittedFinished == False:
            self.__newFileLines += 1
            newFile.write(line)
            return
        if self.__keyNum == 0:
            if line.find('<Row') != -1:      
                self.__mainSheetRowCount += 1
                if self.__mainSheetRowCount == 7:
                    self.__findKeyRow = True
                    self.__newFileLines += 1
                    newFile.write(line)
                    splittedFile.write(line)
                    return
            if line.find('<Cell') != -1 and self.__findKeyRow == True:
                mergeAcrossPos = line.find('ss:MergeAcross')
                if mergeAcrossPos != -1:
                    splitList = line.split()
                    mergedNum = int(splitList[1].split("\"")[1])
                    self.__keyNum = mergedNum + 1
                else:
                    self.__keyNum = 1
                self.__newFileLines += 1
                newFile.write(line)
                splittedFile.write(line)
                self.__findKeyRow = False
                self.__mainSheetRowCount = 0
            else:
                self.__newFileLines += 1
                newFile.write(line)
                splittedFile.write(line)
                return
        else:
            if line.find('<Row') != -1:
                self.__rowCount += 1
                self.__hashKey = ""
                self.__columnNum = 0
                if self.__rowCount > (self.__oneSheetItems + 1):
                    self.__splittedFinished = False
                    self.__newFileLines += 1
                    newFile.write(line)
                    return
                if self.__rowCount > 1:
                    splittedFile.write(line)
                else:
                    self.__newFileLines += 1
                    newFile.write(line)
                    splittedFile.write(line)
                return
            if self.__rowCount <= 1:
                self.__newFileLines += 1
                newFile.write(line)
                splittedFile.write(line)
                return
            if line.find('<Cell') != -1:
                splittedFile.write(line)
                self.__columnNum += 1
                if self.__keyNum >= self.__columnNum:
                    beginPos = line.find('<Data')
                    endPos = line.find('</Data>')                            
                    if endPos != -1 and beginPos != -1:
                        dataStr = line[beginPos:endPos]
                        value = dataStr.split('>')[1]
                        value = value.strip()
                    else:
                        value = ""
                    if self.__hashKey == "":
                        self.__hashKey = "{" + value + "}"
                    else:
                        self.__hashKey = self.__hashKey + "|" + "{" + value + "}"
                    if self.__keyNum == self.__columnNum:
                        self.__splittedKeyList.append(self.__hashKey)
            elif line.find('</Cell>') != -1:
                splittedFile.write(line)
            if line.find('</Row>') != -1:
                splittedFile.write(line)

    def __parseSubSheet(self,line, newFile, splittedFile):
        """
        Parse the sub sheets.
        :param line: the file lines in sub sheets
        :param newFile: the new xml file which excludes the splitted items
        :param splittedFile: the splitted xml file
        """
        if self.__tabFinished == True:
            self.__newFileLines += 1
            newFile.write(line)
            splittedFile.write(line)
            return
        if line.find('</Table>') != -1:
            self.__tabFinished = True
            self.__newFileLines += 1
            newFile.write(line)
            splittedFile.write(line)
            return                   
        if line.find('<Row') != -1:
            self.__rowCount += 1
            self.__hashKey = ""
            if self.__rowCount >= 9:
                self.__columnNum = 0
                self.__subSheetRowList = []
                self.__subSheetRowList.append(line)
            else:
                self.__newFileLines += 1
                newFile.write(line)
                splittedFile.write(line)                                
            return
        if self.__rowCount < 9:
            self.__newFileLines += 1
            newFile.write(line)
            splittedFile.write(line)
            return
        if line.find('<Cell') != -1: 
            self.__subSheetRowList.append(line)                    
            self.__columnNum += 1
            if self.__keyNum >= self.__columnNum:
                beginPos = line.find('<Data')
                endPos = line.find('</Data>')                            
                if endPos != -1 and beginPos != -1:
                    dataStr = line[beginPos:endPos]
                    value = dataStr.split('>')[1]
                    value = value.strip()
                else:
                    value = ""
                if self.__hashKey == "":
                    self.__hashKey = "{" + value + "}"
                else:
                    self.__hashKey = self.__hashKey + "|" + "{" + value + "}"                
        elif line.find('</Cell>') != -1:
            self.__subSheetRowList.append(line)  
        if line.find('</Row>') != -1:
            self.__subSheetRowList.append(line)
            if self.__hashKey in self.__splittedKeyList:
                for row in self.__subSheetRowList:
                    splittedFile.write(row)
            else:
                if len(self.__subSheetRowList) > 0:
                    self.__hasInvalidData = True
                for row in self.__subSheetRowList:
                    self.__newFileLines += 1
                    newFile.write(row)   


        

    