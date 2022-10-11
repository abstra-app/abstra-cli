from .apis import (
  add_workspace_form,
  update_workspace_form
)

from .utils import remove_from_dict

from .messages import (
  form_created_message,
  form_updated_message
)

def add_form(name: str, code: str, **kwargs):
  data = add_workspace_form(name=name, code=code)
  form_id = data[0]['id']
  form_created_message(form_id)


def update_form(form_id: str, **kwargs):  
  print(form_id, kwargs)
  # data = update_workspace_form(form_id, **kwargs)
  # form_updated_message(form_id)

