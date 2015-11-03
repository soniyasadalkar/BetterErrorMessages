from header import *
import re
from match_requirements import *
def generate_error(inp_fh):
	var_main = {}
	
	line = inp_fh.readline()
	decl_pattern = "([a-zA-Z][\w]*)[\s]+([a-zA-Z][\w]*);"
	func_call_pat = "([a-zA-Z][\w]*)\((.*)\);"
	while line:
		line = line.strip()
		old_line = line
		line = line.split()
		if(len(line) > 0):
			m_decl = re.match(decl_pattern,old_line)
			m_func = re.search(func_call_pat,old_line)

			if(m_decl):
				if(m_decl.group(1) not in var_main.keys()):  #declaration of variable.. InputClass ic;
					var_main[m_decl.group(1)] = []
				var_main[m_decl.group(1)].append(m_decl.group(2))	
		
			if(m_func):
				func_name = m_func.group(1)
				args = m_func.group(2)
				args = args.split(',')
				arg_typ_list = []
				for arg in args:
					 get_type(arg,var_main,arg_typ_list)
				
				
				match_requirements(func_name,arg_typ_list)
		line = inp_fh.readline()		

def get_type(arg,var_main,arg_typ_list):
	for typ in var_main.keys():
		if((arg in var_main[typ]) and (typ not in arg_typ_list)):
			arg_typ_list.append(typ)

