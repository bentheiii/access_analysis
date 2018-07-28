# Access Analysis

This program can analyze ACLs and determine multiple properties about the information networks resulted.

## Properties
 * Invalid access: the program finds the shortest invalid access within the network (that is, the one that requires the fewest users to make)
 * BLP assignment: the program attempts to assign the files and users to security levels that fit into a BLP model. If it fails, it explains why.
 * UNIX assignment: the program attempts to assign each file an owner, an owner group, and access permissions in UNIX to represent the ACL. If it fails, it explains why.
 * Dot: the program parses the ACL into a DOT-style graph and uses graphvis to display it as an information flow graph. Both graphviz and the python library must be installed for this functionality.
 
## Setting Up
 * install python 3.6 or higher.
 * install [graphviz](https://www.graphviz.org/download/)
 * add graphviz's `bin` directory to windows's PATH
 * install [graphviz for python](https://pypi.org/project/graphviz/)

## Running
 * The main file is run.py
 * It accepts one positional argument- a txt file describing an ACL (see below for syntax)
 * It also accepts a positional --onlydo argo argument to restrict it to only do some of its regular functions. onlydo is a string that can contain any of the following letters:
   * i: check for invalid access
   * b: check for a BLP mapping
   * u: check for a unix mapping
   * d: run the dot conversion
 * run.py can also be run with the --help argument to print a usage page.

## Input Syntax
The input ACL file is a series of lines, each one describing the access rights to a file. Each line is of the syntax:

`<file name>:(<user0>,<permissions0>)->(<user1>,<permissions1>)...` 

so, for example, the ACL file with the contents:
```
passwords: (root,rw)->(jim,w)->(admin,r)
log: (root,rw)->(jim,rw)->(bob,rw)
diary: (jim,r)->(bob,w)
box:
```
means that:

 * root can read and write to both passwords and log
 * jim can write passwords, read from diary, and read-write log
 * admin can only read from passwords
 * bob can read-write log and write to diary
 * no one can read from or write to box
