ACCESS_TOKEN_FILE = 'access_token.txt'
REFRESH_TOKEN_FILE = 'refresh_token.txt'

def _get_token(file_name):
  with open(file_name, "r") as file:
    token = file.read()
    if token == '':
      return None
    return token
  
def _set_token(file_name, token):
  with open(file_name, 'w') as file:
    file.write(token)

def _delete_token(file_name):
  with open(file_name, 'w'):
    pass

def get_access_token():
  return _get_token(ACCESS_TOKEN_FILE)

def set_access_token(token):
  return _set_token(ACCESS_TOKEN_FILE, token)

def delete_access_token():
  return _delete_token(ACCESS_TOKEN_FILE)

# def get_refresh_token():
#   return _get_token(REFRESH_TOKEN_FILE)
  
# def set_refresh_token(token):
#   return _set_token(REFRESH_TOKEN_FILE, token)

# def delete_refresh_token():
#   return _delete_token(REFRESH_TOKEN_FILE)