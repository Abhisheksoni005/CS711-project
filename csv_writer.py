
import csv

graph = {}



with open(datafile, 'w') as csvfile:
	csvwriter = csv.writer(csvfile)

	csvwriter.writerow(users)
	csvwriter.writerow(posts)

	for i in graph:
		temp = graph[i].copy()
		temp.insert(0, i)
		csvwriter.writerow(temp)		


