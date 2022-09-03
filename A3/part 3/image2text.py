#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (insert names here)
# (based on skeleton code by D. Crandall, Oct 2020)
#
from PIL import Image, ImageDraw, ImageFont
import sys

CHARACTER_WIDTH = 14
CHARACTER_HEIGHT = 25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [["".join(['*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg + CHARACTER_WIDTH)]) for y in
                    range(0, CHARACTER_HEIGHT)], ]
    return result


def load_training_letters(fname):
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return {TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS))}


#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

## Below is just some sample code to show you how the functions above work. 
# You can delete this and put your own code here!


# Each upgrade training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:
# print(test_letters[5])
# print("...".join([ r for r in train_letters['S']]))
# print(train_letters)
# print(c train_letters['S']]))

# Same with test letters. Here's what the third letter of the test data
#  looks like:
#print("\n".join([ r for r in test_letters[30]]))
def intersection(lst1,lst2):  # used this line form geeks of geeks link : https://www.geeksforgeeks.org/python-intersection-two-lists
    lst3 = [value for value in lst1 if value in lst2]
    # ends here

    return len(lst3)
"""******This part will work for train data set******"""
"""this will convert the dictionary into the two list a and b """
charecter = []  # contains corosponding charcter
b = []  # contais pattern of each character
for i, j in train_letters.items():
    charecter.append(i)
    b.append(j)
"""Trying to ger the number of star location from the string"""

liststar = []
def genstar(k):
    all_str = list()
    for i in range(len(b[k])):
        startrain = []
        [startrain.append(j) for j in range(len(b[k][i])) if b[k][i][j]=="*"]
        all_str.append(startrain)
    #print(all_str)
    return all_str
#print(genstar(0))
for j in range(0,72):
    temp = genstar(j)
    liststar.append(temp)
#print(liststar)

"""ends here"""
"""******ends here for train data*******"""

"""******This part will work for test data set******"""
"""this will convert the dictionary into the two list a and b """
a = []  # contains corosponding charcter
b1 = []  # contais pattern of each character
for i in test_letters:
    #a.append(i)
    b1.append(i)
"""ends here"""
"""This will compute the locations of star for space pattern"""
def teststring(q):
    all_ste = []
    for i in range(len(b1[q])):
        startest =[]
        [startest.append(j) for j in range(len(b1[q][i])) if b1[q][i][j]=="*"]
        all_ste.append(startest)
    return all_ste
testlist = []
for q in range(len(b1)):
    temp1 = teststring(q)
    testlist.append(temp1)
"""ends here"""
"""******ends here for train data*******"""

"""computing the score by comparinf the location of stars"""
#print(testlist[0])

def starscore(g,x):
    testlist2 = []
    starscore = []
    for i in range(0,25):
        starscore.append(intersection(liststar[g][i], testlist[x][i]))
    return sum(starscore)

# list1 = []
# for i in range(0,72):
#     starscoretemp = starscore(i)
#     list1.append(starscoretemp)
# print(max(list1))
def testdetect():
    answer = []
    temp = []
    x = 0
    temp.clear()
    emission = { x:0 for x in train_letters} #This to save the emission score for each character
    while x < len(b1):
        for i in range(0, 72):
            starscoretemp = starscore(i,x)
            temp.append(starscoretemp)
        zip_iterator = zip(charecter, temp)
        dic = dict(zip_iterator)
        emission[x] = dic # this will get the emission score for each chareacter
        if max(temp) < 3:
            answer.append(" ")
        else:
            answer.append(max(dic, key=dic.get))

        temp.clear()
        x += 1
    return answer,emission
final,emission =testdetect()

print("Simple: " + "".join([ r for r in final]))
"""comparision ends here"""

"""count the number of space and star for each charecter"""

"""HMM starts Here"""
# Reding data form file bc train
def read_data():
    letter = []
    with open('abtrain', 'r') as file:
        data = file.read().rstrip()
    for line in data:
        for i in range(len(line)):
            letter.append(line[i])
    return letter
letter_list = read_data()

def read_data1():
    exemplars = []
    file = open('bc.train 2', 'r')
    for line in file:
        data = tuple([w.lower() for w in line.split()])
        exemplars += [ (data[0::2], data[1::2]), ]
    return exemplars
v=read_data1()
initial =  { x:0 for x in train_letters}
for i in range(len(v)):
    if ((v[i][0][0][0] == "`") or (v[i][0][0][0] == "&") or (v[i][0][0][0] == ";") or (v[i][0][0][0] == "&" ) or (v[i][0][0][0] == "$" ) or (v[i][0][0][0] == "*" )):
        pass
    else:
        initial[v[i][0][0][0]]+=1
#print(initial)
"""this will count the next charcter of each element of text(charecter lsit)"""
def tempfun(x):
    character_next = []
    for i in range(len(letter_list)-1):
        if letter_list[i] == x:
            character_next.append(letter_list[i+1])
    return character_next
"""this will count the occurence of eacj cjharcter in the text document"""
def countof(x):
    count = 0
    for i in range(len(letter_list)-1):
        if letter_list[i] == x:
            count += 1
    return count
charnext = [] # this will sotore the next char set for each charecter
charcount = [] # this will store the ocurrence of each chatecter
for i in range(len(charecter)):
    charnext.append(tempfun(charecter[i]))
    charcount.append(countof(charecter[i]))
#let,cnt, letprob = (charprob(letter_list))

#print("lenght of letprob",len(letprob[0]))
def probability(a):
    probab = []
    count = 0
    probab.clear()
    for x in range(len(charnext[a])):
        for ele in charnext[a]:
            if (ele == charnext[a][x]):
                count = count + 1
        prob = count/charcount[a]
        count = 0
        probab.append(prob)
    return probab
"this will contains the transmission probability of all charecter"
probability_list = []
for a in range(len(charecter)):
    probability_list.append(probability(a))
#print(max(probability_list[0]))
#print(max(charnext[0]))
#for (item1, item2) in zip(charnext[0], probability_list[0]):
def trasition_probab(z):
    zip_iterator = zip(charnext[z], probability_list[z])
    transition = dict(zip_iterator)
    aDictionary =  { x:0 for x in train_letters}
#print(aDictionary)
    for i in transition:
        for j in aDictionary:
            if i == j:
                transition[i],aDictionary[j] = aDictionary[j],transition[i]
    return aDictionary

finaltransition = { x:0 for x in train_letters}
for i in range(len(finaltransition)):
     temptran = trasition_probab(i)
     finaltransition[charecter[i]] = temptran
"""this will show the trasition probability for each charcter to each charecter"""
#print(finaltransition['E'])
#print(emission[0])

def maxhmm(q,l):
    product = []
    count = 0
    finalhmm = []
    for i,j in finaltransition.items():
        for k,z in j.items():
            if k == q:
                prod = l * j[k]
                product.append(prod)
    return max(product)
        #             prod = z * emission[1][o]
        #             product.append(prod)
        # finalhmm.append(product)
        # print(len(finalhmm))
        #for k in j['A']:
answerhmm = []
Transition_dictionary = { x:0 for x in train_letters}
for w in range(len(b1)):
    for i in emission[w]:
        #print(emission[w][i])
        Transition_dictionary[i]= maxhmm(i,emission[w][i])
    #print(Transition_dictionary)
    answerhmm.append(max(Transition_dictionary, key=Transition_dictionary.get))
#print(answerhmm)
print("Hmm: " + "".join([ r for r in answerhmm]))
#print(max(emission[2],key = emission[2].get))
# def initial():
#     temp = []
#     for key in emission[0]:
#         if key in initial:
#             emission[0].update((int(emission[0][key]) * int(initial[key])))

#print(temp)
#transition = dict(zip(charnext,probability_list))
#print(transition)
# print("   HMM: " + "Sample simple result")
