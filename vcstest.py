l = [5, 6, 5, 6, 5, 6, 5, 6, 5,5,5,6,6,6,6,5,5,6]
a = l[0]
b = l[1]
count = 0
print(len(l))
for i in range(0, len(l)-1):
    if(l[i] == a and l[i+1] == b ):
        count = count+1
        i = i+2
    else: i = i + 1

print(count)
