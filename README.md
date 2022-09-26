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
We expect the target audience of this extended program to be a group of skilled users in SAP S/4HANA Migration Cockpit with good understanding of the template file and the way of data provisioning.

## Download and Installation
1. The exe file offered in this project's bin folder can be downloaded and run independently on Windows OS without any additional settings or configurations and the only input to it should be a legitimate S/4HANA Migraiton Cockpit File Staging compatible data file.
2. Follow the command line prompt to input following parameters in order:
   2.1 the oversized source file which you want to break into smaller ones
   2.2 the number of smaller files you want to generate
   2.3 press Enter to start the split process
3. To build the program by youself, just download and build the source code with a pre-installed Python environment.

## Known Issues
None for the time being.

## How to obtain support
[Create an issue](https://github.com/SAP-samples/<repository-name>/issues) in this repository if you find a bug or have questions about the content.
 
For additional support, [ask a question in SAP Community](https://answers.sap.com/questions/ask.html).

## Contributing
If you wish to contribute code, offer fixes or improvements, please send a pull request. Due to legal reasons, contributors will be asked to accept a DCO when they create the first pull request to this project. This happens in an automated fashion during the submission process. SAP uses [the standard DCO text of the Linux Foundation](https://developercertificate.org/).

## License
Copyright (c) 2022 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](LICENSE) file.
