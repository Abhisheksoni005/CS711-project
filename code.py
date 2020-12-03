import random
import sys
import math
from networkx.generators.random_graphs import erdos_renyi_graph

USER_NUM = 25
POST_NUM = 4
LOOPS = 10
GAUSS_FAC = 10/9
ALPHA  = 0.95
BETA = 0.90

users = USER_NUM*[0]
posts = POST_NUM*[0]

graph = {}
viewership_map = {}
like_map = {}
share_map = {}
dislike_map = {}

def printmaps():
	print("\nviewership")
	for x in viewership_map:print(x,viewership_map[x])
	print("\nDislikes")
	for x in dislike_map:print(x,dislike_map[x])
	print("\nLikes")
	for x in like_map:print(x,like_map[x])
	print("\nShares")
	for x in share_map:print(x,share_map[x])

def printutil():
	print()
	print("Utility of platform:", utility_platform())
	print("Utility of users:", round(sum(utility_users()),2))
	print("Utility of creators:", round(sum(utility_creaters()),2))	

def gaussian(x,mu,sigma):
	if sigma == 0 : return 1
	x = float(x - mu)/sigma
	return math.exp(-x*x/2.0)/math.sqrt(2.0*math.pi)/sigma

def mu_val(arr):
	return sum(arr)/len(arr)

def invert(x):
	return round(1/x,2) if x else 0	

def sigma_val(arr,mu):
	crr = [0]*len(arr)
	for i in range(len(crr)):crr[i] = (arr[i] - mu)**2
	return (sum(crr)/len(crr))**0.5	

def cointoss(p):
	return 1 if random.random() < p else 0

def viewership():
	global viewership_map
	viewership_map = {}
	sigma = 1
	for i in range(len(posts)):
		mu = posts[i]
		for j in range(len(users)):
			k = gaussian(mu,mu,sigma)*GAUSS_FAC
			if cointoss(gaussian(users[j],mu,sigma)/k) == 1:
				if i not in viewership_map:viewership_map[i] = []
				viewership_map[i].append(j)

def generate_actions_given_bias():
	global like_map
	global share_map
	global dislike_map
	like_map = {}
	share_map = {}
	dislike_map = {}

	for i in viewership_map:
		mu = posts[i]
		sigma = 0.25

		k = gaussian(mu,mu,sigma)*GAUSS_FAC
		for j in viewership_map[i]:
			if cointoss(gaussian(users[j],mu,sigma)/k) == 1:
				if i not in like_map:like_map[i] = []
				like_map[i].append(j)
			else:
				if i not in dislike_map:dislike_map[i] = []
				dislike_map[i].append(j)
	
	for i in like_map:
		mu = posts[i]
		sigma = 0.02
		for j in like_map[i]:
			if cointoss(gaussian(users[j],mu,sigma)) == 1:
				if i not in share_map:share_map[i]=[]
				share_map[i].append(j)

def generate_actions():
	global like_map
	global share_map
	global dislike_map
	# like_map = {}
	# share_map = {}
	# dislike_map = {}

	for i in viewership_map:
		mu = posts[i]
		sigma = 0.25

		k = gaussian(mu,mu,sigma)*GAUSS_FAC
		for j in viewership_map[i]:
			if (i in like_map and j in like_map[i]) or (i in dislike_map and j in dislike_map[i]):
				continue
			if cointoss(gaussian(users[j],mu,sigma)/k) == 1:
				if i not in like_map:like_map[i] = []
				like_map[i].append(j)
			else:
				if i not in dislike_map:dislike_map[i] = []
				dislike_map[i].append(j)
	
	for i in like_map:
		mu = posts[i]
		sigma = 0.02
		for j in like_map[i]:
			if i in share_map and j in share_map[i]:continue
			if cointoss(gaussian(users[j],mu,sigma)) == 1:
				if i not in share_map:share_map[i]=[]
				share_map[i].append(j)

def update_user_bias():
	for i in like_map:
		for j in like_map[i]:
			users[j] = round(users[j]*ALPHA + posts[i]*(1-ALPHA),2)

	for i in dislike_map:
		for j in dislike_map[i]:
			users[j] = round(users[j]*ALPHA - posts[i]*(1-ALPHA),2)
			
	for i in share_map:
		for j in share_map[i]:
			users[j] = round(users[j]*BETA + posts[i]*(1-BETA),2)


def share():
	global viewership_map
	# viewership_map = {}
	for i in share_map:
		for j in share_map[i]:
			for k in graph[j]:
				if i not in viewership_map:viewership_map[i]=[]
				if k not in viewership_map[i]:
					viewership_map[i].append(k)


# relate platform utility to decreasing user bias
def utility_platform():
	util = 0
	for i in viewership_map:
		util += len(viewership_map[i])
	return round(util/USER_NUM/POST_NUM,2)


def utility_creaters():
	util = POST_NUM*[0]
	for i in like_map:
		util[i] += len(like_map[i])
	for i in dislike_map:
		util[i] -= len(dislike_map[i])*0.25
	for i in share_map:
		util[i] += len(share_map)*2
	return util	

def utility_users():
	util = USER_NUM*[0]
	for i in viewership_map:
		for j in viewership_map[i]:
			util[j] += abs(posts[i]-users[j])	
	util = map(lambda x: invert(x), util)
	return util

def initialize():	
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

	print(users)
	print(posts)	
	for i in graph:
		print(i,graph[i])

	viewership()
	
initialize()
printutil()
printmaps()

for i in range(LOOPS):
	print("LOOP",i)
	generate_actions()
	update_user_bias()
	printutil()
	printmaps()
	# viewership()
	share()
	# print(users)

