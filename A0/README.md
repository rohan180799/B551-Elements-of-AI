# a0
For the first code, i.e. route_pichu,  we had to implement a search algorithm and find the most optimal solution for the pichu to reach it's goal destination.
I used Depth First Search approach for this which uses stack for exploring all the childs of a particular node. 
The fringe pops the node values it needs to explore the child of and enter the values of explored children. 
After that it pops the unnecessary nodes (the nodes which do not take us to the goal state) and starts exploring childs of another node. 
So, what it basically does is after coming to a dead end of a node it will backtrack to the parent node and start exploring a different path of another node.
The alr_visited list stores the values of all the child nodes visited to avoid repeating the search on trivial nodes. 


For the second assignment, I have used Breadth First Search(BFS) approach. 
Firstly, by using random function of numpy, the system itself chooses a row and column co-ordinate to place the pichu. 
After selecting the random co-ordinates it checks that are there any X or @ or p in that position, if not it will select that co-ordinate and place the pichu there. 
After that, we check the row, column and all four diagonals of the pichu location. 
By using 0,1 flag values (0 if there is no p or @ at any locations and 1 if there is any p or @), it also checks that are there any walls 'X' in the row column or diagonal, if yes then it places the pichu there and if not then the function returns clashing positions of p or @. 
After that, we create the new house map and check for zero indexes and that all the pichus are placed in correct positions or not.
The solve function checks everything and returns false if any condition is not satisfied. 