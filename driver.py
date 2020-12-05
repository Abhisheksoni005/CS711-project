import random
import sys
import math
import csv
import copy

USER_NUM = 150
POST_NUM = 50
LOOPS = 20
GAUSS_FAC = 10/9
ALPHA  = 0.90
BETA = 0.75
RANGE = "ALL"

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

def invert(x,y):
	val = 1/math.exp(abs(x-y)**2)
	return round(val,2) if x else 0	

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

	for i in viewership_map:
		mu = posts[i]
		sigma = 0.25

		for j in viewership_map[i]:
			if (i in like_map and j in like_map[i]) or (i in dislike_map and j in dislike_map[i]):continue
			
			if abs(posts[i]) > 0.5 and posts[i]*users[j] > 0 and abs(posts[i]) > abs(users[j]):
				if cointoss(abs(posts[i])) == 1:
					if i not in dislike_map:dislike_map[i] = []
					dislike_map[i].append(j)
					update_dislike(i,j)
					
				else:
					if i not in like_map:like_map[i] = []
					like_map[i].append(j)
					update_like(i,j)

			elif abs(posts[i]) < 0.25 and abs(posts[i]) <  abs(users[j]):
				if cointoss(abs(1-posts[i])) == 1:
					if i not in like_map:like_map[i] = []
					like_map[i].append(j)
					update_like(i,j)

				else:
					if i not in dislike_map:dislike_map[i] = []
					dislike_map[i].append(j)
					update_dislike(i,j)
				
			else:
				k = gaussian(mu,mu,sigma)*GAUSS_FAC

				if cointoss(gaussian(users[j],mu,sigma)/k) == 1:
					if i not in like_map:like_map[i] = []
					like_map[i].append(j)
					update_like(i,j)

				else:
					if i not in dislike_map:dislike_map[i] = []
					dislike_map[i].append(j)
					update_dislike(i,j)
		
	for i in like_map:
		mu = posts[i]
		sigma = 0.02
		for j in like_map[i]:
			if i in share_map and j in share_map[i]:continue
			if cointoss(gaussian(users[j],mu,sigma)) == 1:
				if i not in share_map:share_map[i]=[]
				share_map[i].append(j)
				update_shares(i,j)

def generate_actions():
	global like_map
	global share_map
	global dislike_map

	for i in viewership_map:
		mu = posts[i]
		sigma = 0.25

		k = gaussian(mu,mu,sigma)*GAUSS_FAC
		for j in viewership_map[i]:
			if (i in like_map and j in like_map[i]) or (i in dislike_map and j in dislike_map[i]): continue

			if cointoss(gaussian(users[j],mu,sigma)/k) == 1:
				if i not in like_map:like_map[i] = []
				like_map[i].append(j)
				update_like(i,j)
			else:
				if i not in dislike_map:dislike_map[i] = []
				dislike_map[i].append(j)
				update_dislike(i,j)
	
	for i in like_map:
		mu = posts[i]
		sigma = 0.02
		for j in like_map[i]:
			if i in share_map and j in share_map[i]:continue
			if cointoss(gaussian(users[j],mu,sigma)) == 1:
				if i not in share_map:share_map[i]=[]
				share_map[i].append(j)
				update_shares(i,j)

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

def update_like(i,j):
	users[j] = round(users[j]*ALPHA + posts[i]*(1-ALPHA),2)

def update_dislike(i,j):
	users[j] = round(users[j]*ALPHA - posts[i]*(1-ALPHA),2)

def update_shares(i,j):
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


def reputation(index):
	return invert(users[index],0)

# relate platform utility to decreasing user bias
def utility_platform():
	util1,util2 = 0,0

	for i in viewership_map:
		util1 += len(viewership_map[i])
	for i in users:
		util2 += invert(i,0)

	# print(util1/USER_NUM/POST_NUM ,util2/USER_NUM)	
	util = util1/USER_NUM/POST_NUM + util2/USER_NUM
	return round(util,2)


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
			util[j] += invert(posts[i],users[j])

	# for i in range(len(users)):
	# 	util[i] += reputation(i)	
	
	return util

def initialize(flag):
	global like_map,dislike_map,share_map
	like_map,dislike_map,share_map = {},{},{}
	
	with open(datafile, 'r') as csvfile:
	
		csvreader = csv.reader(csvfile)
		
		global users
		global posts
		users = next(csvreader)
		posts = next(csvreader)
		
		users = [float(x) for x in users]
		posts = [float(x) for x in posts]

		USER_NUM = len(users)
		POST_NUM = len(posts)

		for row in csvreader:
			graph[int(row[0])] = [ int(x) for x in row[1:]]	

	if flag:viewership()

datafile = "data_" + str(USER_NUM) + "_" + str(POST_NUM) + "_" + RANGE + ".csv"
initialize(1)

init_viewership = copy.deepcopy(viewership_map)

print("Bias:Not Visible")
for i in range(LOOPS):
	generate_actions()
	# printmaps()
	share()
	print(round(sum(map(lambda x:(x**2),users)),3))

printutil()
print(round(sum(map(lambda x:(x**2),users)),3))

initialize(0)

viewership_map = init_viewership

print("Bias:Visible")
for i in range(LOOPS):
	generate_actions_given_bias()
	share()
	print(round(sum(map(lambda x:(x**2),users)),3))


printutil()
print(round(sum(map(lambda x:(x**2),users)),3))


