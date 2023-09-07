import httpx
from fastapi import FastAPI, Depends, Body, Query
import random
from models import Game
import json
import asyncio

app = FastAPI()

@app.get('/')
def test():
    return {'message' : 'Orchestrator.py'}

@app.post('/game/new', status_code=201)
def start_new_game(user_name: str):# = Body()):
    # find user_id
    res = httpx.get('http://localhost:9000/api/v1/stats?user_name=' + user_name)
    guid = res.json()

    # deny when there wrong user_name is given
    if guid == -1:
        return {'game_id' : -1, 'status': 'error', 'message': 'user does not exist'}

    # choose new game_id 
    answers = httpx.get('http://localhost:9100/api/v1/answers/count')
    game_id = random.randint(100, answers.json()['count'])
    # print('new guid: ' + guid)
    # create new game
    # new_game = httpx.post('http://localhost:9300/api/v1/play?guid=' + '1' + 
    #                             '&game_id=' + str(game_id))
    new_game = httpx.post('http://localhost:9300/api/v1/play?guid=' + (guid) + 
                                '&game_id=' + str(game_id))
    return {'status' : 'new game created', 'guid' : guid, 'game_id' : game_id, **new_game.json()}





    # async def find_user_id():
    #     async with httpx.AsyncClient() as client:
    #         # find user_id
    #         user_id = await client.get('http://localhost:9000/api/v1/stats?user_name=' + user_name)
    #         # user_id = user.json()
    #         if user_id == -1:
    #             return {'user_id' : -1, 'error': 'user does not exist'}
    #         else:
    #             return {'user_id' : user_id}

    # async def get_new_game_id():
    #     async with httpx.AsyncClient() as client:
    #         # choose new game_id 
    #         answers = await client.get('http://localhost:9100/api/v1/answers/count')
    #         return {'new_game_id' : random.randint(100, answers.json()['count']) + 100 - 1}

    # async def api_calls():
    #     results = await asyncio.gather(find_user_id(), get_new_game_id())
    #     return results[0]
    #     user_id = results[0]['user_id']
    #     game_id = results[1]['new_game_id']
    #     # create new game
    #     # new_game = httpx.post('http://localhost:9300/api/v1/play?user_id=' + '1' + 
    #     #                             '&game_id=' + str(results[1]['new_game_id'])).json()
    #     new_game = httpx.post('http://localhost:9300/api/v1/play?user_id=' + str(user_id) + 
    #                                 '&game_id=' + str(game_id)).json()
    #     if results[0]['user_id'] == -1:
    #         return {'user_id' : -1, 'error': 'user does not exist'}
    #     return {'user_id' : user_id, 'game_id' : game_id, **new_game}
        
    # return asyncio.run(api_calls())




@app.post('/game/{game_id}', status_code=201)
def add_guess(*, guid: str = Query(default=None), game_id: int, guess: str):
    # check word is valid and has guesses_remaining

    async def validate_word():
        async with httpx.AsyncClient() as client: 
            # check that guess is_valid
            _validate_word_future = await client.get('http://localhost:9200/api/v1/word/is-valid/' + guess)
            validate_word = _validate_word_future.json()
            return validate_word['is_valid_word']

    async def has_guesses_remaining():
        async with httpx.AsyncClient() as client:
            # check game has guesses remaining
            _curr_game_future = await client.get('http://localhost:9300/api/v1/play?guid=' + str(guid) + 
                                        '&game_id=' + str(game_id))
            curr_game = _curr_game_future.json()
            return {'remain': int(curr_game['remain'])}

    async def validate_move():
        return await asyncio.gather(validate_word(), has_guesses_remaining())

    results = asyncio.run(validate_move())

    if not results[0]:
        return {'status': 'error', 'message': 'Invalid guess, try again'}
    if int(results[1]['remain']) < 1:
        return {'status': 'error', 'message': 'Impossible, user is out of guesses'}

    # record and check if guess is correct

    async def record_guess():
        async with httpx.AsyncClient() as client:
            # record the guess and update number of guesses remaining
            _curr_game_future = await client.put('http://localhost:9300/api/v1/play?guid=' + 
                            str(guid) + '&game_id=' + str(game_id) + '&guess=' + guess)
            curr_game_result = _curr_game_future.json()
            return curr_game_result
    
    async def check_guess():
        async with httpx.AsyncClient() as client:
            # check to see if guess is correct
            game = {'game_id' : game_id, 'word_id' : game_id-99, 'guess' : guess}
            _word_check_result_future = await client.post(
                            'http://localhost:9100/api/v1/answers/check', 
                            data=json.dumps(game))
            word_check_result = _word_check_result_future.json()
            return word_check_result

    async def record_and_check_guess():
        return await asyncio.gather(record_guess(), check_guess())

    curr_game_result, word_check_result = asyncio.run(record_and_check_guess())

    # WIN: guess is correct, they are all 2's? 
    # 1. record the win
    if word_check_result.count(2) == 5:
        # from UserStatsRedis.py, to store game result in SQLite
        # class Result(BaseModel):
            # guesses: int
            # won: bool
        game_result = {'guesses': 6 - curr_game_result['remain'], 'won' : True}
        httpx.post('http://localhost:9000/api/v1/stats/' + str(guid) + '/' + str(game_id), 
                                                data=json.dumps(game_result)).json()
    # 2. retrieve user's score to return
        return {**(curr_game_result), 'won': True}

    # LOSE: guess is incorrect and no guesses remain
    elif int(curr_game_result['remain']) == 0:
        # 1. record the loss
        game_result = {'guesses' : 6, 'won' : False}
        httpx.post('http://localhost:9000/api/v1/stats/' + str(guid) + '/' + str(game_id), 
                                                data=json.dumps(game_result)).json()
        # 2. Retrieve winning word
        async def get_game_answer():
            async with httpx.AsyncClient() as client:
                return (await client.get('http://localhost:9100/api/v1/answers/correct?game_id=' + str(game_id))).json()
        answer = asyncio.run(get_game_answer())

        # 3. return user's score
        
        return {'answer': answer['word'], **(curr_game_result), 'won': False}

    # CONT: guess is incorrect and guesses remain
    else:
        # return {'status' : 'incorrect',
        #             'remaining' : curr_game['game'][0],
        #             'letters' : {
        #                 'correct' : [],
        #                 'present' : []
        #             }}
        return {'guess_results': word_check_result, **(curr_game_result)}

    # # check that guess is_valid
    # validate_result = httpx.get('http://localhost:9200/api/v1/word/is-valid/' + guess).json()
    # if validate_result['is_valid'] == False:
    #     return 'Invalid guess, try again'

    # # check game has guesses remaining
    # curr_game = httpx.get('http://localhost:9300/api/v1/play?user_id=' + str(user_id) + 
    #                             '&game_id=' + str(game_id)).json()

    # if curr_game['guesses_remain'] < 1:
    #     return 'Impossible, user is out of guesses'




    # # record the guess and update number of guesses remaining
    # curr_game = httpx.put('http://localhost:9300/api/v1/play?user_id=' + str(user_id) + 
    #                         '&game_id=' + str(game_id) + '&guess=' + guess).json()
    
    # # check to see if guess is correct
    # game = {'game_id' : game_id, 'word_id' : game_id-99, 'guess' : guess}
    # word_check_result = httpx.post('http://localhost:9100/api/v1/answers/check', 
    #                 data=json.dumps(game)).json()





    # # guess is correct, they are all 2's? 
    # # 1. record the win
    # if word_check_result.count(2) == 5:
    #     game_result = {'num_guesses' : 6 - int(curr_game['game'][0]), 'won' : True}
    #     httpx.post('http://localhost:9000/api/v1/stats/' + str(user_id) + '/' + str(game_id), 
    #                                             data=json.dumps(game_result)).json()
    # # 2. retrieve user's score to return
    #     return {'game_result' : {**game_result, 'guesses' : curr_game['game'][1:]}}



    # # guess is incorrect and no guesses remain
    # elif int(curr_game['game'][0]) == 0:
    #     # 1. record the loss
    #     game_result = {'num_guesses' : 6, 'won' : False}
    #     httpx.post('http://localhost:9000/api/v1/stats/' + str(user_id) + '/' + str(game_id), 
    #                                             data=json.dumps(game_result)).json()
    #     # 2. return user's score
    #     return {'game_result' : {**game_result, 'guesses' : curr_game['game'][1:]}}




    # # guess is incorrect and guesses remain
    # else:
    #     return word_check_result

    