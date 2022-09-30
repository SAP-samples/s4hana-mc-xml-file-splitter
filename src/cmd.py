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
    os.system("")
    while True:
        filename = input("Please enter file name:")
        if filename == "":
            print("\033[31mFile name cannot be empty\033[0m")
            continue
        uppercase_name = filename.upper()
        if uppercase_name.find(".XML") == -1:
            print("\033[31minput file is not XML file\033[0m")
            continue
        if os.path.isfile(uppercase_name) is not True:
            print(f"\033[31m{uppercase_name} does not exist\033[0m")
            continue
        break

    while True:
        num = input("Please enter the number of the splitted files:")
        try:
            file_num = int(num)
        except Exception:
            print("\033[31mInput value should be numbers\033[0m")
            continue
        if file_num <= 1:
            print("\033[31mInput value should be bigger than 1\033[0m")
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
