
"""
							Assignment 1 : Prolog Unification
							Submitted By : First Name : Amal Majeed 
											Last Name : Mucheth Abdul Majeed
											Student Number : 200415928

"""



"""
	Program	Constraint : All variables, functions and constants are single characters and not strings.
						Any string(more than one alphabets together) will be treated as Invalid in this 
						program.

						Variables are Uppercase , function names and constants are Lower case
"""

"""
		Instruction to run : 'python assign1amalmajeed.py'

		Example inputs : Expr 1 : f(x,Y)    - function with x - constant and Y - variable
						 Expr 2 : f(A,g(A)) - function with A - variable and g(A) - function 

						 Unified expression : f(x,g(x))

		Screenshots of same example and a failure case example have been attached with the zip file

"""

#Global variables

glb_err_flg = True
replace_map = {}
input_list1 = []
input_list2 = []
function_list1 = []
function_list2 = []
variables_list = []
variables_list1 = []
variables_list2 = []
constants_list1 = []
constants_list2 = []
exp1 = []
exp2 = []

def type_identify(str_list):
	"""
		Function that returns VAR , CONST , FUN or INVALID(for syntax errors) 
		as type of identified character or sequence
	"""
	fstck = []
	lstr = len(str_list) 
	if(lstr == 1):
		if(str_list[0].islower()):
			return "CONST"
		else:
			return "VAR"
	else:
		if((not "(" in str_list) or (not ")" in str_list)):
			# Invalid function format or character string 
			return "INVALID"
		for i,j in enumerate(str_list):
			if((i+1 != lstr) and (j.isupper() and ((str_list[i+1] != ",") and (str_list[i+1] != ")")))):
				# Functions with Uppercase label and string variables are INVALID
				return "INVALID"
			if((i+1 != lstr) and (j.islower() and ((str_list[i+1] != "(") and (str_list[i+1] != ",") and (str_list[i+1] != ")")))):
				# Functions with string labels and string constants are INVALID
				return "INVALID"
			if(j=="("):
				fstck.append(j)
			if(j==")"):
				if(len(fstck)==0):
					# Closed braces without an open is incorrect function syntax and hence INVALID
					return "INVALID"
				temp = fstck.pop()
		if len(fstck) != 0:
			# Open braces without a close is incorrect function syntax and hence INVALID
			return "INVALID"
		else:
			return "FUN"


def map_populate(arg1,arg2):
	"""
		Function to update and track variable mappings for unification
	"""
	global replace_map
	if(arg1 not in replace_map.keys()):
		replace_map[arg1] = arg2
	else:
		tflg = True
		i = arg1
		while(tflg):
			if(replace_map[i] not in replace_map.keys()):
				tflg = False
				replace_map[replace_map[i]] = arg2
			else:
				i = replace_map[i]

def format_map():
	"""
		Function to re assign variables after performing transitive assignments ,
		i.e if A=B , B=C then this function assigns A=C
	"""
	global replace_map,input_list1,input_list2
	for i in replace_map:
		if i.islower() and len(i)==1:
			for j in replace_map:
					if(j!=i):
						replace_map[j]=replace_map[j].replace(replace_map[i],i)
		else:	
			for j in replace_map:
				replace_map[j]=replace_map[j].replace(i,replace_map[i])

def map_check():
	"""
		Function to check if there are constants or functions invalidly assigned to be replaced
	"""
	global replace_map,input_list1,input_list2
	for i in replace_map:
		if i.islower() and len(i)==1:
			if replace_map[i].islower() and len(replace_map[i])==1:
				if(i!=replace_map[i]):
					print "Two different constants cannot be assigned to same variable !"
					return False
			elif(replace_map[i][0].islower() and replace_map[i][1]=="("):
				if(i!=replace_map[i]):
					print "Function and a constant cannot be assigned to same variable !"
					return False
		elif i[0].islower() and i[1]=="(":
			if(i!=replace_map[i]):
					print "Two different functions cannot be assigned to same variable !"
					return False
			elif(replace_map[i].islower() and len(replace_map[i])==1):
				if(i!=replace_map[i]):
					print "Function and a constant cannot be assigned to same variable !"
					return False
	return True


def unify(input_list1,input_list2,Condition):
	"""
	Function that recursively checks the expression for syntax errors/ type mismatch to perform
	assignments to try and unify the two expressions.
	"""
	t1_type = type_identify(input_list1)
	t2_type = type_identify(input_list2)
	global glb_err_flg
	global replace_map
	if(t1_type == "VAR"):
		if(t2_type == "CONST"):
			# CASE 1 : variable and constant
			print "Yes , Unification Possible !","\n","".join(input_list1),"=","".join(input_list2)
			map_populate("".join(input_list1),"".join(input_list2))
			return True
		elif(t2_type == "VAR"):
			# CASE 2 : 2 variables
			print "Yes , Unification Possible !","\n","".join(input_list1),"=","".join(input_list2)
			map_populate("".join(input_list1),"".join(input_list2))
			return True
		elif(t2_type == "INVALID"):
			# CASE 3 : INVALID syntax , unification not possible
			print "No , Unification is not Possible due to invalid syntax of Term 2 !","\n"
			return False
		else:
			# CASE 4 : variable and function
			print "Yes , Unification Possible !","\n","".join(input_list1),"=","".join(input_list2)
			map_populate("".join(input_list1),"".join(input_list2))
			return True
	elif(t1_type == "CONST"):
		if(t2_type == "CONST"):
			# CASE 1 : 2 constants
			if(input_list1[0]==input_list2[0]):
				print "Yes , Unification Possible !","\n","".join(input_list1),"=","".join(input_list2)
				map_populate("".join(input_list1),"".join(input_list2))
				return True
			else:
				print "No , Unification is not Possible for unequal constants!","\n"
				return False
		elif(t2_type == "VAR"):
			# CASE 2 : constant and variable
			print "Yes , Unification Possible !","\n","".join(input_list2),"=","".join(input_list1)
			map_populate("".join(input_list2),"".join(input_list1))
			return True
		elif(t2_type == "INVALID"):
			# CASE 3 : INVALID syntax , unification not possible
			print "No , Unification is not Possible due to invalid syntax of Term 2 !","\n"
			return False
		else:
			# CASE 4 : constant and function
			print "No , Unification is not Possible as function cannot be assigned a constant value !","\n"
			return False
	elif(t1_type == "INVALID"):
		if(t2_type == "INVALID"):
			print "No , Unification not Possible due to invalid syntax of Term 1 and Term 2 !","\n"
			return False
		else:
			print "No , Unification not Possible due to invalid syntax of Term 1!","\n"
			return False
	else:
		# Term 1 is function
		if(t2_type == "VAR"):
			# CASE 1 : function and variable
			print "Yes , Unification Possible !","\n","".join(input_list2),"=","".join(input_list1)
			map_populate("".join(input_list2),"".join(input_list1))
			return True
		elif(t2_type == "CONST"):
			# CASE 2 : function and constant
			print "No , Unification is not Possible as function cannot be assigned a constant value !","\n"
			return False
		elif(t2_type == "INVALID"):
			# CASE 3 : INVALID syntax , unification not possible
			print "No , Unification is not Possible due to invalid syntax of Term 2!","\n"
			return False
		else:
			# CASE 4 : 2 functions
			print " Two functions encountered\n Checking cond1 : If two functors are the same"
			if(input_list1[0]!=input_list2[0]):
				print "No , Unification is not possible as the two functions have different functors/names\n"
				return False
			else:
				flg1 = True
				flg2 = True
				termlist1 = []
				templist1 = []
				termlist2 = []
				templist2 = []
				stck1 = []
				stck2 = []
				# For first function term
				for i1 in range(2,len(input_list1)):
					if(flg1==True):
						# Flag true means its either variable or constant
						if ((input_list1[i1].islower()) and (input_list1[i1+1]=='(')):
							flg1 = False
							templist1.append(input_list1[i1])								
						elif((input_list1[i1]==",") or (input_list1[i1]==")")):
							termlist1.append(templist1)
							templist1 = []
						else:
							templist1.append(input_list1[i1])
					else:
						# Flag false means its another function inside
						if(input_list1[i1]=="("):
							stck1.append("(")
						elif(input_list1[i1]==")"):
							tmp = stck1.pop()
						templist1.append(input_list1[i1])
						if(len(stck1)==0):
							flg1 = True
				print(termlist1)
				# For second function term
				for i2 in range(2,len(input_list2)):
					if(flg2==True):
						# Flag true means its either variable or constant
						if ((input_list2[i2].islower()) and (input_list2[i2+1]=='(')):
							flg2 = False
							templist2.append(input_list2[i2])								
						elif((input_list2[i2]==",") or (input_list2[i2]==")")):
							termlist2.append(templist2)
							templist2 = []
						else:
							templist2.append(input_list2[i2])
					else:
						# Flag false means its another function inside
						if(input_list2[i2]=="("):
							stck2.append("(")
						elif(input_list2[i2]==")"):
							tmp = stck2.pop()
						templist2.append(input_list2[i2])
						if(len(stck2)==0):
							flg2 = True
				print termlist2
				print "Checking cond2 : If two functions have the same number of arguments"
				if(len(termlist1)!=len(termlist2)):
					print "No , Unification is not possible as the two functions have different number of arguments \n"
					return False
				for j,k in zip(termlist1,termlist2):
					Condition = unify(j,k,Condition)
					if Condition == False :
						if(glb_err_flg):
							print "Overall unification attempt failed due to one or more mismatches ! Terminating !\n"
							glb_err_flg = False
						return False
				return True

"""
			MAIN PROGRAM LOGIC
"""

print "=========================Assignment 1===============================\n\n"
print "                         Submitted by : Amal Majeed                  \n\n"
print "Program Constraint : All variables, functions and constants are single characters and not strings.Any string(more than one alphanumeric together) will be treated as Invalid in this program.\n\n"

input_string1 = raw_input("Enter the first expression: ")
exp1 = input_string1.split(",")
first_term = input_string1
input_string2 = raw_input("Enter the second expression: ")
exp2 = input_string2.split(",")
second_term = input_string2
input_list1 = list(input_string1)
input_list2 = list(input_string2)

# Function redundancy error check - To see if a function name is used also as a constant
for i,j in enumerate(input_list1):
	if j.islower() and (i!=len(input_list1)-1) and input_list1[i+1]=="(":
		for x,y in enumerate(input_list1[i+2:len(input_list1)]):
			if(y == j):
				if ((x!=len(input_list1[i+2:len(input_list1)])-1) and (input_list1[i+2:len(input_list1)][x+1]!="(")):
					if glb_err_flg:
						print " Error , function name cannot be used as a separate constant !\n"
						glb_err_flg = False
		for x,y in enumerate(input_list2):
			if(y == j):
				if (x!=len(input_list2)-1) and input_list2[x+1]!="(":
					print "Error , function name cannot be used as a separate constant !\n"
					glb_err_flg = False
for i,j in enumerate(input_list2):
	if j.islower() and (i!=len(input_list2)-1) and input_list2[i+1]=="(":
		for x,y in enumerate(input_list2[i+2:len(input_list2)]):
			if(y == j):
				if((x!=len(input_list2[i+2:len(input_list2)])-1) and (input_list2[i+2:len(input_list2)][x+1]!="(")):
					if glb_err_flg:
						print "Error , function name cannot be used as a separate constant !\n"
						glb_err_flg = False
		for x,y in enumerate(input_list1):
			if(y == j):
				if (x!=len(input_list1)-1) and input_list1[x+1]!="(":
					print "Error , function name cannot be used as a separate constant !\n"
					glb_err_flg = False

if glb_err_flg:
	outp = unify(input_list1,input_list2,True)
	if(outp == False):
		if(glb_err_flg):
			print "Overall unification attempt failed due to one or more mismatches ! Terminating !\n"
	else:
		print "Success in unification Syntax Check !!\n"
		# Checking if there are any inconsistencies in variable mappings
		checkval = map_check()
		final = input_list2[:]
		if checkval:
			# Performing all transitive assignments through the existing variable mappings
			format_map()
			# Checking if there are any inconsistencies in variable mappings again after assignments
			checkval = map_check()
			if checkval:
				print "\nFinal Symbol Mappings : ",replace_map,"\n"
				for i in replace_map:
					final = ("".join(final)).replace(i,replace_map[i])
				print "Original Expression 1 : ","".join(input_list1),"\n"
				print "Original Expression 2 : ","".join(input_list2),"\n"
				print "Final Unified Expression : ",final,"\n"
