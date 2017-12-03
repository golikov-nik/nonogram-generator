# Index
A tool used to generate nonogram by picture  

# Getting started
To run this you need to have python3 installed.  
Installation:  
Run command `pip install -r requirements.txt` in order to install all prerequired packages.  

# Usage
To run this, you need to have `nonogram.py` runnable and `template.tex` in the same folder.  
Use the following syntax: `python nonogram.py <Input file> [<Input parameters>]`  
Input file is a picture in .pbm format  <http://netpbm.sourceforge.net/doc/pbm.html>  
To view help use parameter `-h` or `--help`.  

# Example
In the source directory you can find test file test.pbm  
Run command:  
`python nonogram.py test.pbm`  
The resulting out.tex file will be created in your directory.
