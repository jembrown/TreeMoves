
--------Fake Data-----------------------------------------------------------
#import data and instantiate tree

goo="(X:2,((Y:3,Z:1):2,W:8):6)"
Tim = Tree(goo)
a = Tim.root.children[1]
'((Y:3,Z:1):2,W:8)'
b = a.children[0]
'(Y:3,Z:1)'
b.children = []
Tim.root.children[1].children[0].children
'[]'
#this does erase the original tree instance of these nodes
goo="(X:2,((Y:3,Z:1):2,W:8):6)"
Tim = Tree(goo)
a = Tim.root.children[1]
b = a.children[0]
a.children[0] == b
True
a.children = []
b still exists, but W does not




#Tim_tips = Tim.printTermNodes(Tim.root)
g = pick_goal(Tim,Tim_tips)
x = pick_start(Tim,g)
#tests
x=Tim_tips[0]
x.name
y=Tim_tips[1].
y.name
Tim.edge_length(x)

-----------------------------------------------------------


# pick random tip in tree. traverse backwards to goal. or start
def pick_start(tree, goal, n=tree.root):
	#set root as start node
	n=tree.root
	#start at root, find children until there are no more children.
	while n.children !=[]:
		n = where_my_child(n)[random.choice([0,1])]
		print("where kids: "+str(n.name))
	print("first n: "+str(n.name))
	#find a node based on the goal
	start = traverse_nodes(n,goal)
	print("first start: "+str(start))
	#if you get to the root
	while start == 0:
		#pick another tip, start at root
		while n.children !=[]:
			n = where_my_child(tree.root)[random.choice([0,1])]
		print("n : "+str(n.name))
		#pick another random node based on goal
		start=traverse_nodes(n,goal)
		#print("start: "+str(start))
	#print("p: "+str(p.name))
	return start


----NNI moves-------------------------------------------------------------
loop = "true"
while loop == "true":
	#start with root
	c1=Sim.root
	#find a terminal node (randomly) and assign to c1
	while c1.children !=[]:
		c1 = where_my_child(c1)[random.choice([0,1])]
	#print c1.name
	#for both childrens of the parent of c1, assign name to c2
	for c in c1.parent.children:
		if c != c1:
			c2 =c
	br1, br2 = c1.brl, c2.brl
	#only works if c2 has grand children. Can't NNI on sister taxa only.
	if c2.children != []:
		gc1, gc2 = where_my_child(c2)	
		br3, br4 = gc1.brl, gc2.brl
		loop = "false"
#store branch lengths for decendants of start nodes		
p = c1.parent
#remove all children
p.children = []
#this is the node to attach grandchildren to
new_node = Node("new",parent=p)
#give it same br as before
new_node.brl = br2
#append one of the two grandchildren to p. append other one to new node
adopt=random.choice([1,2])
if adopt == 1:
	p.children.append(gc1)
	new_node.children.append(gc2)
elif adopt ==2:
	p.children.append(gc2)
	new_node.children.append(gc1)
p.children.append(new_node)
#add c1 to new node
new_node.children.append(c1)
--------------------------------------------------------

		# pick random tip in tree. traverse backwards to goal. or start function over
def pick_start(tree, goal, n=0):
	#set root as start node
	if n == 0:
		n=tree.root
	#if not at tip, traverse until you hit a tip
	while n.children !=[]:
		n = where_my_child(n)[random.choice([0,1])]
		print("where kids: "+str(n.name))
	print("n: "+str(n.name))
	#begin at tip and stop at goal or root
	start = traverse_nodes(n,goal)
	#if you get to the root, recursion
	while start == 0:
		#recursive
		print("hit root -> recursion")
		return pick_start(tree,goal,tree.root)
	print("start: "+str(start.name))
	return start
----------------------------------------------------------------------------------------------
#makes a list of all children of a given node. 
def where_my_child(parent):
	children = []
	for child in parent.children:
		children.append(child)
	return children

----------------------------------------------------------------------------------------------
def random_tip(tree, tip_list):
	### make into choose random tip funciton
	#tip_list = tree.list_term_nodes(tree.root) #add this back after debugging list_term_nodes
	random_tip = random.choice(tip_list)
	return random_tip


#pick a random goal to start NNI from.	
def pick_goal(tree, tip_list):
	# get list of tips as node objects. will put this back in when i fix bug.
	#tip_list = tree.printTermNodes(tree.root)
	edge_list = []
	# get list of all tip to root edges
	for node in tip_list:
		edge_list.append(tree.inv_edge_len(node))
	long_edge = max(edge_list)
	#calculate goal, random number between 0 and longest edge.
	g = random.uniform(0,long_edge)
	print("max length: "+str(long_edge))
	print("goal: "+str(g))
	return g


#traverse nodes until you reach goal. If root is reached before goal. Return 0.
def traverse_nodes(node,goal):
	print("traverse node 1: "+str(node.name))
	if node.brl == 0:
		return node.brl
	else:
		#get inverse of branch length add back in after rewriting br macx function to be inverse
		inv_br=1/float(node.brl)
		#subtract from goal
		goal -= inv_br
		#print("new goal:"+str(goal))
		#if goal is less than zero, return p as node you will start NNI with. 
		if goal <= 0:
			end = node
			#print("start: "+str(start.name))
			return end
		#if goal is still above 0, go to parent node and run program again
		elif goal > 0:
			p = node.parent
			#print("new parent: "+str(p.name))
			return traverse_nodes(p,goal)

----------------------------------------------------------------------------------------------
def random_tip(tree, tip_list):
	### make into choose random tip funciton
	#tip_list = tree.list_term_nodes(tree.root) #add this back after debugging list_term_nodes
	random_tip = random.choice(tip_list)
	return random_tip


#pick a random goal to start NNI from.	
def pick_goal(tree, tip_list):
	# get list of tips as node objects. will put this back in when i fix bug.
	#tip_list = tree.printTermNodes(tree.root)
	edge_list = []
	# get list of all tip to root edges
	for node in tip_list:
		edge_list.append(tree.inv_edge_len(node))
	long_edge = max(edge_list)
	#calculate goal, random number between 0 and longest edge.
	g = random.uniform(0,long_edge)
	print("max length: "+str(long_edge))
	print("goal: "+str(g))
	return g


#traverse nodes until you reach goal. If root is reached before goal. Return 0.
def traverse_nodes(node,goal):
	print("traverse node 1: "+str(node.name))
	if node.brl == 0:
		return node.brl
	else:
		#get inverse of branch length add back in after rewriting br macx function to be inverse
		inv_br=1/float(node.brl)
		#subtract from goal
		goal -= inv_br
		#print("new goal:"+str(goal))
		#if goal is less than zero, return p as node you will start NNI with. 
		if goal <= 0:
			end = node
			#print("start: "+str(start.name))
			return end
		#if goal is still above 0, go to parent node and run program again
		elif goal > 0:
			p = node.parent
			#print("new parent: "+str(p.name))
			return traverse_nodes(p,goal)