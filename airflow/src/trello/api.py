
from .base import Trello
from .decorators import return_factory, get


class TrelloAPI(Trello):
    
    @return_factory('board')
    @get
    def get_board(self, board_id):
        return f"/boards/{board_id}"