# Wrapit
python command-line wrapping tool for c code base.(Only for Linux)
## Installing Dependencies
sudo apt-get install swig
## Running the script
Pass <file_name.c> and <filename.i> as command-line arguments.
## Example
  To wrap C code base for Python3 using python3
  ``` 
   python3 wrapit2py3.py file_name.c file_name.i
  ```
  To wrap C code base for Python2 using python3
  ```
    python3 wrapit2py2.py file_name.c file_name.i
  ```
  To wrap C code base for Python3 using python2
  ``` 
   python2 wrapit2py3.py file_name.c file_name.i
  ```
  To wrap C code base for Python2 using python2
  ```
    python wrapit2py2.py file_name.c file_name.i
  ```

### Note
Note: Refer the example test.c and test.i for reference.
