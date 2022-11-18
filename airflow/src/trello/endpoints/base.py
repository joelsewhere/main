from ..base import Trello


class TrelloEndpoint(Trello):
    
    endpoint:str
    
    def construct_request(self, endpoint):
        return ''.join([
            self.root,
            self.endpoint,
            f'/{self.id}' if hasattr(self, 'id') else '',
            endpoint
        ])
    
    def __repr__(self):
        return f'<{self.__class__.__name__} name={self.name}>'
