


def clear_list(lst):
    new_list = []
    for x in lst:
        if isinstance(x, list):
            new_list += clear_list(x)
        else:
            new_list.append(x)
    return new_list
    
    

mylist = [1, 2, 3, [4, 5, 6], [7, [8, 9, 10], 11], 12]
print(clear_list(mylist))


print(isinstance(mylist, list))
print(type(mylist, list))