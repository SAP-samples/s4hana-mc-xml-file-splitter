# Copyright: 2022 SAP SE or an SAP affiliate company
#
# License: Apache-2.0

from traceback import print_exc
import os
from splitter import XmlSplitter


def print_help():
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
    print_help()

    while True:
        filename = input("Please enter file name:")
        if filename == "":
            print("[Error]File name cannot be empty")
            continue
        uppercase_name = filename.upper()
        if uppercase_name.find(".XML") == -1:
            print("[Error]input file is not XML file")
            continue
        if os.path.isfile(uppercase_name) is not True:
            print("[Error]" + uppercase_name + " does not exist")
            continue
        break

    while True:
        num = input("Please enter the number of the splitted files:")
        try:
            file_num = int(num)
        except Exception:
            print("[Error]Input value should be numbers")
            continue
        if file_num <= 1:
            print("[Error]Input value should be bigger than 1")
            continue
        break

    try:
        splitter = XmlSplitter(filename, file_num)
        splitter.split()
    except Exception as error:
        log_file = open("errors.log", "a+", encoding="utf-8")
        print_exc(file=log_file)
        log_file.close()
        print(f"[Error]{error}")


if __name__ == "__main__":
    main()
    input("Press Enter to exit…")
