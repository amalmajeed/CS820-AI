"""
							Assignment 3 : CSP-CP Net solution algorithms with Arc Constraint
							Submitted By : First Name : Amal Majeed 
											Last Name : Mucheth Abdul Majeed
											Student Number : 200415928

"""

import math
import random
import itertools


def create_rb(n,p,r,alpha,np,test=False):
	"""
	Function to create the RB instance / create the problem randomly
	"""
	print "\n***************	Generating CSP instance 	***************\n"
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
	print "incompatible tuples for each constraint ",incomp,"\n"
	print "\n***************	Generating CP-Net instance 	***************\n"
	parentlist = []
	if(not test):
		plist = [[j for j in range(0,i)] for i in range(0,n)]
		for i in plist:
			if(len(i)<=np):
				parentlist.append(i)
			else:
				t = []
				while(len(t)<np):
					tmp = random.choice(i)
					if(tmp not in t):
						t.append(tmp)
				parentlist.append(t)
		n_table = [{} for i in range(0,len(parentlist))]   ## Node table for order of values for parent combos
		for j,i in enumerate(parentlist):
			indices = list(itertools.product(dom,repeat=len(parentlist[j])))
			for k in indices:
				tmp = dom[:]
				random.shuffle(tmp)  ## Generating random order
				n_table[j][k]=tmp
			#print "Indices for ",i ," : ",indices,"\n"
		print "Final parent list : ",parentlist,"\n"
		print "Final node table : ",n_table,"\n"
	return var,dom,cnst,incomp,parentlist,n_table


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

def updatentable():
	global n,var,dom,cnst,incomp,numpair,m_Dlist,incomp,Dlist,parentlist,n_table
	print "Updating the CPT Table based on changed domain list after AC3\n"
	for k,i in enumerate(m_Dlist):
		rx = [x for x in range(0,len(dom))]
		for j in i:
			rx.remove(j)
		for j in n_table[k]:
			for l in rx:
				n_table[k][j].remove(l)


def nextvalue(nd,head,i_val):
	global n,var,dom,cnst,incomp,numpair,m_Dlist,incomp,Dlist,parentlist,n_table,order_list
	## Note , this function performs Consistency check of nextvalue assignment as well, so there is no separate function for 'ISCONSISTENT' like in question paper
	if head == None:
		# Root node
		npconf = True
		# i_val is to change roots value for each pareto optimal solution , otherwise the same solution will be generated everytime
		i = i_val
		print "Finding optimal value for root without violating constraints\n"
		while( npconf and (i<len(n_table[0][()]))):
			for ind1,j in enumerate(numpair):
				con = False
				if 0 in j:
					# We check the position of the root node in random constraint if LHS/1st element or RHS/2nd element
					lhs = True
					if j[1] == 0:
						lhs = False
					for k in incomp[ind1]:
						if lhs:
							if(n_table[0][()][i] == k[0]):
								con = True
						# else:
						# 	if(n_table[0][()][i] == k[1]):
						# 		con = True
				if(con):
					i=i+1
				else:
					npconf = False 
		if(not npconf):
			return True,n_table[0][()][i]
		if(i>=len(n_table[0][()])):
			print "Based on the constraints no move can be made for 0 ! Inconsistency detected ! \n"
			return False,-1
	else:
		# Non Root Node
		## Get parents
		parents = parentlist[nd]
		assignlst = head.keys()
		p_check = True
		for i in parents:
			if i not in assignlst:
				p_check = False
		if not p_check:
			## This condition should not occur because the order of assignment in 0,1,2,.... and the parents of Xi are from X0,X1,...Xi-1
			print "The current node under consideration has an Unassigned parent ! Aborting "
		else:
			tmp = []
			for i in parents:
				tmp.append(head[i])
			print "Parent value list for : ",nd," = ",tmp,"\n"
			tmp = tuple(tmp)
			# List of precedence of values of current node based on assigned values of parents
			nd_orderlist = n_table[nd][tmp]
			print " Orderlist for ",nd," : ",nd_orderlist,"\n"
			npconf = True
			i = 0
			print "Finding optimal value for node ",nd," without violating constraints\n"
			while( npconf and (i<len(nd_orderlist))):
				for ind1,j in enumerate(numpair):
					con = False
					if nd in j:
						# We check the position of the root node in random constraint if LHS/1st element or RHS/2nd element
						lhs = True
						if j[1] == nd:
							lhs = False
						for k in incomp[ind1]:
							# Here we check if the current node is in an incompatible tuple and if any parent that has already been assigned a conflicting value
							if lhs:
								if(nd_orderlist[i] == k[0]):
									if(j[1] in head.keys()):
										if(head[j[1]] == k[1]):
											con = True
							else:
								if(nd_orderlist[i] == k[1]):
									if(j[0] in head.keys()):
										if(head[j[0]] == k[0]):
											con = True
					if(con):
						i=i+1
					else:
						npconf = False 
			if(not npconf):
				return True,nd_orderlist[i]
			if(i>=len(n_table[0][()])):
				print "Based on the constraints no move can be made for ",nd," ! Inconsistency detected ! \n"
				return False,-1


def dominance(s,nod):
	global var,dom,cnst,incomp,numpair,m_Dlist,incomp,Dlist,parentlist,n_table,order_list,k,n
	diff_cnt = 0
	for i in range(0,n):
		if not (s[i] == nod[i]):
			diff_cnt += 1
	if(diff_cnt == 0):
		# Which means s == nod , or the optimal solution is already considered
		return 0,True
	elif(diff_cnt == 1):
		# Which means an existing solution 's' by flipping just one variable becomes 'nod' and hence nod is dominated by s
		return 1,True
	else:
		return 2,False


def backtracking():
	"""
	Main logic for backtracking
	"""
	global var,dom,cnst,incomp,numpair,m_Dlist,incomp,Dlist,parentlist,n_table,order_list,k,n
	S = [] # set of solutions
	# order list contains the order in which the variables are assigned , it is numerical ascending order by default
	root = order_list[0]
	# Order index is used to keep track of variable assignments , at 0 means its at root , 1 means X1 , etc
	order_index = 0
	endsearch = False
	isconsistent = False
	isconsistent,bestval0 = nextvalue(root,None,0)
	print "The optimal value for root without constraint violation is: ",bestval0,"\n"
	fringe = [{0:bestval0}] # Assigned best value to root
	mv0 = 0
	while((len(S)<k) and (endsearch == False)):
		nod = fringe.pop(0) # popping first item in fringe
		status = 2
		if isconsistent:
			if len(nod)==n:
				dcheck = False
				for s in S:
					status,dm = dominance(s,nod)
					if dm:
						print nod," is dominated by an existing solution : ",s,"\n"
						print "Status : ",status,"\n"
						if(status == 0):
							dcheck = True
							while(dm):
								for temporary in range(0,2):
									rnd_nd = random.choice(range(0,n))
									old_val = nod[rnd_nd]
									if rnd_nd == 0:
										old_loc = n_table[rnd_nd][()].index(old_val)
										if(old_loc == (len(n_table[rnd_nd][()])-1)):
											print "Exhausted search space for the flip variable ",rnd_nd," !\n"
										else:
											nod[rnd_nd] = n_table[rnd_nd][()][old_loc+1]
									else:
										plst = parentlist[rnd_nd]
										pval = tuple([nod[i] for i in plst])
										old_loc = n_table[rnd_nd][pval].index(old_val)
										if(old_loc == (len(n_table[rnd_nd][pval])-1)):
											print "Exhausted search space for the flip variable ",rnd_nd," !\n"
										else:
											nod[rnd_nd] = n_table[rnd_nd][pval][old_loc+1]
								status,dm = dominance(s,nod)
							dcheck = False		
						if(status == 1):
							dcheck = True
							while(dm):
								rnd_nd = random.choice(range(0,n))
								old_val = nod[rnd_nd]
								if rnd_nd == 0:
									old_loc = n_table[rnd_nd][()].index(old_val)
									if(old_loc == (len(n_table[rnd_nd][()])-1)):
										print "Exhausted search space for the flip variable ",rnd_nd," !\n"
									else:
										nod[rnd_nd] = n_table[rnd_nd][()][old_loc+1]
								else:
									plst = parentlist[rnd_nd]
									pval = tuple([nod[i] for i in plst])
									old_loc = n_table[rnd_nd][pval].index(old_val)
									if(old_loc == (len(n_table[rnd_nd][pval])-1)):
										print "Exhausted search space for the flip variable ",rnd_nd," !\n"
									else:
										nod[rnd_nd] = n_table[rnd_nd][pval][old_loc+1]
								status,dm = dominance(s,nod)
							dcheck = False
				if(not dcheck):
					S.append(nod)
					print "S currently :",S,"\n"
					if(len(S)<k):
						isconsistent,bestval0 = nextvalue(root,None,len(S))
						print "The optimal value for root without constraint violation is: ",bestval0,"\n"
						fringe = [{0:bestval0}]
						print "Fringe for next pareto optimal solution starts as : ",fringe,"\n"
						order_index = 0
			else:
				# Getting the NEXTVARIABLE from the order_list to assign a value
				order_index += 1
				print "Current Order Index : ",order_index,"\n"
				if(order_index<n):
					print "Order list / order_list[order_index] before nextval :",order_list[order_index]," and nod before nextval :",nod,"\n"
					isconsistent,bestval = nextvalue(order_list[order_index],nod,0)
					nod[order_list[order_index]] = bestval
					print "Fringe Before :",fringe,"\n"
					fringe.append(nod)
					print "Fringe After :",fringe,"\n"
				else:
					print "List exhausted and All Values have been assigned if constraints allowed !"
		if(status == 0):
			pass
		if(status == 1):
			pass
	return S[:k]

def fcprop(curr,future,nod):
	"""
	Propagation logic for Forward checking
	"""
	global var,dom,cnst,incomp,numpair,m_Dlist,incomp,Dlist,parentlist,n_table,order_list,n
	for i in future:
		for j,k in enumerate(numpair):
			if((order_list[i] in k) and (order_list[curr] in k)):
				lhs = True
				if(k[0]==order_list[i]):
					lhs = False
				for l in incomp[j]:
					if(lhs):
						if(l[0]==nod[curr]):
							for x in ntable[i]:
								if(l[1] in ntable[i][x]):
									ntable[i][x].remove(l[1])


def forwardchecking():
	"""
	THIS IS NOT THE MAIN LOGIC DIFFERENCE OF FC , difference is in propagation , check "fcprop"
	"""
	global var,dom,cnst,incomp,numpair,m_Dlist,incomp,Dlist,parentlist,n_table,order_list,k,n
	S = [] # set of solutions
	# order list contains the order in which the variables are assigned , it is numerical ascending order by default
	root = order_list[0]
	# Order index is used to keep track of variable assignments , at 0 means its at root , 1 means X1 , etc
	order_index = 0
	endsearch = False
	isconsistent = False
	isconsistent,bestval0 = nextvalue(root,None,0)
	print "The optimal value for root without constraint violation is: ",bestval0,"\n"
	fringe = [{0:bestval0}] # Assigned best value to root
	mv0 = 0
	while((len(S)<k) and (endsearch == False) and (len(fringe)>0)):
		nod = fringe.pop(0) # popping first item in fringe
		status = 2
		if isconsistent:
			if len(nod)==n:
				dcheck = False
				for s in S:
					status,dm = dominance(s,nod)
					if dm:
						print nod," is dominated by an existing solution : ",s,"\n"
						print "Status : ",status,"\n"
						if(status == 0):
							dcheck = True
							while(dm):
								for temporary in range(0,2):
									rnd_nd = random.choice(range(0,n))
									old_val = nod[rnd_nd]
									if rnd_nd == 0:
										old_loc = n_table[rnd_nd][()].index(old_val)
										if(old_loc == (len(n_table[rnd_nd][()])-1)):
											print "Exhausted search space for the flip variable ",rnd_nd," !\n"
										else:
											nod[rnd_nd] = n_table[rnd_nd][()][old_loc+1]
									else:
										plst = parentlist[rnd_nd]
										pval = tuple([nod[i] for i in plst])
										old_loc = n_table[rnd_nd][pval].index(old_val)
										if(old_loc == (len(n_table[rnd_nd][pval])-1)):
											print "Exhausted search space for the flip variable ",rnd_nd," !\n"
										else:
											nod[rnd_nd] = n_table[rnd_nd][pval][old_loc+1]
								status,dm = dominance(s,nod)
							dcheck = False		
						if(status == 1):
							dcheck = True
							while(dm):
								rnd_nd = random.choice(range(0,n))
								old_val = nod[rnd_nd]
								if rnd_nd == 0:
									old_loc = n_table[rnd_nd][()].index(old_val)
									if(old_loc == (len(n_table[rnd_nd][()])-1)):
										print "Exhausted search space for the flip variable ",rnd_nd," !\n"
									else:
										nod[rnd_nd] = n_table[rnd_nd][()][old_loc+1]
								else:
									plst = parentlist[rnd_nd]
									pval = tuple([nod[i] for i in plst])
									old_loc = n_table[rnd_nd][pval].index(old_val)
									if(old_loc == (len(n_table[rnd_nd][pval])-1)):
										print "Exhausted search space for the flip variable ",rnd_nd," !\n"
									else:
										nod[rnd_nd] = n_table[rnd_nd][pval][old_loc+1]
								status,dm = dominance(s,nod)
							dcheck = False
				if(not dcheck):
					S.append(nod)
					print "S currently :",S,"\n"
					if(len(S)<k):
						isconsistent,bestval0 = nextvalue(root,None,len(S))
						if(isconsistent):
							print "The optimal value for root without constraint violation is: ",bestval0,"\n"
							fringe = [{0:bestval0}]
							print "Fringe for next pareto optimal solution starts as : ",fringe,"\n"
						order_index = 0
			else:
				## PROPAGATE LOGIC BEGINS
				if(order_index<(n-1)):
					curr = order_index
					future = order_list[order_index+1:]
					fcprop(curr,future,nod)
				## PROPAGATE LOGIC ENDS
				# Getting the NEXTVARIABLE from the order_list to assign a value
				order_index += 1
				print "Current Order Index : ",order_index,"\n"
				if(order_index<n):
					print "Order list / order_list[order_index] before nextval :",order_list[order_index]," and nod before nextval :",nod,"\n"
					isconsistent,bestval = nextvalue(order_list[order_index],nod,0)
					if(isconsistent):
						nod[order_list[order_index]] = bestval
						print "Fringe Before :",fringe,"\n"
						fringe.append(nod)
						print "Fringe After :",fringe,"\n"
				else:
					print "List exhausted and All Values have been assigned if constraints allowed !"
		# if(status == 0):
		# 	pass
		# if(status == 1):
		# 	pass
	return S[:k]

def flaprop(curr,future,nod):
	"""
	Propagation logic for Full Look Ahead
	"""
	global var,dom,cnst,incomp,numpair,m_Dlist,incomp,Dlist,parentlist,n_table,order_list,n
	for i in future:
		for j,k in enumerate(numpair):
			if(order_list[i] in k):
				if(order_list[curr] in k):
					lhs = True
					if(k[0]==order_list[i]):
						lhs = False
					for l in incomp[j]:
						if(lhs):
							if(l[0]==nod[curr]):
								for x in ntable[i]:
									if(l[1] in ntable[i][x]):
										ntable[i][x].remove(l[1])
				else:
					lhs = True
					if(k[0]==order_list[i]):
						lhs = False
					if(lhs):
						m = k[0]
						if(m in future):
							plist = []
							for y in parentlist[i]:
								plist.append(nod[y])
							plist = tuple(plist)
							for l in incomp[j]:
								if l[1] == n_table[i][plist][0]:
									for x in ntable[m]:
										if(l[0] in ntable[m][x]):
											ntable[m][x].remove(l[0])
					else:
						m = k[1]
						if(m in future):
							plist = []
							for y in parentlist[i]:
								plist.append(nod[y])
							plist = tuple(plist)
							for l in incomp[j]:
								if l[0] == n_table[i][plist][0]:
									for x in ntable[m]:
										if(l[1] in ntable[m][x]):
											ntable[m][x].remove(l[1])




def fulllookahead():
	"""
	THIS IS NOT THE MAIN LOGIC DIFFERENCE OF FLA , difference is in propagation , check "flaprop"
	"""
	global var,dom,cnst,incomp,numpair,m_Dlist,incomp,Dlist,parentlist,n_table,order_list,k,n
	S = [] # set of solutions
	# order list contains the order in which the variables are assigned , it is numerical ascending order by default
	root = order_list[0]
	# Order index is used to keep track of variable assignments , at 0 means its at root , 1 means X1 , etc
	order_index = 0
	endsearch = False
	isconsistent = False
	isconsistent,bestval0 = nextvalue(root,None,0)
	print "The optimal value for root without constraint violation is: ",bestval0,"\n"
	fringe = [{0:bestval0}] # Assigned best value to root
	mv0 = 0
	while((len(S)<k) and (endsearch == False) and (len(fringe)>0)):
		nod = fringe.pop(0) # popping first item in fringe
		status = 2
		if isconsistent:
			if len(nod)==n:
				dcheck = False
				for s in S:
					status,dm = dominance(s,nod)
					if dm:
						print nod," is dominated by an existing solution : ",s,"\n"
						print "Status : ",status,"\n"
						if(status == 0):
							dcheck = True
							while(dm):
								for temporary in range(0,2):
									rnd_nd = random.choice(range(0,n))
									old_val = nod[rnd_nd]
									if rnd_nd == 0:
										old_loc = n_table[rnd_nd][()].index(old_val)
										if(old_loc == (len(n_table[rnd_nd][()])-1)):
											print "Exhausted search space for the flip variable ",rnd_nd," !\n"
										else:
											nod[rnd_nd] = n_table[rnd_nd][()][old_loc+1]
									else:
										plst = parentlist[rnd_nd]
										pval = tuple([nod[i] for i in plst])
										old_loc = n_table[rnd_nd][pval].index(old_val)
										if(old_loc == (len(n_table[rnd_nd][pval])-1)):
											print "Exhausted search space for the flip variable ",rnd_nd," !\n"
										else:
											nod[rnd_nd] = n_table[rnd_nd][pval][old_loc+1]
								status,dm = dominance(s,nod)
							dcheck = False		
						if(status == 1):
							dcheck = True
							while(dm):
								rnd_nd = random.choice(range(0,n))
								old_val = nod[rnd_nd]
								if rnd_nd == 0:
									old_loc = n_table[rnd_nd][()].index(old_val)
									if(old_loc == (len(n_table[rnd_nd][()])-1)):
										print "Exhausted search space for the flip variable ",rnd_nd," !\n"
									else:
										nod[rnd_nd] = n_table[rnd_nd][()][old_loc+1]
								else:
									plst = parentlist[rnd_nd]
									pval = tuple([nod[i] for i in plst])
									old_loc = n_table[rnd_nd][pval].index(old_val)
									if(old_loc == (len(n_table[rnd_nd][pval])-1)):
										print "Exhausted search space for the flip variable ",rnd_nd," !\n"
									else:
										nod[rnd_nd] = n_table[rnd_nd][pval][old_loc+1]
								status,dm = dominance(s,nod)
							dcheck = False
				if(not dcheck):
					S.append(nod)
					print "S currently :",S,"\n"
					if(len(S)<k):
						isconsistent,bestval0 = nextvalue(root,None,len(S))
						if(isconsistent):
							print "The optimal value for root without constraint violation is: ",bestval0,"\n"
							fringe = [{0:bestval0}]
							print "Fringe for next pareto optimal solution starts as : ",fringe,"\n"
						order_index = 0
			else:
				## PROPAGATE LOGIC BEGINS
				if(order_index<(n-1)):
					curr = order_index
					future = order_list[order_index+1:]
					fcprop(curr,future,nod)
				## PROPAGATE LOGIC ENDS
				# Getting the NEXTVARIABLE from the order_list to assign a value
				order_index += 1
				print "Current Order Index : ",order_index,"\n"
				if(order_index<n):
					print "Order list / order_list[order_index] before nextval :",order_list[order_index]," and nod before nextval :",nod,"\n"
					isconsistent,bestval = nextvalue(order_list[order_index],nod,0)
					if(isconsistent):
						nod[order_list[order_index]] = bestval
						print "Fringe Before :",fringe,"\n"
						fringe.append(nod)
						print "Fringe After :",fringe,"\n"
				else:
					print "List exhausted and All Values have been assigned if constraints allowed !"
		# if(status == 0):
		# 	pass
		# if(status == 1):
		# 	pass
	return S[:k]


def formattedOut(final):
	print "\n\n\n The Final Pareto sets are the following ( formatted output )\n"
	count = 1
	for i in final:
		print "Set ",count,"\n"
		for key in i:
			print "X",key,"  = ",i[key],"\n"
		count+=1

###############        				MAIN LOGIC					#######################

decision = "y"
incons = False
var = []
dom = []
cnst = []
incomp = []
parentlist = []
n_table = []
k=0
np = 0
if(decision=='y'):
	n = input("Enter the number of variables (n) : ")
	p = input("Enter the value of constraint tightness ( 0 < p < 1 ) : ")
	r = input("Enter the constant value r ( r < 0 ) : ")
	alpha = input("Enter the constant value alpha ( alpha < 1 ) : ")
	np = input("Enter the maximum number of parents for each node Xi (np) : ")
	var,dom,cnst,incomp,parentlist,n_table = create_rb(n,p,r,alpha,np,False)
	k = input("Enter the maximum number of Pareto optimal solutions( MUST BE LESS THAN OR EQUAL TO DOMAIN SIZE !) (k) : ")
numpair = num_pair_create()
# List of domains of each variables in var list
Dlist = [dom[:] for i in range(0,n)]
# Creating another modifiable copy of the above domain list
m_Dlist = [dom[:] for i in range(0,n)]
order_list = [i for i in range(0,n)]

ch1 = raw_input(" Do you want to perform arc consistency ( AC3 ) on the problem (y/n) ? :")
ch2 = int(raw_input(" Which algorithm do you want to use to solve if problem is consistent/solvable ?(1/2/3) :\n\t1.Backtracking\n\t2.Forward Checking\n\t3.Full lookahead\t:"))
ch1 = ch1.lower()

if(ch1 == 'y'):
	print " Domain list of variables before ac3 (in order X0,X1,X2.....): ",m_Dlist,"\n"
	AC3()
	print " Domain list of variables after ac3 (in order X0,X1,X2.....) : ",m_Dlist,"\n"
	updatentable()
	print "After updatentable :",n_table,"\n"
	for i in m_Dlist:
		if len(i) == 0:
			incons = True
	if(incons):
		print "After performing Arc Consistency on the randomly generated problem one or many of the revised domains are empty , which means the problem is arc inconsistent or unsolvable !"
	else:
		if ch2 == 1:
			final = backtracking()
			print "\n\n\nFinal Pareto set is : ",final,"\n"
			formattedOut(final)
		elif ch2 == 2:
			final = forwardchecking()
			print "\n\n\nFinal Pareto set is : ",final,"\n"
			formattedOut(final)
		elif ch2 == 3:
			final = fulllookahead()
			print "\n\n\nFinal Pareto set is : ",final,"\n"
			formattedOut(final)
		else:
			print "\n\n\nInvalid Option !\n"
else:
	if ch2 == 1:
		final = backtracking()
		print "\n\n\nFinal Pareto set is : ",final,"\n"
		formattedOut(final)
	elif ch2 == 2:
		final = forwardchecking()
		print "\n\n\nFinal Pareto set is : ",final,"\n"
		formattedOut(final)
	elif ch2 == 3:
		final = fulllookahead()
		print "\n\n\nFinal Pareto set is : ",final,"\n"
		formattedOut(final)
	else:
		print "\n\n\nInvalid Option !\n"