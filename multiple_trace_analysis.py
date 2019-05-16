from collections import *
from itertools import permutations as pm
import time, os
import re, csv

#**************************************variable declaration area*********************************
map = {} # holds events and their corresponding msgs
events = [] # all unique events in the trace
trace = []  # trace in a list after parsing, it is sublisted accoriding to clocks
freq_trace = [] # flat list of trace regardless of clock to calculate the support for each event
event_support = {} # support for each event
rule_support ={}
confidence = {}
RuleCount = {}
input_length = 2
stack = []

last_rule_lenth1 = 0 # to prevent adding suffix rules
last_rule_lenth2 = 0 # to prevent adding suffix rules
base = []
counter = 0

# with open("Mapping info.txt", "r", encoding='utf-8-sig') as fileobj:
#   for line in fileobj:
#       temp = line.split(":")
#       events.append(int(temp[0]))
#       map[int(temp[0])] = temp[1:]

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
    if count> 0: #support input
        #print(len(A))
        rule_support[tuple(A)] = count
    else:
        pass

# files = os.listdir('./inputs/testinputs')
# print(files)
files = ['sample_input.txt','inputTest1.txt']
for FILE in files:
    # print(FILE)
    if FILE.endswith('.txt'):
        with open(FILE, "r", encoding='utf-8-sig') as fileobj:
            for line in fileobj:
                temp = line.split("-1")
                for _ in temp:
                    e = _.split()
                    e = [int(x) for x in e]
                    if (len(e) > 0):
                        trace.append(e)
                        for _ in e:
                            freq_trace.append(_)

        event_support = Counter(freq_trace)
        events = set(freq_trace)
        #----------------------zero and undefined cases----------------------
        if len(confidence) != 0:
            for key in confidence:
                if key[0] in events and key[1] not in events:
                    RuleCount[key] = RuleCount[key][0]+1
                    RuleCount[key[1],key[0]] = RuleCount[key[1],key[0]][1]+1

        # print("Events: ",event_support)
        for i in range(2, input_length + 1):
            pairs = pm(events, i)  # getting the permutation of length 2(i == 2)
            for pair in pairs:
                temp = []
                for each_set in trace:
                    temp1 = []
                    for event in each_set:
                        if event in pair:
                            temp1.append(event)
                    if (len(temp1) == len(pair) and len(temp) == 0):
                        temp.append(int(pair[0]))

                    elif (len(temp1) == len(pair)):
                        temp = temp + list(pair)
                    else:
                        temp = temp + list(temp1)

                if len(set(temp)) > 1:
                    find_support(pair, temp)
        print("event support: ", event_support)
        print("Rule Support: ", rule_support)

        for key in rule_support:
            # print(key,support[key],end =": ")
            # print(key[0:-1])
            # print(event_freq[key[0]])

            if len(key) == 2:
                if key in confidence:
                    confidence[key] = (rule_support[key] / event_support[key[0]])+confidence[key][0], (rule_support[key] / event_support[key[1]])+confidence[key][1]  # FConf, recall
                else:

                    confidence[key] = (rule_support[key] / event_support[key[0]]), (rule_support[key] / event_support[key[1]])  # FConf, recall
                if key in RuleCount:
                    RuleCount[key] = RuleCount[key][0]+1, RuleCount[key][1]+1
                else:
                    RuleCount[key] = 1,1
            else:
                try:
                    confidence[key] = rule_support[key] / rule_support[key[0:-1]], rule_support[key] / event_support[
                        key[-1]]  # findding Fconf for larger rules, is not complete now
                    # print(key, " : ", support[key[0:-1]])
                except ZeroDivisionError:
                    confidence[key] = 0
                    print("divide by zero found!!!")

        print("Rules", confidence)
        print("Rule count",RuleCount)
        freq_trace = []
        trace = []
        rule_support = {}
        print()
# print("trace: ",trace)
# print("frq_trace: ",freq_trace)
# print("distincet events: ",events)
# print("event support: ",event_support)
# print(map)

#******************************** find support for rule of two**********************************
#********************calculate support for event of length 2**********************************



# make projected list



# print("rule_support: ",rule_support)


# find avg confidence for rule of length two

# for key in confidence:
#     if RuleCount[key][0] and RuleCount[key][1] !=0:
#         confidence[key] = confidence[key][0] / RuleCount[key][0], confidence[key][1]/RuleCount[key][1]
#
# print("Final: ",confidence)