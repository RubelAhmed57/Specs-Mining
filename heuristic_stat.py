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
input_length = 2
stack = []

last_rule_lenth1 = 0 # to prevent adding suffix rules
last_rule_lenth2 = 0 # to prevent adding suffix rules
base = []
counter = 0
#[[0, 1], [38, 39, 42, 6], [1, 0], [2, 3], [10], [10], [10, 7, 8], [10], [2, 3]]
#**************************Making data ready for mining(prepocessing)***************************
# Mapping for event number to msgs
with open("Mapping info.txt", "r", encoding='utf-8-sig') as fileobj:
  for line in fileobj:
      temp = line.split(":")
      events.append(int(temp[0]))
      map[int(temp[0])] = temp[1:]


with open("./inputs/sample_input.txt", "r", encoding='utf-8-sig') as fileobj:
  for line in fileobj:
      temp = line.split("-1")
      for _ in temp:
          e = _.split()
          e = [int(x) for x in e]
          if(len(e)>0):
              trace.append(e)
              for _ in e:
                  freq_trace.append(_)

event_support = Counter(freq_trace)
# print("trace: ",trace)
# print("frq_trace: ",freq_trace)
# print("distincet events: ",events)
# print("event support: ",event_support)
# print(map)
#******************************** find support for rule of two**********************************
#********************calculate support for event of length 2**********************************
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


#make projected list
for i in range(2, input_length+1):
    pairs = pm(events,i) # getting the permutation of length 2(i == 2)
    for pair in pairs:
        temp = []
        for each_set in trace:
            temp1 = []
            for event in each_set:
                if event in pair:
                    temp1.append(event)
            if(len(temp1)==len(pair) and len(temp) == 0):
                temp.append(int(pair[0]))

            elif(len(temp1)==len(pair)):
                temp = temp + list(pair)
            else:
                temp = temp + list(temp1)

        if len(set(temp))>1:
            find_support(pair, temp)


# print("rule_support: ",rule_support)


# find confidence for rule of length two
for key in rule_support:
    # print(key,support[key],end =": ")
    # print(key[0:-1])
    # print(event_freq[key[0]])
    if len(key) == 2:
        confidence[key] = rule_support[key] / event_support[key[0]], rule_support[key] / event_support[key[1]]  # FConf, recall
    else:
        try:
            confidence[key] = rule_support[key] / rule_support[key[0:-1]], rule_support[key] / event_support[
            key[-1]]  # findding Fconf for larger rules, is not complete now
            #print(key, " : ", support[key[0:-1]])
        except ZeroDivisionError:
            confidence[key] = 0
            print("divide by zero found!!!")
print("Rule Confidence and recall: ",confidence)
#*****************start for rule of lenght three*******************

rules = []

# for rule in confidence:
#     dest = map[rule[0]][1].replace(" ", "")
#     src = map[rule[1]][0].replace(" ", "")
#     if(confidence[rule][0] >= 0.00 and confidence[rule][1] >=0) and dest == src:
#         rules.append(rule)

f= open("rules_for_original_1.txt","w")

# print(rules)
# nodes = []
visit = []
def Traverse(root, depth, visit):
    global counter
    if (depth == global_depth):
        # last_node = 0
        # print("extra")
        # print(visit)
        f.write(str(visit) + "\n")
            # last_node = x
        # visit.remove(last_node)
        return
    # print(root)
    noNewNode = 1
    for rule in rules:
        node = rule[1]
        # print("visiting : " + str(rule[0]))
        if ( node not in visit and rule[0] == root):
            visit.append(node)
            noNewNode = 0
            Traverse(node, depth+1, visit)
            visit.remove(node)

    if (noNewNode == 1):
        # print(visit)
        # print("End\n")
        f.write(str(visit) + "\n")

## This is the MAX DEPTH
global_depth = 8

# for rule in rules:
#     if(rule[0] in [0, 1, 2, 3, 4, 5, 6]):  # and src == dest:
#         visit.append(rule[0])
#         visit.append(rule[1])
#         base = [rule[0]]  # base is the current seed being grown, is it being added to enhance readability
#         Traverse(rule[1], 2, visit)
#         visit.remove(rule[1])
#         visit.remove(rule[0])
# f.close()

