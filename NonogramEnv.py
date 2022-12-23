import gym
from gym import spaces
import numpy as np
from tkinter import *


def calculate_reward(grid, solution):
    width = len(grid[0])
    height = len(grid)
    reward = 0

    for i in range(width):
        for j in range(height):
            if grid[i][j] != solution[i][j]:
                reward -= 1
    return reward


def generate_random_grid(height, width):
    # generate random playground fill with bools
    grid = np.random.choice(a=[False, True], size=(width, height)).tolist()
    return grid


def read_columns_from_grid(grid):
    columns = []
    for col in range(len(grid)):
        column = [row[col] for row in grid]
        last_false = -1
        c = []
        for i, cell in enumerate(column):
            if not cell:
                if last_false + 1 < i:
                    c.append(len(column[last_false + 1:i]))
                last_false = i
        if last_false + 1 < len(column):
            c.append(len(column[last_false + 1:len(column)]))
        columns.append(c)

    return columns


def read_rows_from_grid(grid):
    rows = []
    for row in grid:
        r = []
        last_false = -1
        for i, cell in enumerate(row):
            if not cell:
                if last_false + 1 < i:
                    r.append(len(row[last_false+1:i]))
                last_false = i
        if last_false+1 < len(row):
            r.append(len(row[last_false+1:len(row)]))
        rows.append(r)
    return rows


def generated_grid_with_numbers(grid, columns, rows):
    table = []
    extra_width = int(len(columns) / 2) + 1
    width = len(columns) + extra_width
    extra_height = int(len(rows) / 2) + 1
    height = len(rows) + extra_height

    for i in range(width):
        t = [0] * extra_width
        if width <= (i + len(columns)):
            for ind, x in enumerate(columns[i - len(t)]):
                t[ind] += x
        table.append(t)
    table = np.array(table).T.tolist()
    for i in range(len(rows)):
        t = [0] * extra_height
        for ind, x in enumerate(rows[i]):
            t[ind] += x
        table.append(t + grid[i])
    return table


class NonogramEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, width, height):
        super(NonogramEnv, self).__init__()

        self.game_width = width
        self.game_height = height

        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(2 * self.game_width * self.game_height)
        # Example for using image as input:
        self.observation_space = spaces.Discrete(
            (self.game_width + int(self.game_width / 2) + 1) * (self.game_height + int(self.game_height / 2) + 1))

        self.game_grid = generate_random_grid(self.game_height, self.game_width)
        self.solution = self.game_grid.copy()
        self.columns = read_columns_from_grid(self.game_grid)
        self.rows = read_rows_from_grid(self.game_grid)

    def step(self, action):
        # Execute one time step within the environment

        self._take_step(action)

        reward = calculate_reward(self.game_grid, self.solution)
        # print("action, reward: ", action, reward)

        obs = self._next_observation()
        done = not any(self.game_grid)

        return obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        # self.game_grid = np.empty((self.game_width, self.game_height))
        data = [None] * self.game_width * self.game_height
        self.game_grid = np.reshape(data, (self.game_width, self.game_height)).tolist()
        return self._next_observation()  # TODO

    def render(self, mode='human', close=False):
        # Render the environment to the screen

        table = generated_grid_with_numbers(self.game_grid, self.columns, self.rows)
        # print(table)

        print_table = []
        for row in table:
            print_table.append(['' if i is None else i for i in row])

        root = Tk()
        t = Table(root, print_table)
        root.mainloop()

        return None  # TODO

    def _next_observation(self):
        return generated_grid_with_numbers(self.game_grid, self.columns, self.rows)

    def _take_step(self, action):
        value = True if action >= self.game_width*self.game_height else False
        if value:
            action -= 25

        row_index = int(action/self.game_width)
        col_index = action - row_index*self.game_width
        self.game_grid[row_index][col_index] = value


class Table:

    def __init__(self, root, data):

        width = len(data[0])
        height = len(data)

        # code for creating table
        for i in range(width):
            for j in range(height):
                self.e = Entry(root, width=20, fg='black',
                               font=('Arial', 16, 'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(END, data[i][j])
