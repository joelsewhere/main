from .base import TrelloEndpoint
from ..decorators import (return_factory, 
                          reset_params, 
                          get, 
                          put, 
                          post,
                          )


class TrelloList(TrelloEndpoint):
    
    endpoint = '/lists'
    
    @return_factory('card')
    @get
    def cards(self):
        return f'/cards'
    
    @post
    def archive_all(self):
        return {"endpoint": '/archiveAllCards'}
    
    @reset_params
    @return_factory("list")
    @put
    def archive(self):
        self.params.update({"value": "true"})
        return {"endpoint": "/closed"}