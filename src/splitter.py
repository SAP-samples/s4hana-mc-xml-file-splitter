# Copyright: 2022 SAP SE or an SAP affiliate company
#
# License: Apache-2.0

import os
from progressbar import ProgressBar, Percentage, Bar


class XmlSplitter:
    """
    Implements the xml splitter, split xml file to several small size files
    """
    __each_file_instances = 50000
    __last_file_instances = 0
    __file_num = 0
    __file_fullname = ""
    __file_name = ""
    __table_finish = False
    __split_finish = True
    __keylist = []
    __key_num = 0
    __subsheet_rowlist = []
    __row_count = 0
    __column_num = 0
    __hashkey = ""
    __invalid = False
    __buffer_filename = ""
    __temp_filename = ""
    __instance_count = 0
    __main_sheet_rows = 0
    __find_key_row = False
    __file_lines = 0
    __buffer_file_lines = 0

    __WORKSHEET_PREFIX = "<Worksheet ss:Name"
    __ROW_PREFIX = "<Row"
    __CELL_PREFIX = "<Cell"
    __DATA_PREFIX = "<Data"
    __MERGE_ACCESS_PREFIX = "ss:MergeAcross"

    __TABLE_SUFFIX = "</Table>"
    __ROW_SUFFIX = "</Row>"
    __CELL_SUFFIX = "</Cell>"
    __DATA_SUFFIX = "</Data>"

    def __init__(self, full_name: str, file_num: int):
        """
        Constructor, initialize variables 
        :param full_name: xml file full name, includes the path
        :param file_num: the count of splitted files
        """
        self.__file_fullname = full_name
        self.__file_num = file_num
        self.__file_name = self.__file_fullname.split('.')[0]
        self.__buffer_filename = self.__file_name + "_bak" + '.xml'
        self.__temp_filename = self.__file_name + "_bak" + "_tmp.xml"
        if os.path.isfile(self.__buffer_filename) is True:
            raise NameError(self.__buffer_filename + " already exists.")
        if os.path.isfile(self.__temp_filename) is True:
            raise NameError(self.__temp_filename + " already exists.")
        self.__initialize()

    def __create_file(self, idx: str) -> bool:
        """
        Create splitted xml file by keys
        :param idx: the index of splitted xml file
        :return: Splitting files finished or not
        """
        worksheet = 0
        splitted_filename = self.__file_name + idx + '.xml'
        self.__buffer_file_lines = 0
        count = 0
        self.__key_num = 0
        self.__split_finish = True
        self.__invalid = False
        self.__keylist = []

        if os.path.isfile(splitted_filename) is True:
            raise NameError(splitted_filename + " already exists.")

        if int(idx) == self.__file_num:
            self.__each_file_instances = self.__last_file_instances

        original_file_name = ""
        if os.path.isfile(self.__buffer_filename) is True:
            original_file_name = self.__buffer_filename
        else:
            original_file_name = self.__file_fullname

        progress_bar = self.__get_progress(splitted_filename)

        with open(original_file_name, "r", encoding="utf-8") as original_file:
            with open(self.__temp_filename, "w+", encoding="utf-8") as buffer_file:
                with open(self.__file_name + idx + ".xml", "w+", encoding="utf-8") as splitted_file:
                    for line in original_file:
                        count += 1
                        progress_bar.update(int(count*100/self.__file_lines))
                        if line.find(self.__WORKSHEET_PREFIX) != -1:
                            self.__table_finish = False
                            self.__row_count = 0
                            self.__column_num = 0
                            worksheet = worksheet + 1
                        if worksheet < 3:
                            self.__buffer_file_lines += 1
                            buffer_file.write(line)
                            splitted_file.write(line)
                            continue
                        if worksheet == 3:
                            self.__parse_main_sheet(
                                line, buffer_file, splitted_file)
                        else:
                            self.__parse_subsheet(
                                line, buffer_file, splitted_file)
                splitted_file.close()
            buffer_file.close()
        original_file.close()
        self.__file_lines = self.__buffer_file_lines

        if os.path.isfile(self.__buffer_filename) is True:
            os.remove(self.__buffer_filename)
        os.rename(self.__temp_filename, self.__buffer_filename)

        if self.__split_finish is True:
            if os.path.isfile(self.__buffer_filename) is True:
                if self.__invalid is False:
                    os.remove(self.__buffer_filename)
                else:
                    os.rename(self.__buffer_filename,
                              self.__file_name + "_invalid_data" + ".xml")
        return self.__split_finish

    def __initialize(self):
        """
        Scan the original file and get the count of instances and the lines of the file.
        """
        worksheet = 0
        row_count = 0
        header_count = 0
        scan_main_finish = False
        if os.path.isfile(self.__file_fullname) is not True:
            raise NameError(self.__file_fullname + " does not exist.")
        with open(self.__file_fullname, "r", encoding="utf-8") as original_file:
            for line in original_file:
                self.__file_lines += 1
                if scan_main_finish is True:
                    continue
                if line.find(self.__WORKSHEET_PREFIX) != -1:
                    worksheet = worksheet + 1
                if worksheet < 3:
                    continue
                if worksheet == 3:
                    if line.find(self.__ROW_PREFIX) != -1:
                        if header_count < 8:
                            header_count += 1
                        else:
                            row_count += 1
                            scan_instances = "Scanning file instances:" + \
                                str(row_count)
                            print(scan_instances, end="")
                            print("\b" * (len(scan_instances)),
                                  end="", flush=True)

                    if line.find(self.__TABLE_SUFFIX) != -1:
                        scan_main_finish = True
                        continue
        original_file.close()
        print("")

        self.__instance_count = row_count
        if self.__instance_count <= 1:
            raise ValueError("There is no instance to be splitted.")
        if self.__instance_count < self.__file_num:
            raise ValueError(
                "The number of splitted files is more than the instances.")
        if self.__instance_count % self.__file_num == 0:
            self.__each_file_instances = self.__instance_count / self.__file_num
            self.__last_file_instances = self.__each_file_instances
        else:
            self.__each_file_instances = self.__instance_count // self.__file_num  # Round down
            self.__last_file_instances = self.__instance_count - \
                self.__each_file_instances * (self.__file_num - 1)
        print(f"A total of {self.__file_num} files will be generated...")

    def split(self):
        """
        Start splitting.
        """
        finish = False
        idx = 0
        while finish is False:
            idx += 1
            finish = self.__create_file(str(idx))
            print("")
        print("Files generated successfully.")

    def __get_progress(self, filename: str) -> ProgressBar:
        """
        Get a new process bar.
        :param filename: the file lines in main sheet
        :return:  progressbar instance
        """
        widgets = [
            "Generating file " + str(filename) + ":",
            Percentage(),
            Bar("=")
        ]
        progress_bar = ProgressBar(widgets=widgets, term_width=100).start()
        return progress_bar

    def __parse_main_sheet(self, line: str, buffer_file, splitted_file):
        """
        Parse the main sheet.
        :param line: the file lines in main sheet
        :param buffer_file: the buffer xml file which excludes the splitted items
        :param splitted_file: the generated xml file
        """

        if self.__table_finish is True:
            self.__buffer_file_lines += 1
            buffer_file.write(line)
            splitted_file.write(line)
            return
        if line.find(self.__TABLE_SUFFIX) != -1:
            self.__table_finish = True
            self.__buffer_file_lines += 1
            buffer_file.write(line)
            splitted_file.write(line)
            return
        if self.__split_finish is False:
            self.__buffer_file_lines += 1
            buffer_file.write(line)
            return
        if self.__key_num == 0:
            if line.find(self.__ROW_PREFIX) != -1:
                self.__main_sheet_rows += 1
                if self.__main_sheet_rows == 7:
                    self.__find_key_row = True
                    self.__buffer_file_lines += 1
                    buffer_file.write(line)
                    splitted_file.write(line)
                    return
            if line.find(self.__CELL_PREFIX) != -1 and self.__find_key_row is True:
                mergeacross_pos = line.find(self.__MERGE_ACCESS_PREFIX)
                if mergeacross_pos != -1:
                    splitlist = line.split()
                    merged_num = int(splitlist[1].split("\"")[1])
                    self.__key_num = merged_num + 1
                else:
                    self.__key_num = 1
                self.__buffer_file_lines += 1
                buffer_file.write(line)
                splitted_file.write(line)
                self.__find_key_row = False
                self.__main_sheet_rows = 0
            else:
                self.__buffer_file_lines += 1
                buffer_file.write(line)
                splitted_file.write(line)
                return
        else:
            if line.find(self.__ROW_PREFIX) != -1:
                self.__row_count += 1
                self.__hashkey = ""
                self.__column_num = 0
                if self.__row_count > (self.__each_file_instances + 1):
                    self.__split_finish = False
                    self.__buffer_file_lines += 1
                    buffer_file.write(line)
                    return
                if self.__row_count > 1:
                    splitted_file.write(line)
                else:
                    self.__buffer_file_lines += 1
                    buffer_file.write(line)
                    splitted_file.write(line)
                return
            if self.__row_count <= 1:
                self.__buffer_file_lines += 1
                buffer_file.write(line)
                splitted_file.write(line)
                return
            if line.find(self.__CELL_PREFIX) != -1:
                splitted_file.write(line)
                self.__column_num += 1
                if self.__key_num >= self.__column_num:
                    begin_pos = line.find(self.__DATA_PREFIX)
                    end_pos = line.find(self.__DATA_SUFFIX)
                    if end_pos != -1 and begin_pos != -1:
                        data_str = line[begin_pos:end_pos]
                        value = data_str.split('>')[1]
                        value = value.strip()
                    else:
                        value = ""
                    if self.__hashkey == "":
                        self.__hashkey = "{" + value + "}"
                    else:
                        self.__hashkey = self.__hashkey + \
                            "{" + value + "}"
                    if self.__key_num == self.__column_num:
                        self.__keylist.append(self.__hashkey)
            elif line.find(self.__CELL_SUFFIX) != -1:
                splitted_file.write(line)
            if line.find(self.__ROW_SUFFIX) != -1:
                splitted_file.write(line)

    def __parse_subsheet(self, line: str, buffer_file, splitted_file):
        """
        Parse the sub sheets.
        :param line: the file lines in sub sheets
        :param buffer_file: the buffer xml file which excludes the splitted items
        :param splitted_file: the splitted xml file
        """
        if self.__table_finish is True:
            self.__buffer_file_lines += 1
            buffer_file.write(line)
            splitted_file.write(line)
            return
        if line.find(self.__TABLE_SUFFIX) != -1:
            self.__table_finish = True
            self.__buffer_file_lines += 1
            buffer_file.write(line)
            splitted_file.write(line)
            return
        if line.find(self.__ROW_PREFIX) != -1:
            self.__row_count += 1
            self.__hashkey = ""
            if self.__row_count >= 9:
                self.__column_num = 0
                self.__subsheet_rowlist = []
                self.__subsheet_rowlist.append(line)
            else:
                self.__buffer_file_lines += 1
                buffer_file.write(line)
                splitted_file.write(line)
            return
        if self.__row_count < 9:
            self.__buffer_file_lines += 1
            buffer_file.write(line)
            splitted_file.write(line)
            return
        if line.find(self.__CELL_PREFIX) != -1:
            self.__subsheet_rowlist.append(line)
            self.__column_num += 1
            if self.__key_num >= self.__column_num:
                begin_pos = line.find(self.__DATA_PREFIX)
                end_pos = line.find(self.__DATA_SUFFIX)
                if end_pos != -1 and begin_pos != -1:
                    data_str = line[begin_pos:end_pos]
                    value = data_str.split(">")[1]
                    value = value.strip()
                else:
                    value = ""
                if self.__hashkey == "":
                    self.__hashkey = "{" + value + "}"
                else:
                    self.__hashkey = self.__hashkey + "{" + value + "}"
        elif line.find(self.__CELL_SUFFIX) != -1:
            self.__subsheet_rowlist.append(line)
        if line.find(self.__ROW_SUFFIX) != -1:
            self.__subsheet_rowlist.append(line)
            if self.__hashkey in self.__keylist:
                for row in self.__subsheet_rowlist:
                    splitted_file.write(row)
            else:
                if len(self.__subsheet_rowlist) > 0:
                    self.__invalid = True
                for row in self.__subsheet_rowlist:
                    self.__buffer_file_lines += 1
                    buffer_file.write(row)
