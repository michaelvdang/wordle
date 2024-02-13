import httpx
from fastapi import FastAPI, Depends, Body, Query
from fastapi.middleware.cors import CORSMiddleware
import random
from models import Game
import json
import asyncio
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

SERVER_IP = os.environ.get('SERVER_IP')
DOMAIN_NAME = os.environ.get('DOMAIN_NAME')
## switch between running individual services or docker compose (same network)
## DEBUGGING: use 'localhost' and run: uvicorn Orchestrator:app --port 9400 --reload
# APP_HOST = 'localhost'
APP_HOST = 'docker'
endpoints = {
    'localhost': {
        'stats': 'http://localhost:9000',
        'wordcheck': 'http://localhost:9100',
        'wordvalidation': 'http://localhost:9200',
        'play': 'http://localhost:9300',
        'orc': 'http://localhost:9400',
    },
    'docker': {
        'stats': 'http://stats:9000',
        'wordcheck': 'http://wordcheck:9100',
        'wordvalidation': 'http://wordvalidation:9200',
        'play': 'http://play:9300',
        'orc': 'http://orc:9400',
    }
}

# app = FastAPI()
origins = [     # curl and local browser are always allowed
    "http://localhost:5173",    # needs this even when React App is local and Orc is remote
    "https://mikespace.xyz",
    "https://mikespace.dev", # DO NOT USE backslash (/)
    "http://" + str(SERVER_IP),
    "http://" + str(DOMAIN_NAME),
    "https://" + str(DOMAIN_NAME),
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

app = FastAPI(middleware=middleware)

@app.get('/')
def test():
    return {'message' : 'Orchestrator.py',
            'SERVER_IP': SERVER_IP}

@app.post('/game/new', status_code=201)
def start_new_game(username: str):# = Body()):
    username = username.lower()
    # find user_id
    # res = httpx.get('http://localhost/stats/id/' + username)    # for running local
    # res = httpx.get('http://stats:9000/stats/id/' + username)    # for container
    res = httpx.get(endpoints[APP_HOST]['stats'] + '/stats/id/' + username)    # for container
    user = res.json()

    # create new user when there wrong username is given
    if user == -1:
        # res = httpx.post('http://localhost/stats/stats/users/new?username=' + username)
        # res = httpx.post('http://stats:9000/stats/users/new?username=' + username)
        res = httpx.post(endpoints[APP_HOST]['stats'] + '/stats/users/new?username=' + username)
        user = res.json()['user']

    # choose new game_id 
    # answers = httpx.get('http://localhost:9100/answers/count')   # use localhost for non container
    # answers = httpx.get('http://wordcheck:9100/answers/count')   # use localhost for non container
    answers = httpx.get(endpoints[APP_HOST]['wordcheck'] + '/answers/count')   # use localhost for non container
    game_id = random.randint(100, answers.json()['count'])
    # print('new guid: ' + guid)
    # create new game
    print('new guid: ' + user['guid'])
    print('new game_id: ' + str(game_id))
    # new_game = httpx.post('http://localhost/play/play?guid=' + (user['guid']) + 
    # new_game = httpx.post('http://play:9300/play?guid=' + (user['guid']) + 
    new_game = httpx.post(endpoints[APP_HOST]['play'] + '/play?guid=' + (user['guid']) + 
                                '&game_id=' + str(game_id))
    return {'status' : 'new game created', 
            'guid' : user['guid'], 
            'user_id' : user['user_id'], 
            'game_id' : game_id, **new_game.json()}


@app.post('/game/{game_id}', status_code=201)
def add_guess(*, game_id: int, username: str, guid: str, user_id: int, guess: str):
    username = username.lower()
    # check word is valid and has guesses_remaining

    async def validate_word():
        async with httpx.AsyncClient() as client: 
            # check that guess is_valid
            # _validate_word_future = await client.get('http://localhost:9200/word/is-valid/' + guess)
            # _validate_word_future = await client.get('http://wordvalidation:9200/word/is-valid/' + guess)
            _validate_word_future = await client.get(endpoints[APP_HOST]['wordvalidation'] + 
                                                     '/word/is-valid/' + guess)
            validate_word = _validate_word_future.json()
            return validate_word['is_valid_word']

    async def has_guesses_remaining():
        async with httpx.AsyncClient() as client:
            # check game has guesses remaining
            # _curr_game_future = await client.get('http://play:9300/play?guid=' + str(guid) + 
            _curr_game_future = await client.get(endpoints[APP_HOST]['play'] + '/play?guid=' + str(guid) + 
                                        '&game_id=' + str(game_id))
            curr_game = _curr_game_future.json()
            try:
                return {'remain': int(curr_game['remain'])}
            except KeyError as e:
                return {'Error': 'Game not found, wrong guid or game_id'}

    async def validate_move():
        return await asyncio.gather(validate_word(), has_guesses_remaining())

    results = asyncio.run(validate_move())

    if not results[0]:
        return {'status': 'error', 'message': 'Invalid guess, try again'}
    # if results[1]['status'] == 'error':
    #     return {'status': 'error', 'message': 'NOT SURE'}
    if int(results[1]['remain']) < 1:
        return {'status': 'error', 'message': 'Impossible, user is out of guesses or this game does not exists yet'}

    # record and check if guess is correct

    async def record_guess():
        async with httpx.AsyncClient() as client:
            # record the guess and update number of guesses remaining
            # _curr_game_future = await client.put('http://play:9300/play?guid=' + 
            _curr_game_future = await client.put(endpoints[APP_HOST]['play'] + '/play?guid=' + 
                            str(guid) + '&game_id=' + str(game_id) + '&guess=' + guess)
            # NOTE: present_letters, absent_letters, game_progress are not used 
            # add something like: word_check_results = {'guess_results': word_check_result}
            # and have play append the results to a results string like: '01200|20210|'
            curr_game_result = _curr_game_future.json()
            return curr_game_result
    
    async def check_guess():
        async with httpx.AsyncClient() as client:
            # check to see if guess is correct
            game = {'game_id' : game_id, 'word_id' : game_id-99, 'guess' : guess}
            _word_check_future = await client.post(
                            # 'http://localhost:9100/answers/check', 
                            # 'http://wordcheck:9100/answers/check', 
                            endpoints[APP_HOST]['wordcheck'] + '/answers/check', 
                            data=json.dumps(game))
            word_check = _word_check_future.json()
            print(word_check)
            return word_check

    async def record_and_check_guess():
        return await asyncio.gather(record_guess(), check_guess())

    curr_game_result, word_check = asyncio.run(record_and_check_guess())

    # WIN: guess is correct, they are all 2's? 
    # 1. record the win
    print('word_check: ', word_check)
    if word_check['results'].count(2) == 5:
        game_result = {'guesses': 6 - int(curr_game_result['remain']), 'won' : True, 'completed' : True}
        print('Orchestrator.py game_result: ', game_result)
        # httpx.post('http://stats:9000/stats/games/store-result?username=' + str(username) + '&user_id=' + str(user_id) + '&game_id=' + str(game_id), 
        httpx.post(endpoints[APP_HOST]['stats'] + '/stats/games/store-result?username=' + str(username) 
                            + '&user_id=' + str(user_id) + '&game_id=' + str(game_id), 
                   data=json.dumps(game_result)).json()
    # 2. retrieve user's score to return
        return {'guess_results': word_check['results'], 
                **(curr_game_result), 
                'won': True, 
                'completed' : True}

    # LOSE: guess is incorrect and no guesses remain
    elif int(curr_game_result['remain']) == 0:
        # 1. record the loss
        game_result = {'guesses' : 6, 'won' : False, 'completed' : True}
        # httpx.post('http://stats:9000/stats/games/store-result?username=' + str(username) + '&user_id=' + str(user_id) + '&game_id=' + str(game_id), 
        httpx.post(endpoints[APP_HOST]['stats'] + '/stats/games/store-result?username=' + str(username) 
                                    + '&user_id=' + str(user_id) + '&game_id=' + str(game_id), 
                    data=json.dumps(game_result)).json()
        # 2. Retrieve winning word
        async def get_game_answer():
            async with httpx.AsyncClient() as client:
                # return (await client.get('http://wordcheck:9100/answers/correct?game_id=' + str(game_id))).json()
                return (await client.get(endpoints[APP_HOST]['wordcheck'] 
                                         + '/answers/correct?game_id=' + str(game_id))).json()
        answer = asyncio.run(get_game_answer())

        # 3. return user's score
        
        return {'guess_results': word_check['results'], 'answer': answer['word'], **(curr_game_result), 'won': False, 'completed' : True}

    # CONT: guess is incorrect and guesses remain
    else:
        # modify curr_game_result here to include word check results and update game progress
        # figure out how to store absent letters and present letters
        # they don't need to be a set because the max length is only 25
        return {'guess_results': word_check['results'], **(curr_game_result), 'won': False, 'completed' : False}

@app.get('/game/restore')
def restore_game(username: str, game_id: int):
    '''
    return {'result': 0} if there is no data in Redis
    return {'result': 1, **user, **game_data} if there is data in Redis
    '''
    # res = httpx.get('http://stats:9000/stats/id/' + username)
    res = httpx.get(endpoints[APP_HOST]['stats'] + '/stats/id/' + username)
    user = res.json()
    # user is not in DB, must be a new user
    if user == -1:
        return {'result': 0}
    
    # restore game from Play API
    # res = httpx.get('http://play:9300/play?guid=' + (user['guid']) + '&game_id=' + str(game_id))
    res = httpx.get(endpoints[APP_HOST]['play'] + '/play?guid=' + (user['guid']) 
                    + '&game_id=' + str(game_id))
    game_data = res.json()
    # if in redis, game_data = {'remain': 3, 'guess1': 'angry', ...}
    # if not in redis, game_data = {'status': 'success'}
    print('user: ', user, 'game_data: ', game_data)
    if 'remain' in game_data and int(game_data['remain']) > 0:
        return {**user, **game_data, 'game_id': game_id, 'result': 1}
    # if not found, start new game
    else: 
        return {'result': 0, 'message': 'Game does not exist in database'}