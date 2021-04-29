import random
import numpy as np
from api import Api
import pickle
import time
file_dir = './q_table/'

class QLearningAgent:
    def __init__(self, world):
        self.actions = ['N', 'S', 'W', 'E']
        self.learning_rate = 0.01
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.world = world
        self.q_table = self.load_qtable()

    def learn(self, state, action, reward, next_state):
        current_q = self.q_table[state[0]][state[1]][action]
        new_q = reward + self.discount_factor * max(self.q_table[next_state[0]][next_state[1]])
        self.q_table[state[0]][state[1]][action] += self.learning_rate * (new_q - current_q)
        print(self.q_table[state[0]][state[1]])
        self.store_qtable()


    def load_qtable(self):
        try:
            print('Checking for q-table of world {} file'.format(self.world))
            filename = 'q_table{}.pkl'.format(self.world)
            q_table = pickle.load(open(file_dir + filename, 'rb'))
            print('Q_table file found.')
            return q_table
        except (OSError, IOError, EOFError) as e:
            print('No q-table file of world {} found. Creating one.'.format(self.world))
            # Initialize Q-Values -> 3-dimensional array with x,y coordinates and action
            q_table = np.array(np.zeros([40, 40, 4]))
            filename = 'q_table{}.pkl'.format(self.world)
            pickle.dump(q_table, open(file_dir + filename, 'wb'))
            print('Q-table file of world {} created successfully.'.format(self.world))
            return q_table

    def store_qtable(self):
        q_table = self.q_table
        filename = 'q_table{}.pkl'.format(self.world)
        pickle.dump(q_table, open(file_dir + filename, 'wb'))
        print('Updating Q-table of world {}'.format(self.world))

    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            # random explore
            action = np.random.choice(len(self.actions))
        else:
            # choosing action from q-table
            state_action = self.q_table[state[0]][state[1]]
            action = self.arg_max(state_action)
        return action

    @staticmethod
    def arg_max(state_action):
        max_index_list = []
        max_value = state_action[0]
        for index, value in enumerate(state_action):
            if value > max_value:
                max_index_list.clear()
                max_value = value
                max_index_list.append(index)
            elif value == max_value:
                max_index_list.append(index)

        return random.choice(max_index_list)

'''
api = Api(1077, 1287)
q_table = np.array(np.zeros([40, 40, 4]))
world = api.get_location()
print(world)
agent = QLearningAgent(q_table)
reward, state = api.make_move('', world)
stateX = int(state['x'])
stateY = int(state['y'])
state = [stateX, stateY]
print(state)
action = agent.get_action(state)
'''
