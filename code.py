import random
import sys
import math

USER_NUM = 20
POST_NUM = 4
users = USER_NUM*[0]
posts = POST_NUM*[0]

viewership_map = {}
like_map = {}
share_map = {}
dislike_map = {}

def gaussian(x,mu,sigma):
	if sigma == 0 : return 1
	x = float(x - mu)/sigma
	return math.exp(-x*x/2.0)/math.sqrt(2.0*math.pi)/sigma

def mu_val(arr):
	return sum(arr)/len(arr)

def sigma_val(arr,mu):
	crr = [0]*len(arr)
	for i in range(len(crr)):crr[i] = (arr[i] - mu)**2
	return (sum(crr)/len(crr))**0.5	

def cointoss(p):
	return 1 if random.random() < p else 0

def viewership():
	mu = mu_val(posts)
	sigma = sigma_val(posts,mu)
	for i in range(len(posts)):
		for j in range(len(users)):
			if cointoss(gaussian(users[j],mu,sigma)) == 1:
				if i not in viewership_map:viewership_map[i] = []
				viewership_map[i].append(j)

def generate_actions():
	for i in viewership_map:
		mu = mu_val(viewership_map[i])
		sigma = sigma_val(viewership_map[i],mu)

		for j in viewership_map[i]:
			if cointoss(gaussian(users[j],mu,sigma)) == 1:
				if i not in like_map:like_map[i] = []
				like_map[i].append(j)
			else:
				if i not in dislike_map:dislike_map[i] = []
				dislike_map[i].append(j)

	for i in like_map:
		mu = mu_val(like_map[i])
		sigma = sigma_val(like_map[i],mu)

		print(like_map[i])
		for j in like_map[i]:
			if cointoss(gaussian(users[j],mu,sigma)) == 1:
				if i not in share_map:share_map[i]=[]
				share_map[i].append(j)


def initialize():	
	for i in range(USER_NUM):users[i]=round(random.uniform(-1,1),1)
	for i in range(POST_NUM):posts[i]=round(random.uniform(-1,1),1)
	users.sort()
	posts.sort()
	viewership()	
	generate_actions()

initialize()

for x in viewership_map:print(x,viewership_map[x])
for x in dislike_map:print(x,dislike_map[x])
for x in like_map:print(x,like_map[x])
for x in share_map:print(x,share_map[x])

