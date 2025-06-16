count = 1

while count <= 5:
    print("iteration",count)
    count += 1

#loop control statements
#breal

numbers=[1,2,3,4,5,6,7]
target=4

for number in numbers:
    print(number)
    if number == target:
        print("target found!")
        break

#continue
scores=[68,20,57,48,92,72,73]
total=0
count=0

for score in scores:
    if score <50:
        continue
    # total += score
    # count += 1

    # average = total / count if count > 0 else 0

    # print("Average score for scores above 50:",average)
    print(score)

    
