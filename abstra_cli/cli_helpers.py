from .utils_config import get_auth_config, save_config

def request_api_token_from_user():
  saved_api_token, _ = get_auth_config()
  if saved_api_token:
      if update_api_token(saved_api_token):
        print('API Token updated!')
        return 
      print('API Token not changed.')
      return

  if create_api_token():
    print('API Token saved')
    return

  print('API Token not saved')

def update_api_token(saved_api_token):
  hidden_token = ''.join(['*']*(len(saved_api_token) - 4)) + saved_api_token[-4:]
  api_token = input(f"Abstra API Token [{hidden_token}]: ")
  if api_token:
    save_config({'api_token': api_token})
    return True
  return False

def create_api_token():
  api_token = input(f"Abstra API Token: ")
  if api_token:
    save_config({'api_token': api_token})
    return True
  return False