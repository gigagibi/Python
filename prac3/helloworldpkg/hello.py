import json
import os

def printh():
	with open(os.path.dirname(__file__) + '\\hw.json') as file:
		data = json.load(file)
	print(data['hello'])