import re
from collections import OrderedDict
from header import *

def add_func(func_name,typ,mem):
	if(mem not in func_table[func_name][typ]):
		func_table[func_name][typ].append(mem)
					
func_name=None
operators = ['+','-','*','/']
ret_type = ["int","float","double","void"]
pre_un_op = "(\+\+|--)([a-zA-Z][\w]*)"
post_un_op = "([a-zA-Z][\w]*)(\+\+|--)"
fun_callop_pat = "([a-zA-Z][\w]*)\(.*\)"
func_pattern = "([\w_][\w_0-9]*)(?=\(.*\))"
param_pattern = "[\w]+[\s][\w_][\w_0-9]*\(([\w]+&?[\s][\w_][\w0-9_]*,?)+\)"
array_pattern = "([\w][\w]*)\[[0-9]+\];"
assgn_pattern = "([\w][\w_0-9]*)[\s]*(=)[\s]*([\w][\w_0-9]*);"  #a = c
arth_op_pattern = "([\w][\w_0-9]*)[\s]*(=)[\s]*([\w_0-9]+)[\s]*([-+*/])[\s]*([\w][\w_0-9]*);" #c = a + b

def process_func(var_dict,line):
	global func_name
	old_line = line #for assignment
	line = line.split()
	
	m_func_callop = re.search(fun_callop_pat,old_line)

	present = line[0] in var_dict.keys()
	if(present):  # if it is a variable declaration or if return type is template param

		m_ctor = re.match("([\w][\w]*)\((([\w]+,?)+)\);",line[1]) # copy ctor, add that var to var_dict
		m_func = re.search(func_pattern,old_line) # Template_type fun_name(params)
		m_array = re.match(array_pattern,line[1]) #array

		if(m_ctor):   #declaration of a variable: T c(a) or T c(1,2,3)
			handle_decl(var_dict,m_ctor,line[0])
			

		elif(m_func):  #matched function prototype
			m2 = re.search(param_pattern,old_line) #to match parameters
			func_name = m_func.group(0)
			func_table[func_name] = OrderedDict()

			if line[0] not in func_table[func_name].keys():
				func_table[func_name][line[0]] = []

			add_func(func_name,line[0],"copy_ctor")

			#extract the params
			if(m2):
				extract_param(func_name,m2,var_dict)

		elif(m_array): #array declaration T a[10];
			var_dict[line[0]].append(m_array.group(1))
			add_func(func_name,line[0],"0_arg_ctor")
		
		 
		else :  #matches T a;
			var_dict[line[0]].append(line[1][0:-1]) # add variable name to list
			add_func(func_name,line[0],"0_arg_ctor")

		add_func(func_name,line[0],"dtor")

	elif(len(line) > 1):

		m_func = re.search(func_pattern,old_line)  #ret_type functionname(parameter_list)
		m_assgn = re.match(assgn_pattern,old_line)
		m_arth = re.match(arth_op_pattern,old_line)

		if((line[0] in ret_type) and m_func):  #ret_type func_name(param list)
			func_name = m_func.group(0)
			func_table[func_name] = OrderedDict()
			m_param = re.search(param_pattern,old_line)

			if m_param:
				extract_param(func_name,m_param,var_dict)

		elif m_assgn: #assignment operation
			assgn_op(var_dict,m_assgn)
			

		elif m_arth: #arithmetic assignment pattern
			arth_op(var_dict,m_arth)
			
		elif(m_func_callop): #function callop b = a()
			typ = det_type(var_dict,m_func_callop.group(1))
			add_func(func_name,typ,"operator()")


	elif(len(line) == 1):  #unary op.. ++a or a++
		un_op(line[0],var_dict,m_func_callop)


def handle_decl(var_dict,m_ctor,typ):
	var_dict[typ].append(m_ctor.group(1))
	arg_list = m_ctor.group(2).split(',')
	arg_len = len(arg_list)

	if(arg_len == 1):
		if(arg_list[0] in var_dict[typ]):
			add_func(func_name,typ,"copy_ctor")

		else:
			add_func(func_name,typ,"1_arg_ctor")

	else:
		add_func(func_name,typ,str(arg_len)+"_arg_ctor")


def assgn_op(var_dict,m_assgn):	
	lhs = m_assgn.group(1)
	rhs = m_assgn.group(3)

	for typ in var_dict.keys():
		if(lhs in var_dict[typ] and rhs in var_dict[typ]):
			add_func(func_name,typ,"operator=")
			break	
	
def arth_op(var_dict,m_arth):
	lhs = m_arth.group(1);
	op1 = m_arth.group(3);
	op = m_arth.group(4);
	op2 = m_arth.group(5);

	for typ in var_dict.keys():
		if(lhs in var_dict[typ] and op1 in var_dict[typ] and op2 in var_dict[typ]):  #member operator function..c = a + b
			add_func(func_name,typ,"operator"+op)
			break	

		elif(lhs in var_dict[typ] and ((op1 in var_dict[typ] and op2 not in var_dict[typ]) or (op1 not in var_dict[typ] and op2 in var_dict[typ]))):  #friend_func c = 2 * a || c = a * 2
			add_func(func_name,typ,"friend_operator"+op)
			break

	add_func(func_name,typ,"operator=")										

def un_op(stmt,var_dict,m_func_callop):
	m_pre = re.match(pre_un_op,stmt)
	m_post = re.match(post_un_op,stmt)
	if(m_pre):
		typ = det_type(var_dict,m_pre.group(2))
		add_func(func_name,typ,"pre_operator"+m_pre.group(1))

	elif(m_post):

		typ = det_type(var_dict,m_post.group(1))
		add_func(func_name,typ,"post_operator"+m_post.group(2))

	elif(m_func_callop): #function call op a()
		typ = det_type(var_dict,m_func_callop.group(1))
		add_func(func_name,typ,"operator()")

	
def create_func_table(inp_fh):
       
	line = inp_fh.readline()
	while line:
		line = line.strip()
		
		if(len(line) > 0):
			if(line[0:8] =="template"):
		                line = line[9:-1].split(',')
		                var_dict = {}
		                for param in line:
		                        param = param.split()
		                        var_dict[param[1]] = []
		     	else:
				process_func(var_dict,line)
										
		line = inp_fh.readline()
	return func_table

def det_type(var_dict,var): 
	for typ in var_dict.keys():
		if var in var_dict[typ] :
			return typ

def extract_param(func_name,fun_param,var_dict):
	params = fun_param.group(0).split('(')[1].split(')')[0].split(',')
        #print("param:", params)
	add_cctor = True
        for i in params:
                p_type,p_name = i.split()
		if(p_type[-1] == '&'):  #check if the parameter is passed by ref, then dont add copy ctor
			p_type = p_type[0:-1]
			add_cctor = False
		else:
			add_cctor = True

	
		if p_type not in func_table[func_name].keys():
			func_table[func_name][p_type] = []

                if p_type in var_dict.keys():
			
                     	var_dict[p_type].append(p_name)
                        if(add_cctor and "copy_ctor" not in func_table[func_name][p_type]):  #passing of args requires copy ctor
                                func_table[func_name][p_type].append("copy_ctor")
			if(add_cctor and "dtor" not in func_table[func_name][p_type]):  #passing of args requires dtor
                                func_table[func_name][p_type].append("dtor")

