from collections import *
from itertools import permutations as pm
import time, os
import re,csv


start_time = time.time()
count = 0 #counter
events = [] #event list from the sequence
unique_events=[] #collection of all unique events
support = {}
confidence = {}
sublist_length = {}


events = []#[1,2,1,3] # these input for testing only.
input = 2

#start reading here!
#open event file and store events as a list
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, './Abstract Traces/10.tstt.txt')
file = [x.split(' ')[0] for x in open(file_path,"r").readlines()]
for event in file:
    events.append(int(" ".join(str(x) for x in re.findall(r'\d+', event)))) #converting list to string to find event list

B =  events
#print(events)
#freq of each event
event_freq = Counter(events)

unique_events = list(set(events))

def find_support(A,B):
    index = {}
    for i, n in enumerate(B):
        index.setdefault(n, deque()).append(i)
    count = 0
    while True:
        last = -1
        try:
            for n in A:
                while True:
                    i = index[n].popleft()
                    if i > last:
                        last = i
                        break
        except (IndexError, KeyError):
            break
        count += 1
    if count>=50: #support input
        #print(type(A),A)
        support[A] = count

for i in range(2, input+1):
    event_group = pm(unique_events,i)
    for groups in event_group:
        #print(list(groups))
        temp = [x for x in events if x in groups]
        sublist_length[groups] = len(temp)
        #print(groups,temp)
        find_support(groups,temp)

#find confidence
for key in support:
    #print(key,support[key],end =": ")
    #print(key[0:-1])
    #print(event_freq[key[0]])
    if len(key) == 2:
        confidence[key] = support[key] / event_freq[key[0]],support[key] / event_freq[key[1]]
    else:
        try:
            confidence[key] = support[key] / support[key[0:-1]]
            #print(key, " : ", support[key[0:-1]])
        except ZeroDivisionError:
            confidence[key] = 0

outlist=[]
for key in support:
    if confidence[key][0] > 0.10: #confidence input

        l = [key,support[key],round(confidence[key][0],3),round(confidence[key][1],3),round((support[key]*len(key)/sublist_length[key]),3)] #key = each rule
        outlist.append(l)
#showing the results in csv file:
headr = ["Rule","support"," forward confidence", "backword confidence", "Frequency"]
headr2 =["event","frequence"]
eventl=[]

print(outlist)
# for key in event_freq:
#     l = [key,event_freq[key]]
#     eventl.append(l)
#
# with open('./outs/test10.csv', 'wt', newline='') as file:
#     writer = csv.writer(file, delimiter=',')
#     writer.writerow(i for i in headr2)
#     for j in eventl:
#         writer.writerow(j)
#     writer.writerow(i for i in headr)
#     for j in outlist:
#         writer.writerow(j)

#print(sublist_length)
# print("freq: ", event_freq)
# print("support:",support)
print("confidence:",confidence)
print ("time elapsed: {:.2f}s".format(time.time() - start_time))