from collections import *
from itertools import permutations as pm
import time, os
import re,csv

#**************************************variable declaration area*********************************
map = {} #holds events and their corresponding msgs
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
#[[0, 1], [38, 39, 42, 6], [1, 0], [2, 3], [10], [10], [10, 7, 8], [10], [2, 3]]
#**************************Making data ready for mining(prepocessing)***************************
# Mapping for event number to msgs
with open("Mapping info.txt", "r", encoding='utf-8-sig') as fileobj:
  for line in fileobj:
      temp = line.split(":")
      events.append(int(temp[0]))
      map[int(temp[0])] = temp[1:]


with open("2.tstt.mem.txt", "r", encoding='utf-8-sig') as fileobj:
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
#print(trace)
#print(freq_trace)
#print(events)
#print(event_support)
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


# print(rule_support)


# find confidence for rule of length two
for key in rule_support:
    # print(key,support[key],end =": ")
    # print(key[0:-1])
    # print(event_freq[key[0]])
    if len(key) == 2:
        confidence[key] = rule_support[key] / event_support[key[0]], rule_support[key] / event_support[key[1]]  # FConf, BConf
    else:
        try:
            confidence[key] = rule_support[key] / rule_support[key[0:-1]], rule_support[key] / event_support[
            key[-1]]  # findding Fconf for larger rules, is not complete now
            #print(key, " : ", support[key[0:-1]])
        except ZeroDivisionError:
            confidence[key] = 0

# print(confidence)
#*****************start for rule of lenght three*******************

# rule1 = {}
# flag  = []
# for i in range(1,2):
#     temp0 = [i]
#     for key in confidence:
#         if(key[0] == i and confidence[key][0] == 1.0 and confidence[key][1] == 1.0): #key =[i,x]
#             #print(key,map[key[1]][0])
#             #rule1[key[0]]=key[1]
#             # zeroth = str(map[i][0]).replace(" ", "")
#             # eroth = str(map[key[1]][0]).replace(" ", "")
#             # op1 = map[i][2].replace("\n", "")
#             # op1 = op1.replace(" ", "")
#             # op2 = map[key[1]][2].replace("\n", "")
#             # op2 = op2.replace(" ", "")
#             #print(eroth)
#             temp0.append(key[1])
#             # if(map[i][1] == eroth and zeroth == map[key[1]][1] and str(op1) == str(op2)):
#             #     flag.append([i,key[1]])
#             #     break
#         else:
#             pass
#
#     print(temp0)
# print(flag)
# for e in temp0:
#     eroth = str(map[e][0]).replace(" ", "")
#     # print(e,map[e])
#     if(map[0][1] == eroth):
#         print(e)
#     # if 0.dest == e.src:
#     #     rule[0] = e


# pair0 = pm(temp0, 2)
# rule1pair =[]
# for pair in pair0:
#     if(pair[0]<pair[1]):
#         try:
#             if(confidence[pair][0] == 1):
#                 rule1pair.append(pair)
#         except KeyError:
#             pass

#print("rule 1",rule1pair)
# reduced1 =[]
# for pp in rule1pair:
#     eroth = str(map[pp[1]][0]).replace(" ", "")
#     if(map[pp[0]][1] == eroth):
#         print(pp)
#         reduced1.append(pp)

#print(reduced1)
# filter_reduced1 = []
# l = [0,8,11,13,17,18,25]
# for ppp in reduced1:
#    if(ppp[0] in l):
#        print(ppp)
#        filter_reduced1.append(ppp)
#
# print("reduced: ",ppp)

rule_2_high_Cf = []

for rule in confidence:
    dest = map[rule[0]][1].replace(" ", "")
    src = map[rule[1]][0].replace(" ", "")
    if(confidence[rule][0] == 1.00 or confidence[rule][1] == 1):# and dest == src:
        rule_2_high_Cf.append(rule)

f= open("rules_all1.txt","w+")

def Fw_recur(root, depth): # B
    stack.append(root)
    global last_rule_lenth1, base
    for rule in rule_2_high_Cf: # for each rule in B->X
            dest = map[root][1].replace(" ","")
            src = map[rule[1]][0].replace(" ","")
            if (stack[-1] == rule[0]) and depth <10 and (confidence[rule][0] == 1 or confidence[rule][1] == 1) and (rule[1] not in stack) and (src == dest): # or confidence[rule][1] == 1 or
                depth += 1
                Fw_recur(rule[1],depth)
    if len(stack)>= last_rule_lenth1:
        last_rule_lenth1 = len(stack)
        rule = base + stack
        f.write(str(rule)+"\n")
        # with open('rules_all.txt', 'a') as f:
        #     print(stack, file=f)
        #print(stack)
        stack.pop()
    else:
        last_rule_lenth1 = len(stack)
        stack.pop()

stack = []
def Bc_recur(root, depth): # A
    stack.append(root)
    global last_rule_lenth2, base
    for rule in rule_2_high_Cf: # for each rule in B->X
            src = map[root][0].replace(" ", "")
            dest = map[rule[1]][1].replace(" ", "")
            if (stack[-1] == rule[1]) and (confidence[rule][1] == 1 or confidence[rule][0] == 1) and depth <5 and (rule[0] not in stack): #confidence[rule][0] == 1 or
                depth += 1
                Bc_recur(rule[0], depth)

    if len(stack)>= last_rule_lenth2:
        last_rule_lenth2 = len(stack)
        rule = base + stack
        f.write(str(stack)+"\n")
        stack.pop()
    else:
        last_rule_lenth2 = len(stack)
        stack.pop()

print(rule_2_high_Cf)
for rule1 in rule_2_high_Cf:
    # dest = map[rule1[0]][1].replace(" ", "")
    # src = map[rule[1]][0].replace(" ", "")
    #if(rule1[0] in ): #and src == dest:
        depth = 0
        base = [rule1[0]] #base is the current seed being grown, is it being added to enhance readability
        # f.write(str(rule1[0])+ " :")
        # print("Prefix: ",rule1[0], end=" ")
        f.write("grow forward:  " + "\n")
        Fw_recur(rule1[1],depth)
        stack = []
        f.write("grow back: " + "\n")
        # f.write(str(rule1[1])+ " :")
        Bc_recur(rule1[0], depth)
f.close()
    # else:
    #     break

    # for rule2 in rule_2_high_Cf: # forward rules
    #     if(rule1[1] == rule2[0]):
    #         if (confidence[rule2][0] == 1 or confidence[rule2][1] == 1):
    #             print(rule1, rule2)
        #     #print(rule1, rule2, map[rule2[0]][1],map[rule2[1]][0])
        #     dest = map[rule2[0]][1].replace(" ","")
        #     src = map[rule2[1]][0].replace(" ","")
        #     if src == dest:
        #         # print(rule1, rule2, src , dest)
        #         # rule3.append(list(rule1).append(rule2[1]))
        #         # temp = temp.append(int(rule2[1]))
        #         print(rule1[0],rule1[1],rule2[1])




