number=[12,9,28,3,1]
largest=second_largest=float('-inf')
for num in number:
    if num>largest:
        second_largest=largest
        largest=num
    elif num>second_largest and num!=largest:
        second_largest=num
print("first number:",largest)
print("second number:",second_largest)        
