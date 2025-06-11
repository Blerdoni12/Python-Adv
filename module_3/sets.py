#creating a set using curly brackets
my_set = {1,2,3}

#creating a set from a list using the set() fucntion
my_set1= set([4,5,6])

#creating an empty set using the set() function
my_set2=set()

my_set3={1,2,2,3,3,3,3}
print(my_set3)

#set operations

#union
set1={1,2,3}
set2={3,4,5}

union_result_method= set1.union(set2)
union_result_operator=set1 | set2

print(union_result_method)
print(union_result_operator)

#intersection
intersection_result_method= set1.intersection(set2)
intersection_result_operator= set1 & set2

print(intersection_result_method)
print(intersection_result_operator)

#difference
difference_result_method=set1.difference(set2)
difference_result_operator=set1-set2

print(difference_result_method)
print(difference_result_operator)

#symetric difference
sd_result_method=set1.symmetric_difference(set2)
sd_result_operator=set1 ^ set2

print(sd_result_method)
print(sd_result_operator)








