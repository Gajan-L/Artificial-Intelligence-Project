import requests
import json

user = {1077: {'x-api-key': '9d3e5f9dad56739bccc0', 'userId': '1077'}}

class Api:
    def __init__(self, user_id, team_id):
        self.COM_HEADER = {'Host': 'www.notexponential.com',
                           'Accept': 'text/html',
                           'Connection': 'keep-alive',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

        self.COM_HEADER.update(user[user_id])
        self.URL = 'http://www.notexponential.com/aip2pgaming/api/index.php'
        self.URL_GW = 'https://www.notexponential.com/aip2pgaming/api/rl/gw.php'
        self.URL_Score = 'https://www.notexponential.com/aip2pgaming/api/rl/score.php'

        self.TEAM_ID = team_id

    @staticmethod
    def check_response_validity(res):
        if res.status_code != 200:
            raise Exception('Http request fail. Status code: ' + str(res.status_code) + '\nContent: ' + res.text)
        js = json.loads(res.text)
        if js['code'] != 'OK':
            raise Exception('Api request fail. Reason: ' + js['message'])

    def get_team_member(self):
        # just for testing the connection with server
        # nothing to do with the project
        cus_para = {'type': 'team', 'teamId': self.TEAM_ID}
        response = requests.get(self.URL, headers=self.COM_HEADER, params=cus_para)
        self.check_response_validity(response)
        return json.loads(response.text)['userIds']

    def get_location(self):
        # get current location
        # example response from api:
        # {"code":"OK","world":"0","state":"0:1"}
        # return: my_world_location, my_state
        cus_data = {'type': 'location', 'teamId': self.TEAM_ID}
        response = requests.get(self.URL_GW, headers=self.COM_HEADER, params=cus_data)
        self.check_response_validity(response)
        my_world_location = json.loads(response.text)['world']
        my_state = json.loads(response.text)['state']
        return my_world_location, my_state

    def enter_world(self, worldId):
        # enter a World
        # example response from api:
        # {"code":"OK","worldId":0,"runId":65,"state":"0:0"}
        # return: world_Id, state
        cus_data = {'type': 'enter', 'teamId': self.TEAM_ID, 'worldId': worldId}
        response = requests.post(self.URL_GW, headers=self.COM_HEADER, data=cus_data)
        self.check_response_validity(response)
        world_Id = json.loads(response.text)['worldId']
        run_Id = json.loads(response.text)['runId']
        state = json.loads(response.text)['state']
        return world_Id, state

    def make_move(self, move, worldId):
        # make a move
        # example return from api:
        # {"code":"OK","worldId":0,"runId":"65","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.1000000000000000055511151231257827021181583404541015625,"newState":{"x":"0","y":1}}
        # return: reward, scoreIncrement, newState
        cus_data = {'type': 'move', 'teamId': self.TEAM_ID, 'worldId': worldId, 'move': move}
        response = requests.post(self.URL_GW, headers=self.COM_HEADER, data=cus_data)
        self.check_response_validity(response)
        world_Id = json.loads(response.text)['worldId']
        run_Id = json.loads(response.text)['runId']
        reward = json.loads(response.text)['reward']
        scoreIncrement = json.loads(response.text)['scoreIncrement']
        newState = json.loads(response.text)['newState']
        return reward, scoreIncrement, newState

    def get_runs(self, x):
        # get last x runs
        # example response from api:
        # {"runs":[{"runId":"14","teamId":"1077","gworldId":"0","createTs":"2021-04-20 12:50:13","score":"-0.1","moves":"1"}],"code":"OK"}
        # return: runs
        cus_data = {'type': 'runs', 'teamId': self.TEAM_ID, 'count': x}
        response = requests.get(self.URL_Score, headers=self.COM_HEADER, params=cus_data)
        self.check_response_validity(response)
        runs = json.loads(response.text)['runs']
        return runs

    def get_score(self):
        # get score
        # example return:
        # {"score":0,"code":"OK"}
        # return: score
        cus_data = {'type': 'score', 'teamId': self.TEAM_ID}
        response = requests.get(self.URL_Score, headers=self.COM_HEADER, params=cus_data)
        self.check_response_validity(response)
        score = json.loads(response.text)['score']
        return score