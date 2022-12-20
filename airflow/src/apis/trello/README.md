# trello-sdk

## Board

### Get a board
```python
board_id = <board_id>
trello = TrelloAPI()
board = trello.get_board(board_id)
```

### Get board lists
```python
board.lists()
```

### Find specific list
```python
board.search_lists('done')
```

### Get board cards
```python
board.cards()
```

### Get board checklists
```python
board.checklists()
```

## Lists

### Get list cards
```python
board.search_lists('done').cards()
```

### Archive all cards in list
```python
board.search_lists('done').archive_all()
```

### Archive the list
```python
board.search_lists('done').archive()
```

## Cards

### Move card to the `Done` list.
```python
# Isolate card object
card = board.cards()[0]
# Move card
card.is_done()
```

### Move card to `To Do` list.
```python
card.is_todo()
```

### Move card to a different list
```python
lists = board.lists()
list_one = lists[0]
list_two = lists[1]
list_card = list_one.cards()[0]
list_card.move_card(list_two.id)
```




