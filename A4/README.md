# a4
#Part - 1 

- Here we have to apply K-nearest neighbor algorithm, with a slight change that when the parameter is set to 'distance', the weights for considering the nearest points should be proportional to 
inverse of the distance from the test sample to each neighbor, while usually directly proportional distance from the test sample to each neighbor is taken. 
- To find patterns that match any application, the simplest supervised method is K nearest neighbors. Assuming the training data has a 
Gaussian distribution while using this method of data analysis we look at the test data and figure out how near the test data is to a certain group in terms of the Gaussian distribution of the train data.
- We had to apply functions to compute manhattan and euclidean distance and also fit and predict method for test data. 
- We had to check the accuracy of our algorithm with respect to the accuracy of sklearn library. Methods to calculate the manhattan and euclidean distance were easy to apply as they are straightforward math computations, and I applied it with the help of numpy library.
Using predict method, it is possible to decide which category the data belongs to by comparing the test and train datasets. I facilitated as asked that if the weight = 'distance', I use the inverse of the distance.
- The accuracy of my algorithm is approximately similar to that of sklearn model library. 

#Part - 2

