from api import Api
import numpy as np
import pickle
import time
from qLearning import QLearningAgent


# loading the visit history
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


# storing the visit history
def store_visit(v):
    pickle.dump(v, open('visit', 'wb'))
    print('Updating visit history')


# decide which world to enter
def decide_world(v):
    world = 1
    visited = v[world]
    for i in range(1, 11):
        if v[i] < visited:
            world = i
            visited = v[i]
    return world


# check the real movement
# there is a chance that agent does not go where you decide to go
def check_real_move(state,newState):
    # actions = ['N', 'S', 'E', 'W']
    newX = newState[0]
    newY = newState[1]
    x = state[0]
    y = state[1]
    if newX == x:
        check_y = newY - y
        if check_y == 1:
            return 0
        elif check_y == -1:
            return 1
    else:
        check_x = newX - x
        if check_x == 1:
            return 2
        elif check_x == -1:
            return 3


# traverse a world until exit
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
        newState, reward = api.make_move(agent.actions[action], world)
        time.sleep(15)
        newStateX = int(newState['x'])
        newStateY = int(newState['y'])
        newState = [newStateX, newStateY]
        action = check_real_move(state, newState)
        print('Agent goes to {}'.format(agent.actions[action]))
        agent.learn(state, action, reward, newState)
        state = newState


if __name__ == "__main__":
    api = Api(1077, 1287)
    visit = visit_num()
    for i in range(50):
        current_world = int(api.get_location())
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


