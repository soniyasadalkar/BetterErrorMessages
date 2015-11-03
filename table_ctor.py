from class_table import *
from func_table import *
from match_requirements import *
from generate_error import *

def requirement_matcher(class_file,func_file,main_file):
		
	fc = open(class_file,'r')
	class_table = create_class_table(fc)
	fc.close()
	print("\n")
	print('-'*80)
	print("Class Table")
	print("\n")
	for key in class_table.keys():
	   print (key,class_table[key])
	   #print("\n")
	print("\n")
	print('-'*80)
	
	
	ff = open(func_file,'r')
	func_table = create_func_table(ff)
	ff.close()

	print("Function Table")
	print("\n")
	for key1 in func_table.keys():
		print(key1)
		for key2 in func_table[key1].keys():
	   		print (key2,func_table[key1][key2])
			#print("\n")
	
	print('-'*80)
	print("\n")
	print("Errors\n\n")
	fm = open(main_file,'r')
	generate_error(fm)
	fm.close()
		


