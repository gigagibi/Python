import json
import requests
import matplotlib.pyplot as plt
import numpy as np

table_data = requests.get('http://sovietov.com/kispython/table.json').json()['data']
failed_data = requests.get('http://sovietov.com/kispython/failed.json').json()

# groups with max submissions
scores_per_group = dict()
for row in table_data:
	if row[0] not in scores_per_group.keys():
		scores_per_group[row[0]] = 1
	else:
		scores_per_group[row[0]] += 1
scores_per_group = sorted(scores_per_group.items(), key=lambda x: x[1])

x = list()
y = list()
print(scores_per_group)

for group in scores_per_group:
	x.append(group[0])
	y.append(group[1])

fig, ax = plt.subplots(1,1)

ax.set_title('Решения групп')
ax.set_xlabel('Номер группы')
ax.set_ylabel('Количество решений')
ax.set_xticks([i+1 for i in range(len(x))])
ax.set_xticklabels(x, rotation=(-90), fontsize=7)
#ax.set_aspect('equal')
ax.plot(x, y)
ax.scatter(x,y)
plt.show()
"""
top = 10
print(f"====== top {top} ======")
for i in range(1, top+1):
	print(scores_per_group[-i][0], scores_per_group[-i][1])
print("====================")
"""

# simplest and hardest tasks
print()
subs_per_task = dict()
for row in table_data:
	#print(row)
	if row[2] not in subs_per_task.keys():
		subs_per_task[row[2]] = 1
	else:
		subs_per_task[row[2]] += 1
subs_per_task = sorted(subs_per_task.items(), key=lambda x: x[1])

x = list()
y = list()
print(subs_per_task)

for task in subs_per_task:
	x.append(int(task[0][1:]))
	y.append(task[1])

plt.title('Сложность задач')
plt.xlabel('Номер задачи')
plt.ylabel('Количество сданных')
plt.xticks(np.arange(min(x), max(x)+1, 1.0))
plt.scatter(x, y)
plt.plot(x,y)
plt.show()

# years with max amount of game releases
print()
with open('games.csv', encoding='utf-8') as file:
	games_data = file.read()

years = dict()
for game in games_data.split('\n'):
	if len(game) > 0:
		year = game.split(';')[-1].replace('"','')
		if year != 'не издана':
			year = int(year)
			if year not in years.keys():
				years[year] = 1
			years[year] += 1

years = sorted(years.items(), key=lambda x: x[1])

x = list()
y = list()

years_amount = 5

for year in range(0, years_amount):
	x.append(years[year][0])
	y.append(years[year][1])

plt.title('Игр в год')
plt.xlabel('Год')
plt.ylabel('Кол-во игр')
plt.plot(x,y)
plt.scatter(x,y)
plt.show()