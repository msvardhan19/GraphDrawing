# importing necessary libraries
import numpy as np
import csv

# prompt user to take height of complete binary tree as input
h = int(input("Please enter the height of the complete binary tree: "))

# v = number of vertices in such binary tree is 2 ^ h - 1
# array a stores a random permutation of [1,2,..., v]
a = np.random.permutation(2 ** h - 1) + 1

with open('task4aOutput.csv', 'w') as f:
    writer = csv.writer(f)
    # number of edges in the binary tree - can be computed using height h
    writer.writerow([len(a) - 1])
    # elements of array are listed according to the bfs traversal of the tree
    lastInternalNode = 2 ** (h - 1) - 1
    for i in range(lastInternalNode):
        # left child of ith index node is (2 * i + 1)th index node
        writer.writerow([a[i], a[2 * i + 1]])
        # right child of ith index node is (2 * i + 2)th index node
        writer.writerow([a[i], a[2 * i + 2]])