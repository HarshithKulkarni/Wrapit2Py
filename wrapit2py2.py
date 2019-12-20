import subprocess
import argparse
import os
from shutil import copy2

def get_file_names(args):
	
	c_file = args.C[0]
	i_file = args.C[1]
	return c_file,i_file

def check_swig():

	checked = subprocess.check_output(["whereis","swig"])
	checked = checked.strip()
	checked = checked.decode('ascii')
	checked = checked[7:]
	return checked

def generate_wrap_and_py_file(i_file,path):

	os.chdir(path)
	subprocess.call(["swig","-python","{}".format(i_file)])

def compile_generated_files(wrap_file,c_file):

	subprocess.call(["gcc","-c", "-fpic", "{}".format(wrap_file), "{}".format(c_file), "-I/usr/include/python2.7"])

def generate_shared_object_files(object_file,wrap_object_file,file_name_raw):

	subprocess.call(["gcc","-shared", "{}".format(object_file), "{}".format(wrap_object_file), "-o", "_{}.so".format(file_name_raw)])

def main():

	parser = argparse.ArgumentParser(description="Generate python3 wrapper for C programs using wrapit.")
	parser.add_argument("C", nargs = '*', metavar = "code", type = str , help="give the c file name you want to wrap for python3")
	parser.add_argument(".i",nargs='*',metavar=".i file",type=str,help="give the .i file name for building the wrapper")
	args = parser.parse_args()
	c_file , i_file = get_file_names(args)
	checked = check_swig()
	if(checked is not ""):
		print("swig found, generating wrap and py files....")
		path = "{}_wrap_files_py2".format(c_file[:-2])
		os.mkdir(path)
		copy2(c_file,path)
		copy2(i_file,path)
		generate_wrap_and_py_file(i_file,path)
	else:
		print("Please install swig to continue.")
		exit()
	print("wrap and py files generated successfully!!")
	wrap_file = c_file[:-2]+"_wrap.c"
	py_file = c_file[:-2]+".py"
	print("Compiling generated files.....")
	compile_generated_files(wrap_file,c_file)
	print("Compiled generated files successfully!!")
	object_file = c_file[:-2]+".o"
	wrap_object_file = c_file[:-2]+"_wrap.o"
	file_name_raw = c_file[:-2]
	print("Generating shared object file.....")
	generate_shared_object_files(object_file,wrap_object_file,file_name_raw)
	print("Python2 wrapper for {} is successfully generated!!".format(c_file))

if __name__ == '__main__':
	
	main()