from .base import TrelloEndpoint
from ..decorators import (return_factory,
                          reset_params,
                          delete,
                          post,
                          get,
                          put,
                          )


class TrelloCheckList(TrelloEndpoint):
    
    endpoint = '/checklists'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        if hasattr(self, "checkItems"):
            self.checkItems = (
                return_factory("checkitem")
                (lambda: self.checkItems)()
                )
            for item in self.checkItems:
                item.set_attributes({"idCard": self.idCard})
            
    @delete
    def delete_checklist_item(self, itemid):
        return f'/checkItems/{itemid}'
    
    @reset_params
    @return_factory('checkitem')
    @post
    def add_checklist_item(self, name, pos='bottom', checked='false'):
        self.params.update(
            {"name": name,
             "pos": pos,
             "checked": checked}
        )
        return {'endpoint':'/checkitems'}
    
    @return_factory('card')
    @get
    def get_card(self):
        return '/cards'


class TrelloCheckItem(TrelloEndpoint):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def construct_request(self, endpoint):
        return f'{self.root}/cards/{self.idCard}/checkItem/{self.id}' + endpoint
    
    @reset_params
    @put
    def is_done(self):
        self.params.update({"state": "complete"})
        return {"endpoint": "",}
    
    @reset_params
    @put
    def is_todo(self):
        self.params.update({"state": "incomplete"})
        return {"endpoint": "",}
