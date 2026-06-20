res = []
def merge(a, b):
    return a + b

for x in [1, 2]:
    for y in [3, 4]:
        res.append(merge(x, y))
print(res)