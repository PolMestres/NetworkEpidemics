#Quarantining Infected Individuals
import networkx as nx
import matplotlib.pyplot as plt 
from random import choice, uniform
import matplotlib.animation as animation
import numpy as np 

n = 100
p = 0.15
k = 5
#G = nx.random_geometric_graph(n,p)
G = nx.watts_strogatz_graph(n,k,p)
#G = nx.watts_strogatz_graph(n,k,1) #Equivalent to Erdos-Renyi random graph

pos = nx.spring_layout(G)

G1 = G.copy()
G2 = G.copy()

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(figsize=(14,8), nrows=2, ncols=2)

beta = 3
delta = 0.5

quar = 0.3 #Probability that when a node is infected, all its connections are dropped

color_map1 = []
color_map2 = []

random_node = choice(list(G.node()))
for node in G:
	if node == random_node:
		color_map1.append([1,0,0])
		color_map2.append([1,0,0])
	else:
		color_map1.append([0,1,0])
		color_map2.append([0,1,0])

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

def update(i):

	global G1, G2, color_map1, color_map2, pos, infec1, infec2, susc1, susc2, recov1, recov2
	global susc1_list, susc2_list, recov1_list, recov2_list, infec1_list, infec2_list
	global final1, final2

	if (i == 0):
		nx.draw(G1, pos, node_color=color_map1, node_size=50, ax=ax1)
		ax2.plot(range(i+1), susc1_list, color=[0,1,0])
		ax2.plot(range(i+1), recov1_list, color=[0,0,1])
		ax2.plot(range(i+1), infec1_list, color=[1,0,0])
		nx.draw(G2, pos, node_color=color_map2, node_size=50, ax=ax3)
		ax4.plot(range(i+1), susc2_list, color=[0,1,0])
		ax4.plot(range(i+1), recov2_list, color=[0,0,1])
		ax4.plot(range(i+1), infec2_list, color=[1,0,0])

	elif (final1 and final2):
		print("Max fraction of infected in G1: {}".format(max(infec1_list)/(len(G1.nodes()))))
		print("Time to max infections peak in G1: {}".format(infec1_list.index(min(infec1_list))))
		print("Time to extinction in G1: {}".format(len(infec1_list)))
		print("Number of susceptibles in equilibrium in G1: {}".format(susc1_list[-1]))

		print("Max fraction of infected in G2: {}".format(max(infec2_list)/(len(G2.nodes()))))
		print("Time to max infections peak in G2: {}".format(infec2_list.index(min(infec2_list))))
		print("Time to extinction in G2: {}".format(len(infec2_list)))
		print("Number of susceptibles in equilibrium in G2: {}".format(susc2_list[-1]))

	elif (not final1 or not final2):
		ax1.clear()
		ax2.clear()
		ax3.clear()
		ax4.clear()

		#Run model G1 (with quarantine)

		color_map12 = []

		for node in G1:
			if color_map1[node] == [0,1,0]:
				infected_neighs = 0
				num_neighs = 0
				for neigh in G1.neighbors(node):
					num_neighs += 1
					if color_map1[neigh] == [1,0,0]:
						infected_neighs += 1
				if num_neighs == 0:
					color_map12.append([0,1,0])
				else:
					if uniform(0,1) < beta*infected_neighs/num_neighs:
						color_map12.append([1,0,0])
						if uniform(0,1) < quar:
							G1.remove_edges_from(list(G1.edges(node))) 
							#Other quarantine approaches can also be considered
							#The fact that edges aren't recovered after being infected increases the prob of being infected bc fraction will be bigger
							#Note that here we introduce an immediate quarantine: we assume no delay between the moment the individual gets infected and the moment it quarantines

					else:
						color_map12.append([0,1,0])

			elif (color_map1[node] == [1,0,0]):
				if uniform(0,1) < quar: #If it didn't quarantine before, every iteration has a chance to do so
					G1.remove_edges_from(list(G1.edges(node)))
				if uniform(0,1) < delta:
					color_map12.append([0,0,1])
				else:
					color_map12.append([1,0,0])

			elif color_map1[node] == [0,0,1]:
				color_map12.append([0,0,1])

		color_map1 = color_map12.copy()

		#Run model G2 (No quarantine)

		color_map22 = []

		for node in G2:
			if color_map2[node] == [0,1,0]:
				infected_neighs = 0
				num_neighs = 0
				for neigh in G2.neighbors(node):
					num_neighs += 1
					if color_map2[neigh] == [1,0,0]:
						infected_neighs += 1
				if num_neighs == 0:
					color_map22.append([0,1,0])
				else:
					if uniform(0,1) < beta*infected_neighs/num_neighs:
						color_map22.append([1,0,0])
					else:
						color_map22.append([0,1,0])

			elif (color_map2[node] == [1,0,0]):
				if uniform(0,1) < quar: #If it didn't quarantine before, every iteration has a chance to do so
					G2.remove_edges_from(list(G2.edges(node)))
				if uniform(0,1) < delta:
					color_map22.append([0,0,1])
				else:
					color_map22.append([1,0,0])

			elif color_map2[node] == [0,0,1]:
				color_map22.append([0,0,1])

		color_map2 = color_map22.copy()

		#Draw

		nx.draw(G1, pos, node_color=color_map1, node_size=50, ax=ax1)

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

		nx.draw(G2, pos, node_color=color_map2, node_size=50, ax=ax3)

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

		infec2_list.append(infec2)
		recov2_list.append(recov2)
		susc2_list.append(susc2)

		ax4.axis('off')
		ax4.plot(range(i+1), susc2_list, color=[0,1,0])
		ax4.plot(range(i+1), recov2_list, color=[0,0,1])
		ax4.plot(range(i+1), infec2_list, color=[1,0,0])


ani = animation.FuncAnimation(fig, update, frames=100, interval=500, repeat=False)
plt.show()









