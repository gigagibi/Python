import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation

class Agent:
	def __init__(self, mood, x, y):
		self.SAD = True
		self.HAPPY = False
		if mood == 1:
			self.HAPPY = True
			self.SAD = False
		self.x = x
		self.y = y
		self.moods = [mood]

	def change_mood(self):
		if self.HAPPY:
			self.SAD = True
			self.HAPPY = False
			self.moods.append(-1)
		else:
			self.HAPPY = True
			self.SAD = False
			self.moods.append(1)


class SchellingModel:
	def __init__(self, width=100, height=100, happy_per=50):
		self._width = width
		self._height = height
		self._happy_per = happy_per
		self._HAPPY = 2
		self._SAD = 1
		self._NON_POPULATED = 0
		self._grid = np.random.randint(3, size=(self._height, self._width))
		self._proportion = 1
		self._agents = list()
		for row_idx, row in enumerate(self._grid):
			for col_idx, col in enumerate(row):
				if col == self._HAPPY:
					self._agents.append(Agent(1, col_idx, row_idx))
				elif col == self._SAD:
					self._agents.append(Agent(-1, col_idx, row_idx))
		self._mood_percentages = list()

	def set_width(self, width):
		self._width = width

	def set_height(self, height):
		self._height = height

	def set_happy_per(self, happy_per):
		self._happy_per = happy_per

	def init(self):
		cmap = colors.ListedColormap(['black', 'red', 'green'], N=None)
		happy_percentages = [i for i in self._mood_percentages]
		sad_percentages = [1/i*100*100 for i in self._mood_percentages]
		x = [i+1 for i in range(len(happy_percentages))]

		gs = GridSpec(nrows=2, ncols=2)

		ax0 = fig.add_subplot(gs[0,0])
		ax0.set_title('Happy, %', fontsize=10)
		
		line0, = ax0.plot(x, happy_percentages)

		ax1 = fig.add_subplot(gs[1,0])
		ax1.set_title('Sad, %', fontsize=10)
		
		line1, = ax1.plot(x, sad_percentages)

		ax2 = fig.add_subplot(gs[:,1])
		ax2.set_title('Grid', fontsize=5)

		line2 = ax2.imshow(self._grid, cmap=cmap)

		fig.tight_layout()

		return line0, line1, line2

	def get_graphics(self):
		cmap = colors.ListedColormap(['black', 'red', 'green'], N=None)
		happy_percentages = [i for i in self._mood_percentages]
		sad_percentages = [1/i*100*100 for i in self._mood_percentages]
		x = [i+1 for i in range(len(happy_percentages))]

		gs = GridSpec(nrows=2, ncols=2)

		ax0 = fig.add_subplot(gs[0,0])
		ax0.set_title('Happy, %', fontsize=10)
		
		line0, = ax0.plot(x, happy_percentages)

		ax1 = fig.add_subplot(gs[1,0])
		ax1.set_title('Sad, %', fontsize=10)
		
		line1, = ax1.plot(x, sad_percentages)

		ax2 = fig.add_subplot(gs[:,1])
		ax2.set_title('Grid', fontsize=10)
		
		line2 = ax2.imshow(self._grid, cmap=cmap)

		return line0, line1, line2


	def animate(self, i):
		self.make_step()
		return self.get_graphics()

	def count_proportion(self):
		happy, sad = 0, 0
		for row_idx, row in enumerate(self._grid):
			for col_idx, col in enumerate(row):
				if col == self._HAPPY:
					happy += 1
				elif col == self._SAD:
					sad += 1
		self._proportion = np.divide(happy, sad) * 100
		return self._proportion

	def get_proportion(self):
		return self._proportion
	
	def make_step(self):
		empty_houses = list()
		happy = 0
		sad = 0
		for agent in self._agents:
			if agent.HAPPY:
				happy += 1
			else:
				sad += 1
		for row_idx, row in enumerate(self._grid):
			for col_idx, col in enumerate(row):
				if col == self._NON_POPULATED:
					empty_houses.append((col_idx, row_idx))

		self._proportion = np.divide(happy, sad) * 100
		self._mood_percentages.append(self._proportion)

		agent_idx = random.randint(0, len(self._agents)-1)
		agent = self._agents[agent_idx]

		same_neighbours = self.count_neighbours(agent.x, agent.y)

		if np.divide(same_neighbours, 7) < np.divide(self._happy_per, 100):

			if len(empty_houses) != 0:
				empty_house_idx = random.randint(0, len(empty_houses)-1)
				non_pop_x, non_pop_y = empty_houses[empty_house_idx]
				self._grid[non_pop_y][non_pop_x] = self._grid[agent.y][agent.x]
				self._grid[agent.y][agent.x] = self._NON_POPULATED
				self._agents[agent_idx].x = non_pop_x
				self._agents[agent_idx].y = non_pop_y
				empty_houses.remove((non_pop_x, non_pop_y))

			elif self._grid[agent.y][agent.x] == self._HAPPY:
				self._grid[agent.y][agent.x] == self._SAD
				self._agents[agent_idx].change_mood()

		elif self._grid[agent.y][agent.x] == self._SAD:
			self._grid[agent.y][agent.x] == self._HAPPY
			self._agents[agent_idx].change_mood()
	
	def count_neighbours(self, agent_x, agent_y):
		same_neighbours = 0
		x_start = max(0, agent_x-1)
		y_it = max(0, agent_y-1)
		x_stop = min(self._width-1, agent_x+1)
		y_stop = min(self._height-1, agent_y+1)
		while y_it <= y_stop:
			x_it = x_start
			while x_it <= x_stop:
				if x_it != agent_x and y_it != agent_y and self._grid[y_it][x_it] == self._grid[agent_y][agent_x]:
					same_neighbours += 1
				x_it += 1
			y_it += 1
		return same_neighbours

model = SchellingModel(10, 10)
fig = plt.figure()
anim = FuncAnimation(fig, model.animate, init_func=model.init, frames=10000, interval=1, blit=True, repeat=False)
plt.show()