print("Basic step: specs Mining!")

import re
count = 0
events = []
freq_list =[]
fresh = []
file = [x.split(' ')[0] for x in open('abstract_trace.txt').readlines()]
#print(file)
for event in file:
    events.append(int(" ".join(str(x) for x in re.findall(r'\d+', event)))) #converting list to string

for event in range(0,max(events)+1):  #finding freq of each event
    freq_list.append(events.count(event))

for event in range(len(events)):
        if (events[event] == 0) and (events[event+1] == 1):
            count = count + 1


print(count)
#print(fresh)

# with open('abstract_trace.txt') as f:
#     print (zip(*[line.split() for line in f])[1])
# with open("abstract_trace.txt") as file:
#     for line in file:
#         events.append(line[0])
     #data = list(file)
     #print(file.read(10));
# list =[1,2,2,1,3,2,1,2,3,4]
# print(list.count(1))
# print(events)