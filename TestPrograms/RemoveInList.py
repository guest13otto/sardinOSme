messy_list = ["a", 2, 3, 1, False, [1, 2, 3]]

cleaned = [item for item in messy_list if isinstance(item,list)]

print(cleaned)
