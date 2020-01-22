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
	# print(checked)
	checked = checked[7:]
	# print(checked)
	return checked

def generate_wrap_and_py_file(i_file,path):

	os.chdir(path)
	check_generation = subprocess.check_output(["swig","-python","{}".format(i_file)])
	check_generation = check_generation.decode('ascii')
	return check_generation

def compile_generated_files(wrap_file,c_file):

	check_compilation = subprocess.check_output(["gcc","-c", "-fpic", "{}".format(wrap_file), "{}".format(c_file), "-I/usr/include/python3.6m"])
	check_compilation = check_compilation.decode('ascii')
	return check_compilation

def generate_shared_object_files(object_file,wrap_object_file,file_name_raw):

	check_shared_obj_generation = subprocess.check_output(["gcc","-shared", "{}".format(object_file), "{}".format(wrap_object_file), "-o", "_{}.so".format(file_name_raw)])
	check_shared_obj_generation = check_shared_obj_generation.decode('ascii')
	return check_shared_obj_generation

def main():

	parser = argparse.ArgumentParser(description="Generate python3 wrapper for C programs using wrapit.")
	parser.add_argument("C", nargs = '*', metavar = "code", type = str , help="give the c file name you want to wrap for python3")
	parser.add_argument(".i",nargs='*',metavar=".i file",type=str,help="give the .i file name for building the wrapper")
	args = parser.parse_args()
	c_file , i_file = get_file_names(args)
	checked = check_swig()
	if(checked is not ""):
		print("swig found, generating wrap and py files....")
		path = "{}_wrap_files_py3".format(c_file[:-2])
		os.mkdir(path)
		copy2(c_file,path)
		copy2(i_file,path)
		check_generation = generate_wrap_and_py_file(i_file,path)
		if(check_generation is not ""):
			exit()
	else:
		print("Please install swig to continue.")
		exit()
	print("wrap and py files generated successfully!!")
	wrap_file = c_file[:-2]+"_wrap.c"
	py_file = c_file[:-2]+".py"
	print("Compiling generated files.....")
	check_compilation = compile_generated_files(wrap_file,c_file)
	if(check_compilation is not ""):
		exit()
	else:
		print("Compiled generated files successfully!!")
	object_file = c_file[:-2]+".o"
	wrap_object_file = c_file[:-2]+"_wrap.o"
	file_name_raw = c_file[:-2]
	print("Generating shared object file.....")
	check_shared_obj_generation = generate_shared_object_files(object_file,wrap_object_file,file_name_raw)
	if(check_shared_obj_generation is not ""):
		exit()
	else:
		print("Python3 wrapper for {} is successfully generated!!".format(c_file))

if __name__ == '__main__':
	
	main()
