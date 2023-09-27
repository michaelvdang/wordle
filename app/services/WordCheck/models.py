from pydantic import BaseModel

class Game(BaseModel):
    game_id: int
    word_id: int
    guess: str