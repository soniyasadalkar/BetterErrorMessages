from header import *
import re
def create_class_table(inp_fh):
	
	line = inp_fh.readline()
	bin_op_pattern = "operator([-+*/=])\(const"
	post_un_pat = "operator(\+\+|--)\(int[\s][\w]+\)"
	pre_un_pat = "operator(\+\+|--)\(\)"
	fun_callop_pat = "operator\(\)\(.*\)"
	ctor_param_pat = "\((([a-zA-Z]+[\s][\w]+,?)+)\)"

	while line:
		line = line.strip()
		old_line = line
		line = line.split()
		
		
		if(len(line) > 0):
			m_bin = re.match(bin_op_pattern,line[1]) if (len(line) > 1) else 0   #ternary operator
			m_post = re.search(post_un_pat,old_line)
			m_pre = re.match(pre_un_pat,line[1]) if (len(line) > 1) else 0
			m_func_callop = re.search(fun_callop_pat,old_line) 
			m_ctor_param = re.search(ctor_param_pat,old_line)

			if(line[0] == 'class'):
				class_name = line[1]
				class_table[class_name] = []
				bc_list = []	#base class list for every class

			if(len(line) > 2 and line[2] == ':'): #inheritance
				bc_line = ' '.join(line[3:])  #reconstruct the old string
				bc_line = bc_line.split(',') 
				for bc in bc_line :
					bc = bc.split() 
					bc_list.append(bc[1])
				

			elif(line[0] == 'private:'):
				
				skip = True
				p_line = inp_fh.readline()
				p_line = p_line.strip()
				while(skip):
					if(p_line == 'public:'):
						skip = False
					if(p_line == '};'):
						line[0] = '};'   #to enter base class function names in class_list 
						skip = False
					if(skip):			
						p_line = inp_fh.readline()
						p_line = p_line.strip()

			elif(line[0] == class_name+"();"):  #0_arg_ctor
				if("0_arg_ctor" not in class_table[class_name]):
					class_table[class_name].append("0_arg_ctor")

			elif(line[0] == class_name + "(const" and line[1] == class_name + "&"): #copy ctor
				class_table[class_name].append("copy_ctor")
				
			elif(re.search(class_name+"\(",line[0]) and m_ctor_param):#parameterised ctor
				num_param = len(m_ctor_param.group(1).split(','))
				class_table[class_name].append(str(num_param) + "_arg_ctor")

			elif(line[0] == "~"+class_name+"();"): #dtor
				class_table[class_name].append("dtor")
			
			elif(((line[0] == class_name + "&") or (line[0] == class_name)) and m_bin and line[2] == class_name + "&"): #bin operators
				class_table[class_name].append("operator"+m_bin.group(1))

			elif(line[0] == class_name + "&" and m_pre): #pre op
				class_table[class_name].append("pre_operator"+m_pre.group(1))

			elif(line[0] == class_name and m_post): #post op
				class_table[class_name].append("post_operator"+m_post.group(1))
		
		
			elif(line[0] == 'friend'):  #friend func
				m_fr = re.match(bin_op_pattern,line[2])
				if(line[1] == class_name and m_fr):
					class_table[class_name].append("friend_operator"+m_fr.group(1))
				
			elif(m_func_callop):  #operator()
				class_table[class_name].append("operator()")
		
		
		if(len(line) > 0 and line[0] == "};"):   #to add base_class functions to derived class func_list
			for bc in bc_list:
				class_list = class_table[bc] 
				for func in class_list:
					if func not in class_table[class_name]:
						class_table[class_name].append(func)	

		line = inp_fh.readline()
	
	
	
	check_and_add_default()	 #provide default fundamental operations if not provided explicitly 
	return class_table
       

def check_and_add_default():
	def_mem = ["dtor","copy_ctor","operator="]
	arg_ctor_pat = "[0-9]+_arg_ctor"
	
	for cls in class_table.keys():
		
		ctor = False
		for mem in class_table[cls]:
			m_ctor = re.match(arg_ctor_pat,mem)
			if(m_ctor):
				 ctor = True
				 break
		if(ctor == False):		
			class_table[cls].append("0_arg_ctor");

		for mem in def_mem:
			if(mem not in class_table[cls]):
				 class_table[cls].append(mem);
					
		
			



