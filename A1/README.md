# Report of Part 1,2 & 3

# Part 3
The goal of this assignment is to create an effective team assignment procedure keeping in mind various conditions to assign the team memebers in such a way that it takes
the grader minimum time to check and grade the assignment:
1. For this assignment we have used A* algorithm for finding the cost of the function, in this case 
   calculating the cost of different team member combinations and choosing the lowest grading time team assignment. 
2. For assigning the team, we have created a list of unpaired students and taking index-wise value from that list
   to enter it into a fringe (that keeps track of visited states (in this case visited team allocations)) and making combinations of team according to teams assigned.
3. We have created a random function that takes any student from unpaired list and adds it to the successor function, where is gets computed and the place for that particular kid is chosen to be assigned to a team. 
4. We have created a priority function which sets priority of the visited states according to their minimum cost function.
5. We have used a combination heapq and random function for choosing a state when we are in a situation where 2 states have the same priority. So, as to prevent the code from running or going in an infinite loop by not choosing any state. 
6. The successor function traverses through all possible states or combination of teams, that will be used for comparison when using the A* algorithm for finding an optimal solution.
7. We have also created a function to read the .txt file and changed it into a format where it is easy to pass, compute and manipulate the values as needed in the algorithm. And, we have also added a desired format output as asked in the assignment to read the output easily.
8. We have designed a function that computes the time taken to check and grade a team's assignment by taking various parameters such as wanted team size, unwanted team members, etc. to check the total time that will be taken to grade a particular team.
9. The algorithm checks which team combination is the best suitable for the graders such that it takes the least amount of time to grade the assignment.