from api import Api
import numpy as np
import pickle
import time
from qLearning import QLearningAgent


def visit_num():
    try:
        print('Checking visit history file...')
        visit = pickle.load(open('visit','rb'))
        print('Visit file found!')
        return visit
    except (OSError, IOError, EOFError) as e:
        print('No visit history file! Start creating one...')
        visit = np.array(np.zeros([11]))
        print(visit)
        return visit

def store_visit(v):
    pickle.dump(v, open('visit', 'wb'))
    print('Updating visit history')

def decide_world(v):
    world = 1
    visited = v[world]
    for i in range(1, 11):
        if v[i] < visited:
            world = i
            visited = v[i]
    return world

def traverse(api, agent):
    # Locating agent and current state
    state, _ = api.make_move('', agent.world)
    time.sleep(15)
    stateX = int(state['x'])
    stateY = int(state['y'])
    state = [stateX, stateY]
    while True:
        print("Agent in {}".format(state))
        world = api.get_location()
        time.sleep(15)
        if world == -1:# break when exit a world
            break
        action = agent.get_action(state)
        print('Agent goes to {}'.format(agent.actions[action]))
        newState, reward = api.make_move(agent.actions[action], world)
        time.sleep(15)
        newStateX = int(newState['x'])
        newStateY = int(newState['y'])
        newState = [newStateX, newStateY]
        agent.learn(state, action, reward, newState)
        state = newState


if __name__ == "__main__":
    api = Api(1077, 1287)
    visit = visit_num()
    for i in range(50):
        current_world = int(api.get_location())
        print(current_world)
        if current_world in range(1, 11):
            print('Agent in world {}'.format(current_world))
            agent = QLearningAgent(current_world)
        else:
            world = decide_world(visit)
            print('Entering world {}.'.format(world))
            api.enter_world(world)
            agent = QLearningAgent(world)
        traverse(api, agent)
        store_visit(visit)
    print("Traverse done!")


