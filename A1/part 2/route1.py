# !/usr/bin/env python3
import sys

# !/usr/bin/env python3
import sys
import math
import heapq
import random


# dichalla: read_data class contains functions required for loading data from txt files.
class read_data:
    road_segments = {}
    city_gps = {}

    # dichalla: access pattern for road_segments for this problem would be given a city, find all successors, i.e all roads connected  to the city.
    # dichalla: So, I am choosing the following structure {city1:{city2:(values),city3:(values)}}.
    # dichalla: values are length,speed limit, road_name
    def load_road_segments(self, filename='./road-segments.txt'):
        with open(filename, 'r') as f:
            for line in f.readlines():
                city1, city2, length, speed_limit, road_name = line.strip().split()
                length = float(length)
                speed_limit = float(speed_limit)
                # dichalla: python3 throws keyerror for dict[a][b] if key a is not present in dict. It doesn't create a new one.
                if (city1 not in self.road_segments):
                    self.road_segments[city1] = {}
                self.road_segments[city1][city2] = (length, speed_limit, road_name)

                # dichalla: creating 2 elements as the paths are bidirectional.
                if (city2 not in self.road_segments):
                    self.road_segments[city2] = {}
                self.road_segments[city2][city1] = (length, speed_limit, road_name)

        pass

    def get_road_segments(self):
        return self.road_segments

    # dichalla: structure for city gps is a json/dictionary as {city1:(latitude, longitude)}
    # dichalla: Choosing the above structure as access requirement of city_gps would only be to fetch latitude and longitude given cityname.
    def load_city_gps(self, filename='./city-gps.txt'):
        with open(filename, 'r') as f:
            for line in f.readlines():
                city, latitude, longitude = line.strip().split()
                # dichalla: typecasting latitude and longtiude to float to be able to use them to calculate eucledian distance
                self.city_gps[city] = (float(latitude), float(longitude))

    def get_city_gps(self):
        return self.city_gps


# dichalla: state object will hold city name and details of path taken so far.
class State:
    def __init__(self, city, segments, miles, hours, delivery_hours, route_sofar):
        self.city = city
        self.segments = segments
        self.miles = miles
        self.hours = hours
        self.delivery_hours = delivery_hours
        self.route_sofar = route_sofar

    def get_coordinates(self, city_gps):
        return city_gps[self.city]

    # dichalla: overiding equals function in python to compare 2 states
    def _eq_(self, other):
        return self.city == other.city

    # dichalla: sets priority of state (f(n)+h(n))
    def set_priority(self, priority):
        self.priority = priority

    # dichalla: heapq uses state1<state2 if priorities are same.
    # dichalla: The below functions just picks any state at random when 2 states have same priority.
    def _lt_(self, other):
        # return False
        return bool(random.getrandbits(1))

    def _le_(self, other):
        # return False
        return bool(random.getrandbits(1))


class Solver:
    road_segments = {}
    city_gps = {}
    start_city = ''
    end_city = ''
    cost = ''

    def __init__(self, road_segments, city_gps, start_city, end_city, cost):
        self.road_segments = road_segments
        self.city_gps = city_gps
        self.start_city = start_city
        self.end_city = end_city
        self.cost = cost
        self.end_city_coordinates = city_gps[end_city]

    # TODO: handle if None ( optional )
    def get_successors(self, s):
        successor_states = []
        for city, (length, speed_limit, road_name) in self.road_segments[s.city].items():
            successor_state = State(
                city=city,
                segments=s.segments + 1,
                miles=s.miles + length,
                hours=s.hours + (length / speed_limit),
                # TODO: consider probability
                delivery_hours=s.hours + (length / speed_limit),
                route_sofar=s.route_sofar + [(city, road_name + ' for ' + str(length) + ' miles')],
                # TODO: format route sofar
            )
            successor_states.append(successor_state)
        return successor_states

    # dichalla: checks if a state is goal state
    def is_goal_state(self, state):
        return state.city == self.end_city

    # dichalla: Cannot use eucleadian distance, as latitude and longitude are given.
    def eucledian_distance(self, p1, p2):
        return math.sqrt(
            ((p1[0] - p2[0]) * 2) + ((p1[1] - p2[1]) * 2)
        )

    # dichalla: distancd function is taken from https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    def distance(self, origin, destination):
        """
        Calculate the Haversine distance.
        Parameters
        ----------
        origin : tuple of float
            (lat, long)
        destination : tuple of float
            (lat, long)
        Returns
        -------
        distance_in_km : float
        Examples
        --------
        >>> origin = (48.1372, 11.5756)  # Munich
        >>> destination = (52.5186, 13.4083)  # Berlin
        >>> round(distance(origin, destination), 1)
        504.2
        """
        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = 6378.1  # km

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) * math.sin(dlon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c

        return d * 0.62137  # dichalla: conversion to miles

    # dichalla: get_heuristic function calculates h(n), heuristic of the state.
    # dichalla: Calculated using latitude and longitude of current state and end state.

    def get_heuristic_distance(self, state):
        # dichalla: using 0 as heuristic for cities that don't have details in city-gps, as 0 is always admissible.
        if (state.city not in self.city_gps):
            return 0
        state_coordinates = self.city_gps[state.city]
        return self.distance(state_coordinates, self.end_city_coordinates)

    # dichalla: get_priority function calculates g(n)=f(n)+h(n). This is used to pop elements of the fringe

    def get_priority(self, state, cost_function='distance'):
        '''dichalla: With the given information, (latitude,longitude), I coouldn't think of a possible way to estimate
        heuristic for segments cost function. for example, There could be a lot of segments within short distance between
        2 points(latitude,longitude). Hence I am using 0 as heuristic for 'segments' cost function.
        '''
        if cost_function == 'segments':
            return state.segments + 0

        heuristic_distance_of_state = self.get_heuristic_distance(state)  # dichalla: h(n) for current state
        if cost_function == 'distance':
            return state.miles + heuristic_distance_of_state

        if cost_function == 'time':
            max_speed = 50
            return state.hours + (heuristic_distance_of_state / max_speed)
        if cost_function == 'delivery':
            max_speed = 50
            return state.delivery_hours + (heuristic_distance_of_state / max_speed)


# dichalla: helper functions
class util_funs:

    # dichalla: checks if an element is in fringe. returns (True,False) or (False,None)
    def is_in_fringe(self, element, fringe):
        for fringe_element_priority, fringe_element_state in fringe:
            if (element.city == fringe_element_state.city):
                return True, (fringe_element_priority, fringe_element_state)
        return False, None


def get_route(start, end, cost):
    """
    Find shortest driving route between start city and end city
    based on a cost function.
    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    # read data from txt files
    data = read_data()
    data.load_city_gps(filename='./city-gps.txt')
    data.load_road_segments(filename='./road-segments.txt')
    solver = Solver(road_segments=data.get_road_segments(), city_gps=data.get_city_gps(
    ), start_city=start, end_city=end, cost=cost)
    del data

    # set initial state
    initial_state = State(
        city=start,
        segments=0,
        miles=0,
        hours=0,
        delivery_hours=0,
        route_sofar=[]
    )

    util = util_funs()

    # dichalla: A* algorithm implementation using Algorithm #3 mentioned in lectures.
    fringe = []
    closed = []
    if (solver.is_goal_state(initial_state)):
        final_state = initial_state
    else:
        initial_state.set_priority(0)
        heapq.heappush(fringe, (initial_state.priority, initial_state))

    while (fringe):

        s_priority, s = heapq.heappop(fringe)
        s.set_priority(s_priority)
        closed.append(s)
        if (solver.is_goal_state(s)):
            final_state = s
            break
        else:
            for successor_state in solver.get_successors(s):
                successor_state.set_priority(solver.get_priority(successor_state))

                # dichalla: if a successor_state in closed, discard it.
                if successor_state in closed:
                    continue

                # dichalla: check if a successor city is already present in fringe with higher priority than current successor and remove it.
                ss_in_fringe, f = util.is_in_fringe(successor_state, fringe)
                if (ss_in_fringe):
                    fp, fs = f
                    if successor_state.priority < fs.priority:
                        fringe.remove((fp, fs))

                # dichalla: insert successor state if not exists in fringe.
                ss_in_fringe, f = util.is_in_fringe(successor_state, fringe)
                if not ss_in_fringe:
                    heapq.heappush(fringe, (successor_state.priority, successor_state))

    # route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
    #                ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
    #                ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    route_taken = final_state.route_sofar
    return {"total-segments": len(route_taken),
            "total-miles": final_state.miles,
            "total-hours": final_state.hours,
            "total-delivery-hours": final_state.delivery_hours,
            "route-taken": route_taken}


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise (Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise (Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])