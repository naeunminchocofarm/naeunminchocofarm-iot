list = [{"a": 11}]
print(list)
list_copy = list.copy()
list[0] = {"b": 22}
print(list_copy)
print(list)