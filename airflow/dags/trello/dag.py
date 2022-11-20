from airflow.decorators import dag, task
from src.trello.api import TrelloAPI

BOARD_ID = <board id>
get_board = lambda: TrelloAPI().get_board(BOARD_ID)

@dag('trello_data')
def trello_data():

    @task
    def lists():
        board = get_board()
        lists = board.lists()
        # Push lists to xcom

    @task
    def cards():
        # Pull lists from xcom
        lists = []
        cards = [list.cards() for list in lists]

        # Push cards to xcom
    
    @task
    def todos():
        board = get_board()
        todos = board.checklists()

        # Push checklist.checkItems to xcom

    @task
    def load_lists():
        # Pull lists
        lists = []

    @task
    def load_cards():
        # Pull cards
        cards = []

    @task 
    def load_todos():
        # Pull todos
        todos = []


# TODO: Set task dependencies
# TODO: Fill in xcom pseudo code
# TODO: Set board id
# TODO: Fill in load pseudo code



