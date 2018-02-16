import sys              #To use functions defined in the sys Module
from re import sub      #To use sub function in regular expression matching operations to locate the co-ordinates from a series of paranthesis, commas, etc.

class CoordinatePoint:  #Implementing class CoordinatePoint to determine if one bridge will cross another and to create many instances of coordinates mentioned in the input file to join bridges

    def __init__(self, x ,y):       #self is the new object in __init__method. It is an instance of CoordinatePoint Class. x and y are the parameters passed at initialization time

        self.x = x                  #self.x and self.y represent the coordinates of a single point for the many point instances that we create
        self.y = y

class BayBridge:        #Implementing a class BayBridge to determine if one bridge will cross another
    def __init__(self, l, m, n):    #self is an instance of BayBridge Class.
        self.l = l                  #l represents the line
        self.m = m                  #m represents the first coordinate of line             
        self.n = n                  #n represents the second coordinate of line

def CounterClockwise(A, B, C):      #This function checks if 3 points taken (say A, B, C) are placed counter clockwise of each other or not
    return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)        #if the slope of line AC is greater than the slope of line AB, then the three points are counter clockwise
                                                            #returns boolean result, true or false

def Intersect(A, B, C, D):          
	 return CounterClockwise(A,C,D) != CounterClockwise(B,C,D) and CounterClockwise(A,B,C) != CounterClockwise(A,B,D)   #This function checks if the four points are    intersecting or not. They are intersecting if A,B are separated by CD or C,D are separated by AB.    
                                                                                                                        #returns boolean result, true or false
myfile = open(sys.argv[1], 'r')     #creating variable for storing the test cases, create a file object with read only(r) previledge
bridges = list()                    #creating a list for the bridges we are going to build

for test in myfile:                 #read file line by line         

	if test.strip() == '':        #check if the line is empty
		continue

	BridgeNumber, Mark = test.split(':')    #store the bridge number mentioned in the given sample input(left most character before each set of coordinates)
                                            #Mark is the bookmark to store the BridgeNumber so that it can be split later
	BridgeCoordinates = list()              #creating a list for the coordinates of bridges

	for point in Mark.split(','):                                       #to get the the coordinates from the input text file and append it to the BridgeCoordinates list 
		BridgeCoordinates.append(float(sub("[^0-9.-]", "", point)))     #using regular expression and convert the string type to float type

	m = CoordinatePoint(BridgeCoordinates[0], BridgeCoordinates[1])     #creating coordinate objects for the points and bridges, m(x1, y1) and n(x2, y2)
	n = CoordinatePoint(BridgeCoordinates[2], BridgeCoordinates[3])
	BridgeNumber = BayBridge(int(BridgeNumber), m, n)
	bridges.append(BridgeNumber)                                        #appending the bridge number to the BridgeNumber list

def PrintBridges(bridges):          #function to print the bridge location
	for bridge in bridges:
		print bridge


def PrintBridgeNumber(bridges):     #function to print the bridge number
	Bnum = list()

	for bridge in bridges:
		Bnum.append(bridge.l)
	Bnum.sort()

	for num in Bnum:
		print num

myfile.close()                      #closes the file object myfile

def Intersections(BridgeNumber, bridges):       #this fuction calculates the no of intersections to further determine if the 2 bridges cross or not
	count = 0                                   

	for BridgeNumber2 in bridges:

		if BridgeNumber.l == BridgeNumber2.l:
			continue

		if Intersect(BridgeNumber.m, BridgeNumber.n, BridgeNumber2.m, BridgeNumber2.n):
			count += 1

	return count

SafeBridges = list()                #creating a list for the bridges that do not intersect
UnsafeBridges = list()              #creating a list for the bridges that intersect

while len(bridges) > 0:             #using this while loop we sort the lines which have no intersections and the lines which have one or more than one intersection

	MaxIntersections = 0
	MaxBridge = {}

	for x in bridges:

		count = Intersections(x, bridges)

		if count == 0:
			SafeBridges.append(x)   #if the line has no intersections, append to the SafeBridges list

		elif count >= MaxIntersections:     #if the line has intersections, set the count of intersections
			MaxIntersections = count        #edit the count of intersections(MaxIntersections) if the number of intersections for the line is increased
			MaxBridge = x

	if MaxBridge:                   #append the bridges with intersections to the UnsafeBridges list
		bridges.remove(MaxBridge)
		UnsafeBridges.append(MaxBridge)

	for x in SafeBridges:           #check the Bridges list such that it does not contain any bridges which are in the SafeBridges list
		if x in bridges:            #if so remove them from the bridges list
			bridges.remove(x)

PrintBridgeNumber(SafeBridges)      #print the SafeBridges list



