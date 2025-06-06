# Copyright: 2025 SAP SE or an SAP affiliate company
#
# License: Apache-2.0

from traceback import print_exc
import os
from splitter import XmlSplitter


def print_help():
    """
    Print help document
    """

    print("You can use this program to split a large SAP S/4HANA Migration Cockpit XML file into smaller files.")
    print("--version 1.0")
    print("")


def main():
    """
    The main entry
    """
    print_help()
    os.system("")
    while True:
        filename = input(
            "Enter the name of the XML file that you want to split into smaller files:")
        if filename == "":
            print("\033[31mYou did not enter a file name.\033[0m")
            continue
        uppercase_name = filename.upper()
        if uppercase_name.find(".XML") == -1:
            print("\033[31mThe specified file is not an XML file.\033[0m")
            continue
        if os.path.isfile(uppercase_name) is not True:
            print(f"\033[31m{uppercase_name} does not exist.\033[0m")
            continue
        break

    while True:
        num = input("Enter the number of XML file that you want to generate:")
        try:
            file_num = int(num)
        except Exception:
            print("\033[31mYou did not enter a number.\033[0m")
            continue
        if file_num <= 1:
            print("\033[31mSpecify a value greater than 1.\033[0m")
            continue
        break

    try:
        splitter = XmlSplitter(filename, file_num)
        splitter.split()
    except Exception as error:
        log_file = open("errors.log", "a+", encoding="utf-8")
        print_exc(file=log_file)
        log_file.close()
        print(f"\033[31m{error}\033[0m")


if __name__ == "__main__":
    main()
    input("Press Enter to exit…")
