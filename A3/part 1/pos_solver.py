###################################
# CS B551 Spring 2021, Assignment #3
#
# Rohan Mehta (mehtaro), Akshay Tiwlekar (akstiwle), Pramey Modi (pmmodi)
#
# (Based on skeleton code by D. Crandall)
#


import random
import math
import numpy as np


# Taken reference for understanding the concept and application of Hidden Markov Model
# from this link: https://www.youtube.com/watch?v=fv6Z3ZrAWuU and Classroom Lectures

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    # We first tried to initiate all the variable globally but then took the idea from Q&A to initiate all the variables
    # in the class itself: https://iu.instructure.com/courses/2027431/external_tools/271583
    def __init__(self):
        self.word_count = 0
        self.unique_words = {}
        self.unique_pos = {}
        self.pos_count = {}
        self.pos_prob = {}
        self.emission_count = {}
        self.emission_prob = {}
        self.transition_count = {}
        self.transition_prob = {}
        self.transition2_count = {}  # for complex mcmc we need to find the transition of transition,
        # i.e. {pos: {'pos': {pos: count , pos1:..}}}
        self.transition2_prob = {}  # for complex mcmc we need to find the transition of transition,
        # i.e. {pos: {'pos': {pos: probability , pos1:..}}}
        self.posterior_simple = 0
        self.posterior_HMM = 0
        self.default_prob = float(1) / float(10 ** 10)  # giving a default probability = 1e-10
        # for avoiding the 0 probability; divide/0 of log(0)

    # Calculate the log of the posterior probability of a given sentence
    # with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        print(sentence, label)
        if model == "Simple":
            posterior = 0
            for i in range(len(sentence)):
                if sentence[i] in self.emission_prob and label[i] in self.emission_prob[sentence[i]]:
                    posterior += math.log(self.emission_prob[sentence[i]][label[i]])
                posterior += math.log(self.pos_prob[label[i]])
            return posterior
        elif model == "HMM":
            posterior = 0
            for i in range(len(sentence)):
                if sentence[i] in self.emission_prob and label[i] in self.emission_prob[sentence[i]]:
                    posterior += math.log(self.emission_prob[sentence[i]][label[i]])
                if i == 0:
                    posterior += math.log(self.transition_prob[label[i]][" "])
                else:
                    posterior += math.log(self.transition_prob[label[i]][label[i - 1]])
            return posterior
        elif model == "Complex":
            # print(self.probability(sentence, label))
            posterior_complex = self.probability(sentence, label)
            return posterior_complex
        else:
            print("Unknown algo!")

    # Do the training!
    # Here we count the total number of unique words, occurrence of each part-of-speech
    # for all the unique words in a dictionary format {'word': {'pos': count, 'pos1': count...}, 'word1': {...},...}.
    # We count the transition count and transition probability of each each part-of-speech to know
    # the highest chance of the next part-of-speech.
    # The emission count and all the emission probability of a word being a particular part of speech.
    # We count the overall probability of each part-of-speech from the whole data, i.e which part-of-speech occurred the
    # highest, i.e. to get the values of P(S) for Bayes Net, simplified ().

    def train(self, data):
        self.datasize = len(data)
        for w, s in data:
            self.word_count += len(w)
            for i in range(len(w)):
                if w[i] not in self.unique_words:
                    self.unique_words[w[i]] = True
                if s[i] not in self.unique_pos:
                    self.unique_pos[s[i]] = True
                if w[i] in self.emission_count:
                    if s[i] in self.emission_count[w[i]]:
                        self.emission_count[w[i]][s[i]] += 1
                    else:
                        self.emission_count[w[i]][s[i]] = 1
                else:
                    self.emission_count[w[i]] = {}
                    self.emission_count[w[i]][s[i]] = 1
                if s[i] in self.pos_count:
                    self.pos_count[s[i]] += 1
                else:
                    self.pos_count[s[i]] = 1
                if i == 0:
                    if s[i] in self.transition_count:
                        if " " in self.transition_count[s[i]]:
                            self.transition_count[s[i]][" "] += 1
                        else:
                            self.transition_count[s[i]][" "] = 1
                    else:
                        self.transition_count[s[i]] = {}
                        self.transition_count[s[i]][" "] = 1

                else:
                    if s[i] in self.transition_count:
                        if s[i - 1] in self.transition_count[s[i]]:
                            self.transition_count[s[i]][s[i - 1]] += 1
                        else:
                            self.transition_count[s[i]][s[i - 1]] = 1
                    else:
                        self.transition_count[s[i]] = {}
                        self.transition_count[s[i]][s[i - 1]] = 1
                if i >= 2:
                    if s[i] in self.transition2_count:
                        if s[i - 1] in self.transition2_count[s[i]]:
                            if s[i - 2] in self.transition2_count[s[i]][s[i - 1]]:
                                self.transition2_count[s[i]][s[i - 1]][s[i - 2]] += 1
                            else:
                                self.transition2_count[s[i]][s[i - 1]][s[i - 2]] = 1
                        else:
                            self.transition2_count[s[i]][s[i - 1]] = {}
                            self.transition2_count[s[i]][s[i - 1]][s[i - 2]] = 1
                    else:
                        self.transition2_count[s[i]] = {}
                        self.transition2_count[s[i]][s[i - 1]] = {}
                        self.transition2_count[s[i]][s[i - 1]][s[i - 2]] = 1

            # Counting the probabilities for each Part-of-speech
            # Now we count the TRANSITION PROBABILITY of all the POS
            # for hmm_viterbi we need the transition probability , i.e. the occurrence of pos1 for the preceding pos
            # for example {'noun': {'noun': 4, 'det': 5, adp: '0'...}
            for pos in self.unique_pos.keys():
                if pos not in self.transition_prob:
                    self.transition_prob[pos] = {}
                for precede in self.unique_pos.keys():
                    if precede in self.transition_count[pos]:
                        self.transition_prob[pos][precede] = float(self.transition_count[pos][precede]) / float(
                            self.word_count - self.datasize)
                    else:
                        self.transition_prob[pos][precede] = self.default_prob

        # finding the emission probabilities of word and its part-of-speech for hmm
        for word in self.unique_words.keys():
            for pos in self.unique_pos.keys():
                if word not in self.emission_prob:
                    self.emission_prob[word] = {}
                if pos in self.emission_count[word]:
                    self.emission_prob[word][pos] = float(self.emission_count[word][pos]) / float(self.pos_count[pos])
                else:
                    self.emission_prob[word][pos] = self.default_prob

        # transition probabilities for mcmc case where in each pos depends on the pos of two precedent words.
        # So, to count that we need to values from transition2_prob
        for pos in self.unique_pos.keys():
            if pos not in self.transition2_prob:
                self.transition2_prob[pos] = {}
            for precede1 in self.unique_pos.keys():
                if precede1 in self.transition2_count[pos]:
                    if precede1 not in self.transition2_prob[pos]:
                        self.transition2_prob[pos][precede1] = {}
                    for precede2 in self.unique_pos.keys():
                        if precede2 in self.transition2_count[pos][precede1]:
                            self.transition2_prob[pos][precede1][precede2] = float(
                                self.transition2_count[pos][precede1][precede2]) / float(
                                self.word_count - (2 * self.datasize))
                        else:
                            self.transition2_prob[pos][precede1][precede2] = self.default_prob
                else:
                    if precede1 not in self.transition2_prob[pos]:
                        self.transition2_prob[pos][precede1] = {}
                    for precede2 in self.unique_pos.keys():
                        self.transition2_prob[pos][precede1][precede2] = self.default_prob

        for pos in self.unique_pos.keys():
            if " " in self.transition_count[pos]:
                self.transition_prob[pos][" "] = float(self.transition_count[pos][" "]) / float(self.datasize)
            else:
                self.transition_prob[pos][" "] = self.default_prob

        # counting the POS probabilities, i.e. pos/total count of all pos
        for pos in self.unique_pos.keys():
            self.pos_prob[pos] = float(self.pos_count[pos]) / float(self.word_count)

    # print (self.unique_pos) # all different pos
    # print (self.pos_prob) # probability of each pos : pos/ total words
    # print (self.emission_count) # occurrence of each word in different pos
    # print (self.emission_prob) # probability that the word is a particular pos
    # print (self.transition_count) # count of the next pos, i.e. pos: {other pos after the initial pos}
    # print (self.transition_prob) # probability of the next pos, i.e. pos: {other pos after the initial pos}
    # print (self.transition2_count)
    # print (self.unique_words)
    # print (self.word_count)
    # print (self.datasize)

    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        simple = []
        for word in sentence:
            max_prob = -1
            end_pos = "."
            for pos in self.unique_pos.keys():
                if word not in self.emission_prob:
                    x = self.default_prob  # giving default probability = 1e-10 for words that don't exist in
                    # emission probability dictionary to avoid the Zero Probability problem
                else:
                    x = self.emission_prob[word][pos]
                if self.pos_prob[pos] * x > max_prob:
                    max_prob = self.pos_prob[pos] * x
                    end_pos = pos
            simple.append(end_pos)
        return simple

# taken reference of the concept from https://www.youtube.com/watch?v=12eZWG0Z5gY and Class Lectures
    def complex_mcmc(self, sentence):
        pos_predicted = self.hmm_viterbi(sentence)
        init_predicted = pos_predicted
        k = 0
        samples = []
        for k in range(100):
            sample_predicted = self.gibbs_sampling(sentence, init_predicted)
            if k > 50:
                samples.append(sample_predicted)
            k += 1
        sample_cols = list(zip(*samples))
        pos_predicted = [max(set(a), key=a.count) for a in sample_cols]
        return pos_predicted

    # The idea of applying Gibbs Sampling taken from: https://inscribe.education/main/indianau/6754110229500968/questions/6749461749650582
    # Reference for applying Gibbs Sampling: https://www.youtube.com/watch?v=7LB1VHp4tLE
    def gibbs_sampling(self, sentence, init_predicted):
        pos_sample = list(init_predicted)
        for i in range(len(sentence)):
            pos = []
            pos_prob = []
            for curr_pos in self.unique_pos.keys():
                pos.append(curr_pos)
                pos_sample[i] = curr_pos
                curr_pos_prob = self.probability(sentence, pos_sample)
                pos_prob.append(math.exp(curr_pos_prob))
            gs_sum = sum(pos_prob)
            if gs_sum == 0:
                pos_sample[i] = pos[0]
            else:
                temp_prob = [x / gs_sum for x in pos_prob]
                pos_sample[i] = np.random.choice(pos, p=temp_prob)
        return pos_sample

    def probability(self, sentence, pos_predicted):
        prob = 0
        for p in range(len(sentence)):
            word = sentence[p]
            pos = pos_predicted[p]
            if word not in self.emission_prob:
                x = self.default_prob
            else:
                x = self.emission_prob[word][pos]
            prob += math.log(x)
            if p == 0:
                prob += math.log(self.pos_prob[pos])
            elif p == 1:
                pos_prev1 = pos_predicted[p - 1]
                prob += math.log(self.transition_prob[pos][pos_prev1])
            else:
                pos_prev1 = pos_predicted[p - 1]
                pos_prev2 = pos_predicted[p - 2]
                prob += math.log(self.transition2_prob[pos][pos_prev1][pos_prev2])
            # print(prob)
        return prob

    def hmm_viterbi(self, sentence):
        pos_predicted = ["noun" for i in range(len(sentence))]
        # pos_predicted = 0.9
        # creating the transition matrix for applying viterbi
        transition_matrix = [[(0, ".", ".") for i in range(12)] for j in range(len(sentence))]
        pos_index = {}

        j = 0
        for pos in self.unique_pos.keys():
            pos_index[pos] = j
            j += 1

        j = 0
        for pos in self.unique_pos.keys():
            if sentence[0] in self.emission_prob:
                x = self.emission_prob[sentence[0]][pos]
            else:
                x = self.default_prob
            transition_matrix[0][j] = (self.transition_prob[pos][" "] * x, pos, pos)
            j += 1

        for i in range(1, len(sentence)):
            k = 0
            for pos in self.unique_pos.keys():
                j = 0
                max_prob = -1
                precede = "."
                for pos1 in self.unique_pos.keys():
                    if transition_matrix[i - 1][j][0] * self.transition_prob[pos][transition_matrix[i - 1][j][1]] > max_prob:
                        max_prob = transition_matrix[i - 1][j][0] * self.transition_prob[pos][transition_matrix[i - 1][j][1]]
                        precede = transition_matrix[i - 1][j][1]
                    j += 1
                if sentence[i] in self.emission_prob:
                    x = self.emission_prob[sentence[i]][pos]
                else:
                    x = self.default_prob
                transition_matrix[i][k] = (max_prob * x, pos, precede)
                k += 1

        # Taken the reference for backtracking for HMM from Q & A: https://iu.instructure.com/courses/2027431/external_tools/271583
        # Backtracking code is mentioned below
        j = 0
        max_prob = -1
        end_pos = "."
        for pos in self.unique_pos.keys():
            if transition_matrix[len(sentence) - 1][j][0] > max_prob:
                max_prob = transition_matrix[len(sentence) - 1][j][0]
                end_pos = transition_matrix[len(sentence) - 1][j][1]
                # pos_predicted[len(sentence) - 1] = end_pos
            j += 1
        if max_prob != 0:
            self.posterior_HMM = math.log(max_prob)
        len_sent = len(sentence) - 1
        for i in range(len(sentence)):
            pos_predicted[len_sent] = end_pos
            end_pos = transition_matrix[len_sent][pos_index[end_pos]][2]
            len_sent = len_sent - 1
        return pos_predicted

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labellings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")
