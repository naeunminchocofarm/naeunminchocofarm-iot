import json

str = '{"name": "alice", "age": 25.6}'
data = json.loads(str)
print('name:', data['name'])
print('age:', data['age'])