d = {}
numbers = [1, 1, 1, 2, 3, 3, 5]
for i in numbers:
    if i in d:
        d[i] += 1
    else:
        d[i] = 1
print(d)