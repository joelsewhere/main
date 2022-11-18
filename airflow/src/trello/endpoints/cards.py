from .base import TrelloEndpoint
from ..decorators import (return_factory, 
                          get, 
                          put, 
                          delete, 
                          reset_params, 
                          post,
                          )


class TrelloCard(TrelloEndpoint):
    
    endpoint = '/cards'
    
    @return_factory('board')
    @get
    def get_board(self):
        return '/board'
    
    @put
    def is_done(self):
        list_id = self.get_board().search_lists('done').id
        return self.move_card(list_id)
    
    @put
    def move_card(self, list_id):
        return {
            "endpoint": '',
            "data": {
                'idList': list_id
            }
        }
    
    @delete
    def delete_card(self):
        return ''
    
    @return_factory("checklist")
    @get
    def checklists(self):
        return '/checklists'
        
    def is_todo(self):
        list_id = self.get_board().search_lists('to do').id
        return self.move_card(list_id)
    
    @reset_params
    @post
    def add_comment(self, text):
        self.params.update({"text": text})
        return {
            "endpoint": '/actions/comments'
        }
        
    @reset_params
    @return_factory('card')
    @post
    def add_card(self, idList, desc='', pos='bottom'):
        self.params.update(
            {
                "name": self.name,
                "desc": desc,
                "idList": idList,
                "pos": pos
                }
            )
        return {"endpoint": ''}
    
    @reset_params
    @return_factory('checklist')
    @post
    def add_checklist(self, name, pos='bottom'):
        self.params.update(
            {"name":name, "pos":pos}
        )
        return {'endpoint':'/checklists'}
    
    @delete
    def delete_checklist(self, checklist_id):
        return f'/checklists/{checklist_id}'
