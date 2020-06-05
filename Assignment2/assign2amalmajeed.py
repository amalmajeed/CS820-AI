"""
							Assignment 2 : CSP solution algorithms with Arc Constraint
							Submitted By : First Name : Amal Majeed 
											Last Name : Mucheth Abdul Majeed
											Student Number : 200415928

"""

import math
import random



def create_rb(n,p,r,alpha,test=False):
	"""
	Function to create the RB instance / create the problem randomly

	"""
	print "\n***************	Generating RB instance 	***************\n"
	d = int(round(pow(n,alpha)))
	no_constraints = int(round(r*n*math.log(n)))
	no_incompatible = int(round(p*d**2))

	print "Domain size : ",d,"\n"
	print "No of Constraints : ",no_constraints,"\n"
	print "No of Incompatible tuples per pair : ",no_incompatible,"\n"
	var = ['X'+str(x) for x in range(0,n)]
	dom = [x for x in range(0,d)]
	print "vars ",var,"\n","domain ",dom,"\n"
	if(not test):
		print "\n***************	Creating Constraints	***************\n"
		cnst = []
		while(len(cnst)<no_constraints):
			x = random.choice(var)
			y = ""
			flg = True
			while(flg):
				y = random.choice(var)
				if(y!=x):
					flg = False
			temp = (x,y)
			if temp not in cnst:
				cnst.append(temp)
	else:
		cnst = [('X7','X1'),('X3','X0'),('X7','X3'),('X0','X6')]
	print "constraints ",cnst,"\n"
	if(not test):
		print "\n***************	Creating Incompatible tuples for each Constraint	***************\n"
		incomp = []
		while(len(incomp)<no_constraints):
			tmp = []
			while(len(tmp)<no_incompatible):
				a = random.choice(dom)
				b = -1
				flg = True
				while(flg):
					b = random.choice(dom)
					if(b!=a):
						flg = False
				t = (a,b)
				if t not in tmp:
					tmp.append(t)
			incomp.append(tmp)
	else:
		incomp = [[(1,5),(1,0),(6,4),(3,4),(1,2)],[(4,6),(2,0),(4,1),(5,4),(5,0)],[(0,1),(4,2),(0,2),(4,6),(5,1)],[(5,0),(2,5),(5,3),(1,2),(3,5)]]
	print "incompatible tuples for each constraint ",incomp,"\n"
	return var,dom,cnst,incomp


def num_pair_create():
	"""
	Function to create numeric tuples of constraint variable pairs , Eg : (X0,X1) - > (0,1)
	"""
	global cnst
	numpair = []
	for i in cnst:
		tmp =(int(i[0][-1:]),int(i[1][-1:]))
		numpair.append(tmp)
	return numpair


def REVISE(i,j,ind):
	"""
	Function to revise the domains of variables according to constraints of the problem
	"""
	global m_Dlist,incomp,Dlist
	revise = False
	#ind = find_cnst_index(i,j)
	for a in Dlist[i]:
		for b in Dlist[j]:
			#print "Checking (",a,",",b,")\n"
			if (a,b) in incomp[ind]:
				#print "Incompatible pair ",a,"\t",b,"\n"
				#print "m_Dlist value :",m_Dlist,"\n"
				if a in m_Dlist[i]:
					m_Dlist[i].remove(a)
					#print "m_Dlist value after removing ",a," : ",m_Dlist,"\n"
					#print "Dlist value after removing ",a," : ",Dlist,"\n"
				else:
					pass
				revise = True
	return revise

def AC3():
	"""
	Function to implement arc consistency algorithm AC3
	"""
	global var,dom,cnst,incomp,numpair
	Q = numpair[:]
	while(len(Q)!=0):
		#print "Entered AC3\tQ : ",Q,"\n"
		x = Q.pop()
		#print "First Element in AC3 ",x,"\n"
		if(REVISE(x[0],x[1],numpair.index(x))):
			for a in numpair:
				if((a[1]==x[0]) and (a[0]!=x[1])):
					if a not in numpair:
						Q.append(a)
					else:
						pass

def emptyset(e_set):
	return (len(e_set)==0)


def ac3bt(i,instantiated):
	"""
		Function to do the logic of Backtracking
	"""
	global m_Dlist,cnst,incomp,numpair
	Q = []
	for j in numpair:
		if((j[1] in instantiated) and (j[0]==i)):
			Q.append(j)
	notconsistent = False
	while((len(Q)!=0) and (not notconsistent)):
		x = Q.pop()
		notconsistent = REVISE(x[0],x[1],numpair.index(x))
	return (not notconsistent)

def ac3fc(i,future):
	"""
		Function to do the logic of Forward Checking
	"""
	global m_Dlist,cnst,incomp,numpair
	Q = []
	for j in numpair:
		if((j[0] in future) and (j[1]==i)):
			Q.append(j)
	notconsistent = False
	while((len(Q)!=0) and (not notconsistent)):
		x = Q.pop()
		if REVISE(x[0],x[1],numpair.index(x)):
			notconsistent = emptyset(m_Dlist[x[1]])
	return (not notconsistent)

def ac3fla(i,future):
	"""
		Function to do the logic of Full Look ahead
	"""
	global m_Dlist,cnst,incomp,numpair
	Q = []
	for j in numpair:
		if(((j[0] in future) or (j[0]==i)) and((j[1] in future) or (j[1]==i))):
			Q.append(j)
	notconsistent = False
	while((len(Q)!=0) and (not notconsistent)):
		x = Q.pop()
		if REVISE(x[0],x[1],numpair.index(x)):
			for a in numpair:
				if((a[1]==x[0]) and (a[0]!=x[1])):
					if a not in numpair:
						Q.append(a)
					else:
						pass
			notconsistent = emptyset(m_Dlist[x[1]])
	return (not notconsistent)


def backtracking():
	"""
		Entry logic for backtracking , main logic in function ac3bt
	"""
	global m_Dlist,cnst,incomp,numpair
	failflg = False
	moves = []
	instantiated = []
	flg = False
	r=-1
	while((flg==False) and (r <= len(m_Dlist[0]))):
		r = r+1
		flg = True
		for k in numpair:
			if k[0]==0:
				for l in cnst[numpair.index(k)]:
					if l[0]==m_Dlist[0][r]:
						flg = False
	if(r<=len(m_Dlist[0])):
		move = random.choice(m_Dlist[0])
		moves.append(move)
		print "Move made for Var X0 : ",move,"\n"
		instantiated.append(0)
	else:
		failflg = True
	if(not failflg):
		for i in range(1,n):
			if(not ac3bt(i,instantiated)):
				if(len(m_Dlist[i])==0):
					failflg = True
				else:
					r=0
					#move = m_Dlist[i][r]
					move = random.choice(m_Dlist[i])
					print "Move made for Var X",i," : ",move,"\n"
					moves.append(move)
					instantiated.append(i)
			else:
				move = random.choice(m_Dlist[i])
				print "Move made for Var X",i," : ",move,"\n"
				moves.append(move)
				instantiated.append(i)
	if(failflg):
		print "The problem is inconsistent after backtrack approach. It is unsolvable !\n"
	else:
		print "Solved !\n Moves made : ",moves,"\n"

def forwardchecking():
	"""
		Entry logic for forwardchecking , main logic in function ac3fc 
	"""
	global var,m_Dlist,cnst,incomp,numpair
	moves = []
	future = [i for i in range(0,len(var))]
	failflg = False
	i = 0
	while((len(future)>0) and (not failflg)):
		#print "Future now : ",future,"\n"
		curr = future.pop(i)
		if(len(future)==0):
			if(len(m_Dlist[curr])==0):
				print "The problem is inconsistent after forward checking. It is unsolvable !\n"
				failflg = True
			else:
				#move = m_Dlist[curr][0]
				move = random.choice(m_Dlist[i])
				if(ac3fc(curr,future)):
					moves.append(move)
				else:
					print "The problem is inconsistent after forward checking. It is unsolvable !\n"
					failflg = True	
		else:
			#move = m_Dlist[curr][0]
			move = random.choice(m_Dlist[i])
			if(ac3fc(curr,future)):
				moves.append(move)
			else:
				print "The problem is inconsistent after forward checking. It is unsolvable !\n"
				failflg = True
	if(not failflg):
		print "Solved !\n Moves made : ",moves,"\n"

def fulllookahead():
	"""
		Entry logic for fulllookahead , main logic in function ac3fla 
	"""
	global var,m_Dlist,cnst,incomp,numpair
	moves = []
	future = [i for i in range(0,len(var))]
	failflg = False
	i = 0
	while((len(future)>0) and (not failflg)):
		print "Future now : ",future,"\n"
		curr = future.pop(i)
		if(len(future)==0):
			if(len(m_Dlist[curr])==0):
				print "The problem is inconsistent after forward checking. It is unsolvable !\n"
				failflg = True
			else:
				move = random.choice(m_Dlist[curr])
				if(ac3fla(curr,future)):
					moves.append(move)
				else:
					print "The problem is inconsistent after forward checking. It is unsolvable !\n"
					failflg = True	
		else:
			move = random.choice(m_Dlist[curr])
			if(ac3fla(curr,future)):
				moves.append(move)
			else:
				print "The problem is inconsistent after forward checking. It is unsolvable !\n"
				failflg = True
	if(not failflg):
		print "Solved !\n Moves made : ",moves,"\n"




###############        MAIN LOGIC		



decision = raw_input("Do you want to run a randomly generated problem (Press 'y') ? / run a known example problem that is consistent (Press 'n') ?  :")
incons = False
if(decision=='y'):
	n = input("Enter the number of variables : ")
	p = input("Enter the value of constraint tightness ( 0 < p < 1 ) : ")
	r = input("Enter the constant value r ( r < 0 ) : ")
	alpha = input("Enter the constant value alpha ( alpha < 1 ) : ")
	var,dom,cnst,incomp = create_rb(n,p,r,alpha,False)
else:

	n = 9
	p = 0.11
	r = 0.2
	alpha = 0.9
	print "Values assigned from previously observed example:\nn = 9\np = 0.11\nr = 0.2\nalpha = 0.9\n "
	var,dom,cnst,incomp = create_rb(n,p,r,alpha,True)
numpair = num_pair_create()
# List of domains of each variables in var list
Dlist = [dom[:] for i in range(0,n)]
# Creating another modifiable copy of the above domain list
m_Dlist = [dom[:] for i in range(0,n)]

ch1 = raw_input(" Do you want to perform arc consistency ( AC3 ) on the problem (y/n) ? :")
ch2 = int(raw_input(" Which algorithm do you want to use to solve if problem is consistent/solvable ?(1/2/3) :\n\t1.Backtracking\n\t2.Forward Checking\n\t3.Full lookahead\t:"))
ch1 = ch1.lower()

if(ch1 == 'y'):
	print "Before ac3 : ",m_Dlist,"\n"
	AC3()
	print "After ac3 : ",m_Dlist,"\n"
	for i in m_Dlist:
		if len(i) == 0:
			incons = True
	if(incons):
		print "After performing Arc Consistency on the randomly generated problem one or many of the revised domains are empty , which means the problem is arc inconsistent or unsolvable !"
	else:
		if ch2 == 1:
			backtracking()
		elif ch2 == 2:
			forwardchecking()
		elif ch2 == 3:
			fulllookahead()
		else:
			print "Invalid Option !\n"
else:
	if ch2 == 1:
		backtracking()
	elif ch2 == 2:
		forwardchecking()
	elif ch2 == 3:
		fulllookahead()
	else:
		print "Invalid Option !\n"

