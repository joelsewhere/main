from functools import wraps

def filters(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        filter_ = ''
        filter_ += '?' + '&'.join(
            [f'{key}={value}'
             for key,value in kwargs.items()]
        )
        endpoint = func(*args, **kwargs)
        return endpoint + filter_
    return wrapper
        

def get(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        endpoint = func(*args, **kwargs)
        if isinstance(endpoint, str):
            endpoint = {"endpoint": endpoint}
        data = args[0].get(**endpoint)
        return data
    return wrapper

def delete(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        endpoint = func(*args, **kwargs)
        if isinstance(endpoint, str):
            endpoint = {"endpoint": endpoint}
        data = args[0].delete(**endpoint)
        return data
    return wrapper

def put(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload = func(*args, **kwargs)
        data = args[0].put(**payload)
        return data
    return wrapper

def post(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload = func(*args, **kwargs)
        data = args[0].post(**payload)
        return data
    return wrapper

def check_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        try:
            return response.json()
        except:
            return response
    return wrapper

def reset_params(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        output = func(*args, **kwargs)
        args[0].reset_params()
        return output
    return wrapper
    
    

def return_factory(type_):
    """
    Generates return type decorators.

    Example: 
    
    If an endpoint returns a list of courses, the api returns
    the courses as dictionaries. It is helpful to return
    those dictionaries as a CanvasCourse object instead.

    To do so, a CanvasCourse decorator is made by:
    ```
    course = return_factory('course')
    ```

    Then the decorator can be imported into a module
    ```
    from ..decorators import course
    ```

    And placed above an instance method
    ```
    @course
    def method(self):
    ```
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw):
            return_type = type_factory(type_)
            result = func(*args, **kw)
            if isinstance(result, dict):
                return return_type(**result)
            elif isinstance(result, list):
                return [return_type(**data) for data in result]
        return wrapper
    return decorator

def type_factory(type_):
    """
    There are some circular imports happening between the different endpoint modules.
    (CanvasCourse.get_users returns CanvasUser objects
     & CanvasUser.get_courses returns CanvasCourse objects)

    The imports are placed inside this function so the module objects
    can be full constructed, and the imports are only activated
    when needed/after the module objects are constructed.
    
    """
    if type_ == "board":
        from .endpoints.boards import TrelloBoard as type_
    elif type_ == "list":
        from .endpoints.lists import TrelloList as type_
    elif type_ == "card":
        from .endpoints.cards import TrelloCard as type_
    elif type_ == "checklist":
        from .endpoints.checklists import TrelloCheckList as type_
    elif type_ == "checkitem":
        from .endpoints.checklists import TrelloCheckItem as type_

    return type_