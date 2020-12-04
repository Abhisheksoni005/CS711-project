import csv


graph = {}
users = []
posts = []

datafile = "nam.csv"
with open(datafile, 'r') as csvfile:
	csvreader = csv.reader(csvfile)

	users = next(csvreader)
	posts = next(csvreader)

	for row in csvreader:
		graph[row[0]] = row[1:]	

print(users)
print(posts)
print(graph)
