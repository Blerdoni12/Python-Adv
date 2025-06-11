from enum import unique

my_set = {1,2,3}

my_set.add(7)
print(my_set)

my_set.remove(3)
print(my_set)

my_set.discard(8)
print(my_set)

my_set.clear()
print(my_set)

set_length=len(my_set)
print(set_length)

my_list=[1,2,2,3,4,4,5]

unique_set=set(my_list)

unique_list=list(unique_set)
print(unique_list)
