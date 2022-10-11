def form_created_message(form_id: str):
  print(f'Form created successfully: {form_id}')

def form_updated_message(form_id: str):
  print(f'Form updated successfully: {form_id}')
  

def not_implemented(*args, **kwargs):
    print("Invalid command")

def required_argument(argument):
  print(f'required argument: [{argument}]')

def required_parameter(parameter):
  print(f'required parameter: --{parameter} [{parameter}]')

def invalid_variable(argument):
  print(f"invalid variable: {argument}")

def duplicate_variable(argument):
  print(f"duplicate variable: {argument}")
