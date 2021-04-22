from api import Api

worldId = 0
move = 'N'
x = 10

Api = Api(1077, 1287)
world_Id, state = Api.enter_world(worldId)
print("You have successfully entered world: ", world_Id)
print("You current state is: ", state)
reward, scoreIncrement, newState = Api.make_move(move, worldId)
print("reward:", reward)
print("score increment: ", scoreIncrement)
print("new state: ", newState)
my_world_location, my_state = Api.get_location()
print("You are in world ", my_world_location)
print("Your current state is ", my_state)
runs = Api.get_runs(1)
print(runs)
score = Api.get_score()
print('Your score: ', score)