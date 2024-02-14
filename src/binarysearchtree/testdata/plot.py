import matplotlib.pyplot as plt
import numpy as np
import json
import pprint

test_data = json.load(open('tests.json', 'r'))
big_tree_data = json.load(open('big_tree.json', 'r'))
optimized_tree_data = json.load(open('optimized_tree.json', 'r'))

test_names = [key for key, value in test_data.items()]

insertion_tests = filter(lambda x: "Insertion" in x, test_names)
searching_tests = filter(lambda x: "Searching" in x, test_names)
big_search = big_tree_data['Searching the random tree']
optimized = optimized_tree_data['Searching the random tree']

for test in insertion_tests:
    xAxis = [key for key, value in test_data[test].items()]
    yAxis = [value for key, value in test_data[test].items()]
    plt.plot(xAxis, yAxis, label=test)

plt.grid(True)
plt.xlabel('number of nodes')
plt.ylabel('time (s)')
plt.legend(loc='best')
plt.show()

for test in searching_tests:
    xAxis = [key for key, value in test_data[test].items()]
    yAxis = [value for key, value in test_data[test].items()]
    plt.plot(xAxis, yAxis, label=test)


plt.grid(True)
plt.xlabel('number of searches')
plt.ylabel('time (s)')
plt.legend(loc='best')
plt.show()


raw_x = np.array([key for key, value in big_search.items()])
raw_y = np.array([value for key, value in big_search.items()])
opt_x = np.array([key for key, value in optimized.items()])
opt_y = np.array([value for key, value in optimized.items()])

xAxis = raw_x
yAxis = np.around(((raw_y - opt_y) / raw_y) * 100, 2)

print(yAxis)
plt.bar(xAxis, yAxis, label="Percent improvement of optimization")


plt.grid(True)
plt.xlabel('number of searches')
plt.ylabel('%')
plt.legend(loc='best')
plt.show()