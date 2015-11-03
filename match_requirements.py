from header import *

def match_requirements(func_name,arg_typ_list):
	func_typ_dict = func_table[func_name]
	i = 0
	for param_typ in func_typ_dict.keys(): 
		arg_typ = arg_typ_list[i]
		un_req = match(class_table[arg_typ],func_typ_dict[param_typ])
		if(len(un_req) > 0):
			print(func_name+"..... "+str(un_req)+" not supported by " + arg_typ + "\n")
		else:
			print("Template parameter " + param_typ + " supports all the requirements of " + func_name + "()\n")
		i = i + 1	
		
	
def match(class_list,func_list):
	unmatched_req = []
	for func in func_list:
		if func not in class_list:
			unmatched_req.append(func)

	return unmatched_req


