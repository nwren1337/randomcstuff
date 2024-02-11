import matplotlib.pyplot as plt
import json
import pprint

test_data = json.load(open('tests.json', 'r'))

test_names = [key for key, value in test_data.items()]

insertion_tests = filter(lambda x: "Insertion" in x, test_names)
searching_tests = filter(lambda x: "Searching" in x, test_names)

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