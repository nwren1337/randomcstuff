import matplotlib.pyplot as pyplot
import json

test_data = json.load(open('tests.json', r))

json.pprint(test_data)