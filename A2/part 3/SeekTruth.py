# SeekTruth.py : Classify text objects into two categories
#
# Rohan Mehta [mehtaro], Pramey Modi [pmmodi],Akshay Tiwlekar [akstiwle]
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys


def load_file(filename):
    objects = []
    labels = []
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ', 1)
            labels.append(parsed[0] if len(parsed) > 0 else "")
            objects.append(parsed[1] if len(parsed) > 1 else "")
    return {"objects": objects, "labels": labels, "classes": list(set(labels))}


# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated class label for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
import time


def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!
    stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", ".", ",", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    count = dict()  # creating a blank dictionary to count the number of occurrences of each word in truthful and deceptive reviews
    # print(train_data["objects"][0],train_data["labels"][0],train_data["classes"][0])
    for i in range(len(train_data["objects"])):

        line = train_data["objects"][i]  # reading the reviews line by line
        parsed = line.strip().lower().split()  # splitting the reviews word by word to count the occurrences
        for word in parsed:
            if word not in count:
                count[word] = {}  # adding the not occurred word in the count dictionary

            if train_data["labels"][i] == "truthful":  # checking each word occurrence in truthful

                if 'truthful' not in count[word]:
                    count[word]['truthful'] = 0  # if not truthful then giving the count as 0
                count[word]["truthful"] += 1  # else incrementing the count by 1
            else:

                if 'deceptive' not in count[word]:
                    count[word]['deceptive'] = 0  # if not deceptive then giving the count as 0
                count[word]["deceptive"] += 1  # else incrementing the count by 1

    print (count)

    result = []  # creating a blank list to store the result of the train dataset
    for i in range(len(test_data['objects'])):
        line = test_data['objects'][i]

        ratio_T_D = 1  # initiating the ratio (truthful/deceptive as 1 to further multiply it with the probability
        for word in line.strip().lower().split():
            # handling the stopwords and special characters
            # if word in stopwords:
            #     continue
            if word not in count:
                continue  # handling the error of 0 probability by continuing if a word in test data is not found in train data count dictionary
            else:
                if 'truthful' not in count[word] or 'deceptive' not in count[word]:
                    continue  # handling the error of 0 probability by continuing if a word in test data is not found in train data truthful or deceptive count dictionary

                else:
                    ratio_T_D *= count[word]['truthful'] / count[word]['deceptive']  # counting the probability of the review in test data being deceptive or truthful
        if (ratio_T_D > 1):  # if probability is > 1, then truthful will be appended in result
            result.append('truthful')
        else:  # if probability is < 1, then deceptive will be appended in result
            result.append('deceptive')

    return result

    # return [test_data["classes"][0]] * len(test_data["objects"])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if (sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results = classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([(results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"]))])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
