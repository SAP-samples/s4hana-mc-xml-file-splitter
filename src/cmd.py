from shutil import copyfile
from sys import exit
from splitter import xmlSplitter
import fileinput
import os

def printHelp():
    """
    Print help document
    """
    print("Split oversized MC files into smaller units which can then be fed into S/4 HANA Migration Cockpit File Staging approach for further processing of data provisioning.")
    print("--version 1.0")
    print("")

def main():
    """
    The main entry
    """    
    printHelp()

    while True:
        filename = input("Please enter file name:")
        if filename == "":
            print('[Error]File name cannot be empty')
            continue
        uppercaseName = filename.upper()
        if uppercaseName.find('.XML') == -1:
            print("[Error]input file is not XML file")
            continue
        if os.path.isfile(uppercaseName) is not True:  
            print("[Error]" + uppercaseName + " does not exist")
            continue
        break

    while True:
        num = input("Please enter the number of the splitted files:")
        try:
            fileNum = int(num)
        except:
            print("[Error]Input should be numbers")
            continue
        if fileNum <= 1:
            print("[Error]Input should be bigger than 1")
            continue
        break

    splitter = xmlSplitter(filename, fileNum)
    splitter.split() 

    # try:
    #     splitter = xmlSplitter(filename, fileNum)
    #     splitter.split() 
    # except Exception as error:
    #     print(f"[Error]{error}")

if __name__ == "__main__":
    main()
    input("Press Enter to exit…")
