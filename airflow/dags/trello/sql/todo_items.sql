create table {{ params.schema }}.{{ params.table }} if not exists (
    id integer
  , list_id integer
  , card_id integer
  , todo_name varchar(286)
  , item_name varchar(286)
  , complete boolean
  , marked_complete_time timestamp
)