# importing necessary libraries
import numpy as np
import csv

# prompts user to enter the input
n = int(input("Please enter n (no of partitions): "))
k = int(input("Please enter k (no of vertices in each partition): "))

a = np.random.permutation(n * k) + 1

with open('task4boutput.csv', 'w') as f:
    writer = csv.writer(f)
    # number of edges in complete multi-partite graph is (k ^ 2) * (nc2)
    edges = int((k * k * (n - 1) * n)/2)
    writer.writerow([edges])
    for i in range(n):
        for j in range(k):
            for u in range(i + 1, n):
                for v in range(k):
                    writer.writerow([a[i * k + j], a[u * k + v]])