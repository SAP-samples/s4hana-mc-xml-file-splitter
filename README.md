[![REUSE status](https://api.reuse.software/badge/github.com/SAP-samples/s4hana-mc-xml-file-splitter)](https://api.reuse.software/info/github.com/SAP-samples/s4hana-mc-xml-file-splitter)

# SAP S/4HANA Migration Cockpit XML File Splitter
Sample code for a command line interface program (implemented in Python3) that can split a large SAP S/4HANA Migration Cockpit XML file into smaller files. Using smaller files can improve performance. Note that this program is only relevant for the migration approach "Migrate Data Using Staging Tables".

## Contained Files

1. The LICENSE file:
In most cases, the license for SAP sample projects is `Apache 2.0`.
2. The README.md file (this file):
Contains information about using the program.
3. The bin folder:
The folder contains a compiled executable file that you can already use.
4. The src folder:
Contains the Python source code which you can download and compile.
5. The doc folder:
Contains information about Installing Python and required libraries.

## Requirements
1. A good working knowledge of the migration approach "Migrate Data Using Staging Tables", specifically with using and managing XML template files for data provisioning.
2. This program must only be used with SAP S/4HANA Migration Cockpit XML files.

## How to Run or Rebuild
1. The .exe file contained in the bin folder can be downloaded and run independently on Windows OS without any additional settings or configuration steps.
2. To run the File Splitter program, follow the command line prompt. You need to enter the following information:
   * 2.1 The name of the XML file that you want to split into smaller files.
   * 2.2 The number of XML files that you want to generate.
   * 2.3 Press Enter to start the process and monitor the task progress in console output.
3. You can compile the program yourself if required. You can download the source code and compile it in your local pre-installed Python environment. For information about installing Python and required libraries, see the [Help](doc) document.

## Known Issues
None for the time being.

## How to obtain support
SAP does not provide support for the sample code, but you can discuss the tool with other users on the [SAP Community](https://answers.sap.com/questions/ask.html).

## License
Copyright (c) 2022 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](LICENSE) file.
