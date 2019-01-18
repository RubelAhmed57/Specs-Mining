from collections import Counter
import re

count = 0 #counter
events = [] #event list
support = {}
confidence = {}

# function to find ABorBA sequence
def support_ABorBA(l):
    a = l[0]
    b = l[1]
    count = 0
    #print(len(l))
    for i in range(0, len(l)-1):
        if(l[i] == a and l[i+1] == b ):
            count = count+1
            i = i+2
        else: i = i + 1
        support[str(a)+"->"+str(b)]= count
    count = 0
    for i in range(0, len(l)-1):
        if(l[i] == b and l[i+1] == a ):
            count = count+1
            i = i+2
        else: i = i + 1
        support[str(b)+"->"+str(a)] = count

#open event file and store events as a list
file = [x.split(' ')[0] for x in open('abstract_trace.txt').readlines()]
for event in file:
    events.append(int(" ".join(str(x) for x in re.findall(r'\d+', event)))) #converting list to string to find event list

#freq of each event
event_freq = Counter(events)


for i in range(0,len(events)-3348):# -1 default
    temp=[]
    for j in range(0,len(events)):
        if events[j] == events[i] or events[j] == events[i+1]:
            temp.append(events[j])
        if(len(temp)>1):
            support_ABorBA(temp)

#print(type(support))

#find confidence
for key in support:
    confidence[key] = support[key] / event_freq[int(key[0])]

#print(confidence)
with open("output.txt","w") as file:
    file.write("Frequency of each event: \n")
    #print(event_freq)
    for i in range(len(event_freq)):
          file.write(str(i)+": "+ str(event_freq[i])+"\n")
    file.write("\nSupport: \n")
    for key in support:
        file.write(key+": "+str(support[key])+"\n")
    file.write("\nConfidence: \n")
    for key in confidence:
         file.write(key+": "+str(confidence[key])+"\n")

print("Done!")