import os
from requests import Session
from .decorators import check_response


class Trello(Session):
    
    root = 'https://api.trello.com/1'
    ENV_VARS = dict(
        key='TrelloKey',
        token='TrelloToken',
        )

    def __init__(self, **kwargs):
        super().__init__()
        self.reset_params()
        self._keys = []
        self.set_attributes(kwargs)

    def set_attributes(self, kwargs):
        if kwargs:
            for key in kwargs:
                self._keys.append(key)
                setattr(self, key, kwargs[key])
                
    def reset_params(self):
        keys = self.get_keys()
        self.params.update(keys)
        
    def get_keys(self):
        return {
            key:os.environ[item] 
            for key,item in self.ENV_VARS.items()
            }
    
    @check_response
    def get(self, endpoint, construct=True, **kwargs):
        if construct:
            url = self.construct_request(endpoint)
        else:
            url = endpoint
        response = super().get(url, **kwargs)
        try:
            return response.json()
        except:
            return response
        
    @check_response
    def put(self, endpoint, data={}, construct=True, **kwargs):
        if construct:
            url = self.construct_request(endpoint)
        else:
            url = endpoint
        
        return super().put(url, data=data, **kwargs)
    
    @check_response
    def post(self, endpoint, construct=True, **kwargs):
        if construct:
            url = self.construct_request(endpoint)
        else:
            url = endpoint
        
        return super().post(url, **kwargs)
    
    def delete(self, endpoint, construct=True, **kwargs):
        if construct:
            url = self.construct_request(endpoint)
        else:
            url = endpoint
        
        return super().delete(url, **kwargs)
        
    
    def construct_request(self, endpoint):
        return self.root + endpoint
    
    def to_dict(self):
        data = {}
        for key in self._keys:
            value = self.__dict__[key]
            if isinstance(value, list) and value and isinstance(value[0], Trello):
                value = [x.to_dict() for x in value]
            data[key] = value
        return data