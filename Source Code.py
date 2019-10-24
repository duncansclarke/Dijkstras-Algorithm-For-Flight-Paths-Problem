# Duncan Clarke
# 20056561
# I certify that this submission contains my own work, except as noted.

start = 61
end = 65

class Flight:
    """ A flight path from one city to another.
    Attributes
    ---------------
    departure_city (int):
        The starting point of the flight path
    arrival_city (int):
        The destination of the flight path
    departure_time (int):
        The universal time of the flight departure
    arrival_time (int):
        The universal time of the flight arrival
    """
    def __init__(self, departure_city, arrival_city, departure_time, arrival_time=0):
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        self.departure_time = departure_time
        self.arrival_time = arrival_time


# Opens and reads file containing flight data, saving the number of cities in a variable and separating the flight data
file = open("2019_Lab_2_flights_real_data.txt", "r")
city_count = int(file.readline())
subsequent_lines = file.readlines()[0:]

# Reads the flight data and stores each flight in a list of flight objects, each containing the data of its flight
# Keeps track of each city in a list of vertices
flights = []
vertices = []
for line in subsequent_lines:
    current_line = line.split('\t') # separate line into each piece of flight data
    current_line[3] = current_line[3].replace('\n',  '') # remove new line formatting
    current_line = list(map(int, current_line)) # store the flight data in a list
    flights.append(Flight(current_line[0], current_line[1], current_line[2], current_line[3])) # create flight object containing the data

    # check if the departure or arrival cities are in the vertices array... add them if not
    if current_line[0] not in vertices:
        vertices.append(current_line[0])
    if current_line[1] not in vertices:
        vertices.append(current_line[1])


def dijkstra(flights, vertices, city_count, start, end):
    """ Determines the shortest flight path from a start city to a destination city, along with the corresponding arrival time of the optimal path.
    Parameters
    ---------------
    flights (list):
        all flight objects with flight data
    vertices (list):
        all possible cities for travel
    city_count (int):
        how many cities can be traveled to
    start (int):
        the starting city
    end (int):
        the desired destination city
    """

    # creates a list keeping track of which cities have been visited, and sets the starting city to visited
    reached = [False] * city_count
    reached[start] = True

    # creates a list to keep track of the earliest estimated arrival time found for each city
    estimates = [float("inf")] * city_count
    estimates[start] = 0

    # creates a list to keep track of the absolute earliest possible arrival time for each city
    earliest = [float("inf")] * city_count
    earliest[start] = 0

    # creates a list of possible candidates for destination cities on the path. initializes each city as a non-candidate
    candidate = [False] * city_count

    # creates a list keeping track of which city precedes which in the flight path
    predecessor = [None] * city_count

    # find every neighbor of the starting city and call them candidates
    # keeps track of the earliest arrival times for each neighboring city
    for flight in flights:
        if flight.departure_city == start:
            if flight.arrival_time < estimates[flight.arrival_city] :
                estimates[flight.arrival_city] = flight.arrival_time
                candidate[flight.arrival_city] = True
                predecessor[flight.arrival_city] = start

    while reached[end] == False:
        best_candidate_estimate = float("inf")
        for flight in flights:
            if (candidate[flight.arrival_city] == True):
                if earliest[flight.departure_city] < flight.departure_time and (estimates[flight.arrival_city] < best_candidate_estimate):
                    city = flight.arrival_city
                    best_candidate_estimate = estimates[city]
        earliest[city] = estimates[city]
        reached[city] = True
        candidate[city] = False
        # update the estimated arrival times of the neighboring cities
        for flight in flights:
            # check if flight goes to neighboring city and makes sure the neighbor hasn't been visited already
            if flight.departure_city == city and reached[flight.arrival_city] == False :
                # makes sure the flight leaves after we have arrived at the departure city
                if (flight.departure_time > earliest[city]) and (flight.arrival_time < estimates[flight.arrival_city]) :
                    estimates[flight.arrival_city] = flight.arrival_time
                    candidate[flight.arrival_city] = True
                    predecessor[flight.arrival_city] = city


    # creates a list of the optimal path traveled from the start to the destination

    # accounts for the case where the destination city is the starting city
    if start == end :
        path = [start, end]
        printPath(path, earliest[end])

    # accounts for the case where the destination city cannot be reached from the starting city
    elif predecessor[end] == None :
        print('\nThere is no route from ' + str(start) + ' to ' + str(end) + '\n')

    else:
        # works backwards, building the flight path from the end point with the predecessor list
        path = [end]
        cur = end
        while predecessor[cur] is not None:
            cur = predecessor[path[-1]]
            path.append(cur)
        # reverses the list to return the full flight path
        path.reverse()
        # prints the optimal flight path
        printPath(path, earliest[end])


def printPath(path, arrival_time):
    """ Prints a flight path from a list of destinations along the path.
    Parameters
    ---------------
    path (list):
        the list of cities in order of their position in the flight path
    arrival_time (int):
        the final arrival time in the flight path
    """
    print('Optimal route from ' + str(path[0]) + ' to ' + str(path[-1]) + '\n')
    for i in range(1, len(path)):
        print('Fly from ' + str(path[i-1]) + ' to ' + str(path[i]))
    print('\nArrive at ' + str(path[-1]) + ' at time ' + str(arrival_time))


def main():
    dijkstra(flights, vertices, city_count, start, end)

if __name__== "__main__":
  main()
