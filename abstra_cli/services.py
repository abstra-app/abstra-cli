from .apis import (
  add_workspace_packages,
  add_workspace_form,
  add_workspace_vars,
  delete_file,
  delete_workspace_form,
  delete_workspace_packages,
  delete_workspace_vars,
  list_workspace_files,
  list_workspace_vars,
  list_workspace_packages,
  list_workspace_forms,
  upload_file,
)

from .messages import (
  form_created_message
)

def add_code(name: str, code: str, **kwargs):
  data = add_workspace_form(name=name, code=code)
  form_id = data[0]['id']
  form_created_message(form_id)
  