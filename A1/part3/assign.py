#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: [Rohan Mehta (mehtaro), Akshay Tiwlekar (akstiwle), Pramey Modi (pmmodi)]
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
# Discussed successor function with Dinesh Reddy Challa(dichalla)

import heapq
import sys
import random

# created a class to create and compute states of team assignments
class State:
    # creating a constructor of the State Class to call it while applying A* algorithm
    def __init__(self, teams, not_paired_stud):
        self.teams = teams
        self.not_paired_stud = not_paired_stud

    # overriding in-built equals function for comparing between 2 states
    def __eq__(self, other):
        if (len(self.teams) != len(other.teams)):  # optimization, Check length first. Then compare elements of array
            return False

        return sorted([sorted(x) for x in self.teams]) == sorted([sorted(x) for x in other.teams])

    # to set the priority of state while computing f(n) = (g(n)+h(n))
    def set_priority(self, priority):
        self.priority = priority

    # when using heapq for checking if state1<state2 or not,
    # the in-built functions __lt__ (less than) and __le__ (less than equal to) picks any of the 2 states randomly having the same priority.
    def __lt__(self, other):
        # return False
        return bool(random.getrandbits(1))

    def __le__(self, other):
        return False
        # return bool(random.getrandbits(1))

    #  this __repr__ in-built function is used to return a string of the desired format of unpaired students in a list
    def __repr__(self) -> str:
        print("teams:", self.teams)
        print("not_paired_stud", self.not_paired_stud)
        return '---------'

    # def __str__(self) -> str:
    #     print("teams:", self.teams)
    #     print("not_paired_stud", self.not_paired_stud)
    #     return ''

# this function is defined to check whether the reached state is goal state or not
def check_goal_state(state):
    return len(state.not_paired_stud) == 0

# this function takes input as a new team assignment element and checks whether the new element has already been visited
# by comparing the new element with other visited elements in the fringe
def check_fringe(element, fringe):
    for fringe_element_priority, fringe_element_state in fringe:
        if element.teams == fringe_element_state.teams:
            return True, (fringe_element_priority, fringe_element_state)
    return False, None



# cost function: this cost function checks the conditions for preferred team size, unwanted students, etc... and
# add the time accordingly to calculate the total time for grading the assignments.
def get_priority(state, stud_dictionary):
    time = 0
    for team in state.teams:
        time += 5  # grading time for each team, i.e 5 minutes per team
        team_size = len(team)
        for student_name in team:
            student = stud_dictionary[student_name]

            # grading time for assigning not preferred team size, i.e. 2 minutes
            if student['wanted_team_size'] != team_size:
                time += 2

            # calculating time for students who are not assigned to their preferred choice teammate and the chance that they share code, i.e 3 mins
            student_choice = student['preference']
            for preference in student_choice:
                if preference not in team:
                    time += (5 / 100) * 60

            # calculating the time when students are assigned with not preferred teammates, i.e 10 mins
            team_without_this_student = [s for s in team if s != student]
            for s in team_without_this_student:
                if s in student['unwanted']:
                    time += 10
    time += 4 * len(state.not_paired_stud)
    return time

# this is the successor function, where we traverse through each element and see the various possibilities of team
# assignments and store the successors in a successor list so as to use them while assigning the teams and calculating the time
def get_successors(state):
    successor_states = []
    for unpaired_student in state.not_paired_stud:
        # initial state would look like this:
        # {'teams': [[]], 'not_paired_stud': initial_stud}
        successor_states.append(
            State(
                teams=state.teams + [[unpaired_student]],
                not_paired_stud=[
                    student for student in state.not_paired_stud if student != unpaired_student]
            )
        )
        for team in state.teams:
            if len(team) >= 3:
                continue
            else:
                new_team = team + [unpaired_student]
                # print(new_team)
                team_no_repeat = [t for t in state.teams if t != team]
                successor_states.append(State(teams=team_no_repeat + [new_team],
                                              not_paired_stud=[student for student in state.not_paired_stud if
                                                                 student != unpaired_student]
                                              ))

        successor_states.append(State(teams=state.teams + [[unpaired_student]],
                                      not_paired_stud=[
                                          student for student in state.not_paired_stud if student != unpaired_student]
                                      ))

    return successor_states

# this function applies A* algorithm taught in class and we use the successor function, priority function to compute the
# best possible and efficient team assignment so as to reduce the grading time
def solve(initial_state, students_dict):
    fringe = []
    closed = []
    if check_goal_state(initial_state):
        final_state = initial_state
    else:
        initial_state.set_priority(0) # setting the initial state priority to 0
        # adding the state and its priority in a heapq to compare it with other states.
        heapq.heappush(fringe, (initial_state.priority, initial_state))

    while fringe:

        state_priority, state = heapq.heappop(fringe)
        state.set_priority(state_priority)
        print("exploring:", state_priority, state)
        closed.append(state)
        if check_goal_state(state):
            final_state = state
            break
        else:
            for successor_state in get_successors(state):
                successor_state.set_priority(
                    get_priority(successor_state, students_dict))

                if successor_state in closed:
                    continue

                successor_state_in_fringe, f = check_fringe(successor_state, fringe)
                if successor_state_in_fringe:
                    fringe_priority, fringe_state = f
                    if successor_state.priority < fringe_state.priority:
                        fringe.remove((fringe_priority, fringe_state))

                successor_state_in_fringe, f = check_fringe(successor_state, fringe)
                if not successor_state_in_fringe:
                    heapq.heappush(
                        fringe,
                        (successor_state.priority, successor_state)
                    )
    return final_state.teams, get_priority(final_state, students_dict)

# this function reads the text file of team preferences given by students and stores a readable format to compute in
# a dictionary and list so as to use it for all the computations taking place.
# And after completing the computation it gives the output in a desired format as asked in assignment.
def solver(input_file):
    students = {}
    initial_students_list = []
    with open(input_file) as file:
        input_lines = file.readlines()

    file_list = [[stud for stud in item.split()] for item in input_lines]

    for l in file_list:
        initial_students_list.append(l[0])
        students[l[0]] = {'name': l[0],
                          'preference': [s for s in l[1].split('-') if s != 'xxx'],
                          'unwanted': l[2].split(','),
                          'wanted_team_size': len(l[1].split('-'))}

    initial_state = State(teams=[[]], not_paired_stud=initial_students_list)
    end_teams, priority = solve(initial_state, students)

    print(end_teams)
    desired_list = ['-'.join(x) for x in end_teams]

    print(priority)

    yield ({"assigned-groups": desired_list,
            "total-cost": priority})
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """




if __name__ == "__main__":
    if (len(sys.argv) != 2):
        raise (Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d\n" % result["total-cost"])

