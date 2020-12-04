import random
import sys
import math

import csv
from networkx.generators.random_graphs import erdos_renyi_graph

USER_NUM = 25
POST_NUM = 4

users = USER_NUM*[0]
posts = POST_NUM*[0]

graph = {}

for i in range(USER_NUM):users[i]=round(random.uniform(-1,1),2)
for i in range(POST_NUM):posts[i]=round(random.uniform(-1,1),2)
users.sort()
posts.sort()
g = erdos_renyi_graph(USER_NUM,0.5)
for x,y in g.edges:
	if x not in graph:graph[x] = []
	if y not in graph:graph[y] = []
	graph[x].append(y)
	graph[y].append(x)

datafile = "data_" + str(USER_NUM) + "_" + str(POST_NUM) + ".csv"

with open(datafile, 'w') as csvfile:
	csvwriter = csv.writer(csvfile)

	csvwriter.writerow(users)
	csvwriter.writerow(posts)

	for i in graph:
		temp = graph[i].copy()
		temp.insert(0, i)
		csvwriter.writerow(temp)		


