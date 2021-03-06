#!/usr/bin/env python

from __future__ import (division, print_function)
import random
import numpy

class Node:
	"""
	This class defines the structure of Nodes that will be used to build trees.
	"""
	
	def __init__(self,name="",parent=None,children=None, branchlength = 0):
		"""
		This function initializes the node's:
			- Name
			- Parent
			- Children
			- Branch length
		"""
		self.name = name
		self.brl = branchlength
		if parent is None:
			self.parent = []
		else:
			self.parent = parent
		if children is None:
			self.children = []
		else:
			self.children = children
		
class Tree:
	"""
	Defines a phylogenetic Tree class, consisting of linked Node objects.
	
	Assumes rooted, bifurcating trees.
	"""

	def __init__(self, data, ndict=None, terminal_nodes=None):
		
		# Instantiate a root node
		self.root = Node("root") 
		
		# Create tree from newick string, rooted on self.root
		self.newick_splicer(data.strip(";"), self.root)


	def newick_splicer(self, data, parent):
		"""
		Splices newick tree string (data) to instantiate a Tree object. The string passed
		as data should already have the trailing ";" removed. This tree will be rooted on 
		the node passed as parent.
		"""
		data = data.replace(" ", "")[1: len(data)] 	 #Get rid of all spaces and removes first and last parenthesis
		n = 0
		if data.count(",") != 0: #While there are comma separated taxa
			for key in range(len(data)): #Find the corresponding comma for a given parenthesis (n will be 0 for the correct comma)
				if data[key] == "(":
					n += 1 #Increase index of n by 1 for 1 step into new node
				elif data[key] == ")":
					n -= 1 #Decrease index of n by 1 for 1 step outout node
				elif data[key] == ",":
					if n == 0: #To check for correct comma
						vals = (data[0:key], data[key+1:len(data)-1]) #Break newick into left and right datasets
						for unit in vals: #For each entry of dataset
							if unit.find(":") != -1: #For cases with branch lengths
								d = unit[0:unit.rfind(":")] #get rid of trailing branchlength if provided. rfind from the right side
								node_creater = Node(d, parent = parent) #Create node entry
								node_creater.brl = float(unit[unit.rfind(":")+1:]) #Append branch length of that branch
								parent.children.append(node_creater) #Create children. Hello parent, your children are ...
								self.newick_splicer(d, node_creater) #Recursive function
							else: #For case with no branch lengths
								d=unit
								node_creater = Node(d, parent = parent)
								parent.children.append(node_creater)
								self.newick_splicer(d, node_creater)
						break #Terminate loop, we don't need to look any further


	def print_names(self,node):
		"""
		A method of a Tree object that will print out the names of its terminal nodes. To 
		print out all terminal node names, pass the root as an argument.
		"""
		if node.children == []: #Identifies terminal node
			print (node.name)
		else:
			for child in node.children:
				self.print_names(child)
	
	
	def list_term_nodes(self,node):
		"""
		A method of a Tree object that will print out the node names and instances for 
		all tips in a tree (or clade) subtended by the provided node. 
		"""
		if node.children == []: # Identifies terminal node
			print(node.name)
			print(node)
		else:	# Internal node
			for child in node.children:
				self.list_term_nodes(child)
	
	
	def inv_edge_len(self,node,edge=0):
		"""
		A method of a Tree object that will return the inverse of the total length from 
		given node to root. 
		"""
		#at root return total
		if node.brl == 0:
			return edge 
		else:
			#add branch length
			edge += 1/float(node.brl)
			return self.inv_edge_len(node.parent,edge)


	def tree_len(self,node):
		"""
		A method to calculate and return total tree length. Pass the root as an argument.
		"""
		tot_len = 0
		if node.children == []: #Terminal branch returns branch length
			return node.brl
		else:
			tot_len += node.brl #Add length of internal branch
			for child in node.children:
				tot_len += self.tree_len(child) #Add length of terminal branch
			return tot_len


	def inv_tree_len(self,node):
		"""
		A method to calculate and return inverse of total tree length.
		"""
		inv_tot_len = 0
		if node.children == []: #Terminal branch returns branch length
			return 1/float(node.brl)
		else:
			if node.brl == 0: #otherwise we get an error for root
				inv_tot_len += 0
				for child in node.children:
					inv_tot_len += self.inv_tree_len(child)
				return inv_tot_len
			else:
				inv_tot_len += 1/float(node.brl) #Add length of internal branch
				for child in node.children:
					inv_tot_len += self.inv_tree_len(child) #Add length of terminal branch
				return inv_tot_len


	def newick(self,node):
		"""
		A method of a Tree object that will print out the Tree as a
		parenthetical string (Newick format).
		"""

		newick = "(" #Opening bracket
		if node.children == []: #Terminal branch returns name
			return node.name + ":" + str(node.brl)
		else:
			for child in node.children:
				if node.children[-1] == child: #Don't add commas to last entry
					newick += self.newick(child)
				else:
					newick += self.newick(child) + "," #Adds commas to non-last entries
			if node.brl != 0:
				newick += "):" + str(node.brl) #Adds closing bracket
			else:
				newick += ")"
			return newick


	def has_grandkids(self,node):
		"""
		Takes a node and will randomy choose a child and return the child node if it has grandchildren
		could add an argument to determine if the child is chosen randomly or based on branch length of children. (for passing shorter branches to NNI moves more often).
		"""
		#if node has children
		if node.children != []:
			#pick random child
			kid = node.children[random.choice([0,1])]
			#if child has children, return grandchildren of node
			if kid.children != []:
				return kid
			else:
				return self.has_grandkids(node)
		#if node doesnt have children, you are at a tip
		else:
			return 0


	def node_dict(self,node,ndict=None):
		"""
		Returns dictionary with all nodes as keys and branch lengths as values.
		"""
		if ndict is None:
			ndict={}
		if node.children == []:		# Terminal node
			ndict[node]=node.brl	# Only terminal branch length returned
			return ndict
		else:						# Internal nodes
			ndict[node]=node.brl 	# Add internal branch length to dictionary
			for child in node.children:
				self.node_dict(child,ndict) # Recursively add all descendant brls
			return ndict
			
			
def pick_start_node(tree):
	"""
	Picks node as focus for NNI move.
	"""
	# Defines dictionary of nodes and branch lengths for tree
	n_dict = tree.node_dict(tree.root)
	
	# Draws random number from exponential to use when picking node
	goal = numpy.random.exponential(0.1)
	
	# Finds largest brl that's smaller than random exponential (goal)
	# Note for future: could also use smallest brl that's larger than goal
	start_brl = max(brl for brl in list(n_dict.values()) if brl < goal)
	
	# Finds node that matches chosen branch length
	# TO FIX: need to randomly select from among nodes with equal branch lengths
	for key, value in n_dict.items():
		if value == start_brl:
				start_node = key
				
	return start_node

def pickier_start_node(tree):
	"""
	Serves as wrapper around pick_start_node to filter out root and tips.
	"""
	# Start with root
	start_node = tree.root
	
	# Keep picking nodes until the node is not the root or a terminal branch
	while start_node.brl == 0 or start_node.children == []:
		start_node = pick_start_node(tree)
			
	return start_node  

"""
NOTE: Might want to define other functions for picking focal branch for NNI move (e.g., 
uniform across branches or directly proportional to inverse of branch length).
"""

def NNI(orig_tree):
	"""
	Does NNI move on random branch, preferentially choosing smaller branches. Returns altered tree. 
	
	Assumes bifurcating tree.
	"""
	tree = Tree(orig_tree.newick(orig_tree.root))
	
	# Store first focal node in c2
	c2 = pickier_start_node(tree)
	
	# Store 2nd focal node (parent) in p
	p = c2.parent
	
	#print("c2 = "+str(c2.name))
	#print("p = "+str(p.name))
	#assign other child to c1
	
	# Stores other child of p in c1
	for c in p.children:
			if c != c2:
				c1 = c
	
	# c2 will be the node for the brl we choose, so it will always have children. 
	# c1 is the other child of c2's parent
	# Storing branch lengths for c1 and c2. We don't technically need to store these 
	# because they are all still attached to c2, but doing it for clarity for now.
	br1 = c1.brl
	br2 = c2.brl
	
	# Finding children of c2 and storing their branch lengths
	gc1 = c2.children[0]
	gc2 = c2.children[1]
	br3 = gc1.brl
	br4 = gc2.brl
	
	# Remove all children from p
	p.children = []
	
	# Name and instantiate new node
	name = "new_"+str(c2.name)
	new_node = Node(name,parent=p)
	
	# Give it branchlength of c2, then start adding branches
	new_node.brl = br2
	
	# Add new node to parent
	p.children.append(new_node)
	
	# Add c1 to new node
	new_node.children.append(c1)
	c1.parent = new_node
	
	# Reassigning grandkids, one to parent, one to new node. randomly. 
	adopt=random.choice([1,2])
	if adopt == 1:
		p.children.append(gc1)
		gc1.parent = p
		new_node.children.append(gc2)
		gc2.parent = new_node
	elif adopt ==2:
		p.children.append(gc2)
		gc2.parent = p
		new_node.children.append(gc1)
		gc1.parent = new_node

	return tree