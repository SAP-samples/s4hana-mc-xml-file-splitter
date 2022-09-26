# SAP-samples/s4hana-mc-xml-file-splitter
Sample code of a small command line interface program implemented in Python, to facilitate customers’ data migration by splitting oversized XML data file into smaller ones which can then be fed into S/4 HANA Migration Cockpit File Staging approach for further processing without causing too much memory overhead and network traffic timeout.

# Containing Files

1. The LICENSE file:
In most cases, the license for SAP sample projects is `Apache 2.0`.

2. The README.md file (this file):

3. the splitter.exe file 

4. The source code in src folder

## Description
<!-- Please include SEO-friendly description -->

## Requirements
We expect that the target audience of this extended program to be a group of skilled users in the usage of SAP S/4HANA Migration Cockpit with good understanding of the template file and its way of data provisioning.

## To run or rebuild
1. The exe file shipped in this project's bin folder can be downloaded and run independently on Windows OS without any additional settings or configurations.
2. The only input to this program MUST be a legitimate S/4HANA Migraiton Cockpit File Staging compatible data file.
2. Follow the command line prompt to input following parameters in order:
   * 2.1 the name of oversized source file which you want to break into smaller ones
   * 2.2 the number of target files you want to generate as a result
   * 2.3 Start the split process by pressing Enter and monitor the task progress in console output
3. To build the program from scratch, just download the source code and build it with a pre-installed Python environment.

## Known Issues
None for the time being.

## How to obtain support
[Create an issue](https://github.com/SAP-samples/s4hana-mc-xml-file-splitter/issues) in this repository if you find a bug or have questions about the content.
 
For additional support, [ask a question in SAP Community](https://answers.sap.com/questions/ask.html).

## Contributing
If you wish to contribute code, offer fixes or improvements, please send a pull request. Due to legal reasons, contributors will be asked to accept a DCO when they create the first pull request to this project. This happens in an automated fashion during the submission process. SAP uses [the standard DCO text of the Linux Foundation](https://developercertificate.org/).

## License
Copyright (c) 2022 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](LICENSE) file.
