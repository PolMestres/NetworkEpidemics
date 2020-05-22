#Compare between two strategies
#Central locations vs non central locations (static or dynamic graph)
import networkx as nx
import matplotlib.pyplot as plt 
from random import choice, uniform
import matplotlib.animation as animation
import numpy as np
from scipy.special import gamma, factorial

n = 100
p = 0.15
k = 4
#G = nx.random_geometric_graph(n,p)
G = nx.watts_strogatz_graph(n,k,p)

G1 = G.copy()
G2 = G.copy()

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(figsize=(14,8), nrows=2, ncols=2)
#plt.axis('off')
#plt.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off', labeltop='off', labelright='off', labelbottom='off')

beta1 = 1
delta1 = 0.2
beta2 = 1
delta2 = 0.2

extra_conn_lam1 = 0.1
extra_conn_lam2 = 0.1

central_location_infection_prob = 0.8
central_location_prob = 0.4

quar = 0.3

color_map1 = []
color_map2 = []

random_node = choice(list(G.nodes()))
for node in G:
	if node == random_node:
		color_map1.append([1,0,0])
		color_map2.append([1,0,0])
	else:
		color_map1.append([0,1,0])
		color_map2.append([0,1,0])

#Central location nodes
num_central_locations = 2
central_locations = []
for k in range(num_central_locations):
	nn = len(G1.nodes)
	G1.add_node(nn)
	central_locations.append(nn)
	color_map1.append([1,1,0]) #yellow

pos1 = nx.spring_layout(G1)
pos2 = nx.spring_layout(G2)

infec1 = 0
susc1 = 0
recov1 = 0

infec2 = 0
susc2 = 0
recov2 = 0

infec1_list = [1]
susc1_list = [n-1]
recov1_list = [0]

infec2_list = [1]
susc2_list = [n-1]
recov2_list = [0]

final1 = False
final2 = False

time_to_no_susc1 = 0
time_to_no_susc2 = 0

def update(i):

	global G1, G2, color_map1, color_map2, pos, infec1, infec2, susc1, susc2, recov1, recov2
	global susc1_list, susc2_list, recov1_list, recov2_list, infec1_list, infec2_list
	global final1, final2
	global time_to_no_susc1, time_to_no_susc2

	if (i == 0):
		#print(len(G1.nodes()))
		#print(len(pos1))
		#print(len(color_map1))
		nx.draw(G1, pos1, node_color=color_map1, node_size=50, ax=ax1)
		ax2.plot(range(i+1), susc1_list, color=[0,1,0])
		ax2.plot(range(i+1), recov1_list, color=[0,0,1])
		ax2.plot(range(i+1), infec1_list, color=[1,0,0])
		nx.draw(G2, pos2, node_color=color_map2, node_size=50, ax=ax3)
		ax4.plot(range(i+1), susc2_list, color=[0,1,0])
		ax4.plot(range(i+1), recov2_list, color=[0,0,1])
		ax4.plot(range(i+1), infec2_list, color=[1,0,0])

	elif (final1 and final2):
		print("-----")

		print("Max fraction of infected in G1: {}".format(max(infec1_list)/(len(G1.nodes()))))
		print("Time to max infections peak in G1: {}".format(infec1_list.index(max(infec1_list))))
		print("Time to extinction in G1: {}".format(len(infec1_list)))
		print("Number of susceptibles in equilibrium in G1: {}".format(susc1_list[-1]))
		print("Time to no susceptibles in G1: {}".format(time_to_no_susc1))

		print("-----")

		print("Max fraction of infected in G2: {}".format(max(infec2_list)/(len(G2.nodes()))))
		print("Time to max infections peak in G2: {}".format(infec2_list.index(max(infec2_list))))
		print("Time to extinction in G2: {}".format(len(infec2_list)))
		print("Number of susceptibles in equilibrium in G2: {}".format(susc2_list[-1]))
		print("Time to no susceptibles in G2: {}".format(time_to_no_susc2))

	elif (not final1 or not final2):
		ax1.clear()
		ax2.clear()
		ax3.clear()
		ax4.clear()

		# extra_edges1 = []
		# for node in G1:
		# 	if node not in central_locations:
		# 		num_extra_connections1 = np.random.poisson(extra_conn_lam1)
		# 		for k in range(num_extra_connections1):
		# 			hn = choice(list(G1.nodes()))
		# 			if (not G1.has_edge(node,hn)):
		# 				G1.add_edge(node,hn)
		# 				extra_edges1.append([node,hn])

		# extra_edges2 = []
		# for node in G2:
		# 	num_extra_connections2 = np.random.poisson(extra_conn_lam2)
		# 	for k in range(num_extra_connections2):
		# 		hn = choice(list(G2.node()))
		# 		if (not G2.has_edge(node,hn)):
		# 			G2.add_edge(node,hn)
		# 			extra_edges2.append([node,hn])

		#At each iteration each node makes extra connections randomly with a central location
		central_location_edges = []
		#central_location_prob = 2*infec1/len(G1.nodes()) #it can be greater than one but it's okay
		for node in G1:
			if node not in central_locations:
				if uniform(0,1) < central_location_prob:
					cen_loc = choice(central_locations)
					G1.add_edge(node,cen_loc)
					central_location_edges.append([node,cen_loc])

		#Run model G1

		color_map12 = []

		for node in G1:
			if color_map1[node] == [0,1,0]:
				infected_neighs = 0
				num_neighs = 0
				for neigh in G.neighbors(node):
					num_neighs += 1
					if color_map1[neigh] == [1,0,0]: #infected
						infected_neighs += 1
				if num_neighs == 0:
					color_map12.append([0,1,0])
				else:				
					if uniform(0,1) < beta1*infected_neighs/num_neighs:
						color_map12.append([1,0,0])
						if uniform(0,1) < quar:
							G1.remove_edges_from(list(G1.edges(node))) 
					else:
						color_map12.append([0,1,0])

				for central_location in central_locations: #if the node didn't get infected by normal procedures but went to a central location
					if (color_map12[node] == [0,1,0] and G.has_edge(node,central_location)):
						if uniform(0,1) < central_location_infection_prob:
							del color_map12[-1]
							color_map12.append([1,0,0])

			elif (color_map1[node] == [1,0,0]):
				if uniform(0,1) < delta1:
					color_map12.append([0,0,1])
				else:
					color_map12.append([1,0,0])

			elif color_map1[node] == [0,0,1]:
					color_map12.append([0,0,1])

			elif color_map1[node] == [1,1,0]: #central location
				color_map12.append([1,1,0])

			
		color_map1 = color_map12.copy()

		#Run model G2

		color_map22 = []

		for node in G2:
			if color_map2[node] == [0,1,0]:
				infected_neighs = 0
				num_neighs = 0
				for neigh in G.neighbors(node):
					num_neighs += 1
					if color_map2[neigh] == [1,0,0]: #infected
						infected_neighs += 1
				if num_neighs == 0:
					color_map22.append([0,1,0])
				else:				
					if uniform(0,1) < beta2*infected_neighs/num_neighs:
						color_map22.append([1,0,0])
					else:
						color_map22.append([0,1,0])

			elif (color_map2[node] == [1,0,0]):
				if uniform(0,1) < delta2:
					color_map22.append([0,0,1])
				else:
					color_map22.append([1,0,0])

			elif color_map2[node] == [0,0,1]:
					color_map22.append([0,0,1])

		color_map2 = color_map22.copy()

		#Draw

		#print("Before drawing")
		#print(G1.edges())

		nx.draw(G1, pos1, node_color=color_map1, node_size=50, ax=ax1)

		infec1 = 0
		recov1 = 0
		susc1 = 0

		for color in color_map1:
			if color == [1,0,0]:
				infec1 += 1
			elif color == [0,1,0]:
				susc1 += 1
			elif color == [0,0,1]:
				recov1 += 1

		if infec1 == 0:
			final1 = True

		if (susc1 == 0 and time_to_no_susc1 == 0):
			time_to_no_susc1 = i

		infec1_list.append(infec1)
		recov1_list.append(recov1)
		susc1_list.append(susc1)

		ax2.axis('off')
		ax2.plot(range(i+1), susc1_list, color=[0,1,0])
		ax2.plot(range(i+1), recov1_list, color=[0,0,1])
		ax2.plot(range(i+1), infec1_list, color=[1,0,0])

		#frame1 = plt.gca()
		#frame1.axes.xaxis.set_ticklabels([])
		#frame1.axes.yaxis.set_ticklabels([])

		nx.draw(G2, pos2, node_color=color_map2, node_size=50, ax=ax3)

		infec2 = 0
		recov2 = 0
		susc2 = 0

		for color in color_map2:
			if color == [1,0,0]:
				infec2 += 1
			elif color == [0,1,0]:
				susc2 += 1
			elif color == [0,0,1]:
				recov2 += 1

		if infec2 == 0:
			final2 = True

		if (susc2 == 0 and time_to_no_susc2 == 0):
			time_to_no_susc2 = i

		infec2_list.append(infec2)
		recov2_list.append(recov2)
		susc2_list.append(susc2)

		ax4.axis('off')
		ax4.plot(range(i+1), susc2_list, color=[0,1,0])
		ax4.plot(range(i+1), recov2_list, color=[0,0,1])
		ax4.plot(range(i+1), infec2_list, color=[1,0,0])

		#Remove extra edges
		# for edge in extra_edges1:
		# 	if G1.has_edge(edge[0],edge[1]):
		# 		G1.remove_edge(edge[0],edge[1])

		# for edge in extra_edges2:
		# 	if G2.has_edge(edge[0],edge[1]):
		# 		G2.remove_edge(edge[0],edge[1])

		#Remove extra edges central location
		for edge in central_location_edges: #?
			if (G1.has_edge(edge[0],edge[1])):
				G1.remove_edge(edge[0],edge[1])

ani = animation.FuncAnimation(fig, update, frames=100, interval=500, repeat=False)
plt.show()



















