# akstiwle-mehtaro-pmmodi-a3
a3 created for akstiwle-mehtaro-pmmodi
# Part - 1
# Simplified Model
- In the Simplified model, we just considered the dependence between the parts of speech and the words. 
- We maximize the posterior probability P(S|W) {probability of part-of-speech given the word}, i.e. Prior * Likelihood (P(S) * P(W|S)), for each word in the sentence.
- The final result for this method, we got 93.9% accuracy for words and 47.45% for sentences.

# Hidden Markov Model using Viterbi Algorithm
- Unlike other models, this model takes into account the dependency on consecutive words as well as the dependency on word to sentence.
- Our process includes keeping a track of the maximum probabilities till the probabilities of each of the words in a sentence is calculated, and 
we use the maximum probabilities of the previous word, which is precalculated. We created the transition matrix for the same to make the values more accessible for computation.
- The final result for this method, we got 94.63% accuracy for words and 53.3% for sentences.

# Complex Markov Chain Monte Carlo using Gibbs Sampling
- In this particular approach transition probabilities need to be evaluated in this case from the third word in a sentence to two precedent parts of speech.
- P(noun, det, verb) is for instance derived from the dict[noun][det][verb]. In the absence of probability information for a particular sequence, a minimum probability (in our case 1e-10) is assigned for computation feasibility.
- Considering S(n) is the Parts-of-Speech tag for the nth word in a sentence, and S(n-1), S(n-2) are the parts of speech tags for the following cells. A transition probability dictionary of dictionaries was built earlier for HMM. For this case, we need to add one more layer since another variable (parts of speech tag) must be stored. By just accessing corresponding keys in the dictionary, we will be able to obtain transition probability quickly.
- In order to generate part of speech tags for each word in the sentence, many samples must be generated. For testing, here a simulation of 100 samples are generated with 50 of them being left out for preparation. The accuracy of the prediction was not significantly affected when varying from 100 to 2000 samples. We use word predictions from HMM for this and we think this would be a better approach and chance of convergence to happen in less time is higher.
- An example would be to loop over each word and keep all the tags the same and then POS distribution is calculated. We calculate the probability of each of 12 speech tags being related to the current word. The distribution is used to select a tag for the current word, which is then modified for the following sample. This revised version will be used to generate the next sample.
- The final result for this method, we got 93.2% accuracy for words and 51.85% for sentences.

# Part - 2
- The program is used to find the layer of ice that is accumulated on the rock bed with the help of image processing and with other probability calculation such as bayes net, Viterbi and some of the human feedback.
- For bayes net we started with calculation of the emission probability. In the image we were provided with the code for edge strength.
- Basically, the edge strength function uses sobel filter function from the OpenCV library, purpose of which is to calculate the strength of the edges that changes color in an image (basically a grey scale image). Only issue with this function was that the value of the edge strength was always greater, because of which the less dark pixel is considered. 
- Hence in bayes net the yellow line is bit higher as compared to the darker line
- In Viterbi the emission probability is taken from the bayes net function. The transmission probability is taken with respect to the position of the pixel as hinted by the assignment.
- The probability of the pixel whose distance is greater will be less than the probability of the pixel which is close to the previous pixel.
- In most of the images the probability is giving almost smooth curse for Viterbi, only with the image 23.png, because we have not given any weight or made any estimation to the probability the curse is little bit distorted.
- In the human feedback, we have given the point where the darker layer should start. As such the code is the same as the code for Viterbi, just that we have added some more weightage to the transmission probability. 
- The curve might not get perfect as might not give the proper result for Viterbi or the human feedback, but the algorithm application is properly done by us. If time persist we will try to improve the Viterbi algorithm as well as the human feedback.

# Part - 3
In this question we have to identify the characters from the image and all the characters are in the form of stars ‘*’ and spaces ‘  ‘. We need to apply two algorithms.

1.	Simple Bayes Net:
For this algorithm first we store the kyes of the dictionary which are characters itself and the values into the separate list.
So, in the code charter list represent the characters and b contains the patterns for corresponding characters.
1.Training Data set: for training the data we got one sample image with accurate images of each character. We used that list of patterns to train the algorithm. To train the algorithm, we make the heuristic as bellow.
	Heuristic:  the pattern is 14*25. So, for each 25 row the locations of star will be stored into separate list (temporary list). And that list will be appended into another list. So, basically the list of lists will have the star locations of 25 rows of each character (training character). 
	Afterwards each testing letter’s star locations (for every row) will compare with each character star location with the training data and for each match their will be an increment of one count and the final count will be added to the list. So, we will have the list of lists for count of matches for character of each character of data set. Which will become the probability of pater given it is a particular character(P(Oi | Li)). So, we will have the probability of pattern being each pattern and the max values will be assigned to keys in the dictionary.
So, this way with bayes net we got the probability o f P (l1, ..., ln|O1, ..., On)

 
The key with probability closest to 1 will be printed as final character. And this whole process will run for each pattern in the test case.

This algorithm has a good accuracy. Since, it will detect almost every character each time.
2.	HMM:
For applying HMM: basically, we need Initial Probability, Emission Probability, Transition Probability.
Initial Probability: For this first we aggregated each sentence of a text data set into the tuple and (name of tuple = V) after that by using v[i][0][0][0] and running it through the loop achieved the beginning letters of each sentence and stored it into the list and got the occurrence of each letter from that and divide it with total number of initial letters. That way I got the initial probability of each letter.

Emission Probability: for this we used the probability of pattern being a particular letter as an emission probability

Transition Probability: for this I used the same data set I used for initial probability but store all the character of the whole text file in the form of list (including the letter, numbers, and special letters). After that for each 72 characters that stored previous in bayes net into the list name character I found the next character will be stored in the list and then occurrence and divided by the occurrence of main character (A,B,C…) of each character counted and stored into the nested dictionary. So, we have the nested dictionary. So, now the dictionary will have the probability of every character after char probability. {A: {A: B: , C: …},B:{A: ,B:, C:…},….}.

After find all the probability I made a dictionary of each element of character list multiplying the emission probability and initial probability to generate score for every first element of each test case. {A: ,B:, C:,…}. 

After that appending the multiplication of {A: ,B:, C:,…} * {A: {A: B: , C: …},B:{A: ,B:, C:…},….} to find the final score for each character transition after the initial and printing the max of it to get the final output.