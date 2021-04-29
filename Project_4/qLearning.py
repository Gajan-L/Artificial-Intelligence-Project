import random
import numpy as np
import pickle
file_dir = './q_table/'

class QLearningAgent:
    def __init__(self, world):
        self.actions = ['N', 'S', 'E', 'W']
        self.learning_rate = 0.01
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.world = world
        self.q_table = self.load_qtable()
    
    # the learing function
    def learn(self, state, action, reward, next_state):
        current_q = self.q_table[state[0]][state[1]][action]
        new_q = reward + self.discount_factor * max(self.q_table[next_state[0]][next_state[1]])
        self.q_table[state[0]][state[1]][action] += self.learning_rate * (new_q - current_q)
        print(self.q_table[state[0]][state[1]])
        self.store_qtable()

    # loading qtable fime
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
    
    # storing qtable file
    def store_qtable(self):
        q_table = self.q_table
        filename = 'q_table{}.pkl'.format(self.world)
        pickle.dump(q_table, open(file_dir + filename, 'wb'))
        print('Updating Q-table of world {}'.format(self.world))
    
    # avoid the action that will hit the wall
    # it returns a list of actions that are valid 
    def avoid_hitting_wall(self,state):
        valid_action = [0, 1, 2, 3]
        if state[0] == 0:
            # avoid go west
            valid_action.remove(3)
        if state[0] == 39:
            # avoid go east
            valid_action.remove(2)
        if state[1] == 0:
            # avoid go south
            valid_action.remove(1)
        if state[1] == 39:
            # avoid go north
            valid_action.remove(0)
        return valid_action

    # get next action
    def get_action(self, state):
        valid_action = self.avoid_hitting_wall(state)
        if np.random.rand() < self.epsilon:
            # random explore
            action = np.random.choice(valid_action)
        else:
            # choosing action from q-table
            state_table = self.q_table[state[0]][state[1]]
            action = self.arg_max(state_table, valid_action)
        return action

    @staticmethod
    def arg_max(state_table, valid_action):
        max_index_list = []
        max_value = state_table[valid_action[0]]
        for index in valid_action:
            if state_table[index] > max_value:
                max_index_list.clear()
                max_value = state_table[index]
                max_index_list.append(index)
            elif state_table[index] == max_value:
                max_index_list.append(index)
        return random.choice(max_index_list)
