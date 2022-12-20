from .base import TrelloEndpoint
from ..decorators import return_factory, get, post, reset_params

class TrelloBoard(TrelloEndpoint):
    
    endpoint='/boards'
    
    @return_factory('card')
    @get
    def cards(self):
        return f'/cards'
    
    @return_factory('list')
    @get
    def lists(self, **kwargs):
        return f'/lists'
    
    def search_lists(self, name):
        lists = self.lists()
        for l in lists:
            if l.name.lower() == name.lower():
                return l
    
    @reset_params
    @return_factory('list')
    @post
    def add_list(self, name, pos='bottom'):
        self.params.update(
            {"name": name,
             "pos": pos})
        return {'endpoint':'/lists'}

    @return_factory("checklist")
    @get
    def checklists(self):
        return '/checklists'