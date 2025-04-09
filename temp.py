dict = {}
for i in range(5):
  list = dict.get('num')
  if not list:
    dict['num'] = []
  dict['num'].append(i)

print(dict)