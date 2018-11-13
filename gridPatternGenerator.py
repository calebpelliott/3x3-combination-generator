import copy

#Template used to print map
#   TL | TM | TR
#   ------------
#   ML | MM | MR
#   ------------
#   BL | BM | BR

template="""#   TL | TM | TR
#   ------------
#   ML | MM | MR
#   ------------
#   BL | BM | BR"""

#All possible points
allPoints = ["TL","TM","TR","ML","MM","MR","BL","BM","BR"]

#All points immediately visible to a given point
availToTL = ["TM", "ML", "MM", "MR", "BM"]
availToTM = ["TL", "TR", "ML", "MM", "MR", "BL", "BR"]
availToTR = ["TM", "ML", "MM", "MR", "BM"]
availToML = ["TL", "TM", "TR", "MM", "BL", "BM", "BR"]
availToMM = ["TL", "TM", "TR", "ML", "MR", "BL", "BM", "BR"]
availToMR = ["TL", "TM", "TR", "MM", "BL", "BM", "BR"]
availToBL = ["TM", "ML", "MM", "MR", "BM"]
availToBM = ["TL", "TR", "ML", "MM", "MR", "BL", "BR"]
availToBR = ["TM", "ML", "MM", "MR", "BM"]

#Dictionary to use point to get its corresponding list above
pointDict = {
    "TL": availToTL,
    "TM": availToTM,
    "TR": availToTR,
    "ML": availToML,
    "MM": availToMM,
    "MR": availToMR,
    "BL": availToBL,
    "BM": availToBM,
    "BR": availToBR
}

#Used to prove uniqueness of set of passwords
patternSet = set([])

#Prints out the map, the order of points, and the number of combinations found
def printShape(list, count):
    #Create deep copy because we don't want to be changing it
    local = copy.deepcopy(allPoints)

    #Leaves local with points that haven't been used
    for point in list:
        local.remove(point)

    localTem = template

    #Replace those points with blanks
    for point in local:
        localTem = localTem.replace(point, "  ")

    #Build the order of points
    order = ""

    for point in list:
        order += point + "->"
    #Strip off the appending ->
    order = order[:-2]

    print(localTem)
    print("Combination Number: " + str(count))
    print(order + "\n")

    if order not in patternSet:
        patternSet.add(order)
    else:
        print("DUPLICATE FOUND!")
        raise (Exception)

#Create a list of points visible to the currentPoint
#Brute force way of doing this. Quickly becomes unreasonably difficult to implement for any N x M grid, where N and M
#are reasonable sizes
def getAvailablePoints(currentPoint, localUsedPoints):
    #baseSet is the set of points assumed to be viewable by default
    baseSet = pointDict.get(currentPoint)

    #The final set of points viewable to the current point
    finalSet = []

    #Add points from the baseSet only if it hasn't been used
    for point in baseSet:
        if point not in localUsedPoints:
            finalSet.append(point)

    if currentPoint is "TL":
        if "TM" in localUsedPoints and "TR" not in finalSet:
            finalSet.append("TR")

        if "MM" in localUsedPoints and "BR" not in finalSet:
            finalSet.append("BR")

        if "ML" in localUsedPoints and "BL" not in finalSet:
            finalSet.append("BL")

    elif currentPoint is "TM":
        if "MM" in localUsedPoints and "BM" not in finalSet:
            finalSet.append("BM")

    elif currentPoint is "TR":
        if "TM" in localUsedPoints and "TL" not in finalSet:
            finalSet.append("TL")

        if "MM" in localUsedPoints and "BL" not in finalSet:
            finalSet.append("BL")

        if "MR" in localUsedPoints and "BR" not in finalSet:
            finalSet.append("BR")

    elif currentPoint is "ML":
        if "MM" in localUsedPoints and "MR" not in finalSet:
            finalSet.append("MR")

    #Don't need to check MM. All points are always visible to it.
    #   elif currentPoint is "MM":

    elif currentPoint is "MR":
        if "MM" in localUsedPoints and "ML" not in finalSet:
            finalSet.append("ML")

    elif currentPoint is "BL":
        if "ML" in localUsedPoints and "TL" not in finalSet:
            finalSet.append("TL")

        if "MM" in localUsedPoints and "TR" not in finalSet:
            finalSet.append("TR")

        if "BM" in localUsedPoints and "BR" not in finalSet:
            finalSet.append("BR")

    elif currentPoint is "BM":
        if "MM" in localUsedPoints and "TM" not in finalSet:
            finalSet.append("TM")

    elif currentPoint is "BR":
        if "MM" in localUsedPoints and "TL" not in finalSet:
            finalSet.append("TL")

        if "MR" in localUsedPoints and "TR" not in finalSet:
            finalSet.append("TR")

        if "BM" in localUsedPoints and "BL" not in finalSet:
            finalSet.append("BL")

    return finalSet

#Recursive function to traverse the grid
def goToPoint(usedPoints, counter, counter4):
    locaUsedPoints = copy.deepcopy(usedPoints)
    # Our current point is the point at the end of the list
    currentPoint = locaUsedPoints[-1]

    #Find the points available to go to based on the current point and points that have been used
    localAvailPoints = getAvailablePoints(currentPoint, locaUsedPoints)

    #Update counter
    counter += 1
    if len(usedPoints) >= 4:
        counter4 += 1

    #Print the grid
    printShape(locaUsedPoints, counter)


    #Iterate through the point available to the current point
    for availPoint in localAvailPoints:
        #Go to the point if it hasn't been used
        if availPoint not in locaUsedPoints:
            locaUsedPoints.append(availPoint)
            #Always need to refresh location to original usedPoints for every available point
            location = copy.deepcopy(usedPoints)
            location.append(availPoint)
            [counter, counter4] = goToPoint(location, counter, counter4)

    return [counter, counter4]

#Total will be the number of patterns possible for length > 0
#Total4 will be the number of patterns possible for length >3 (This is a condition for Samsung's grid password)
total = total4 = 0
for point in allPoints:
    [newtotal, newtotal4] = goToPoint([point], 0, 0)
    total += newtotal
    total4 += newtotal4


for key in patternSet:
    removedArrows = key.split("->")

    #Ensure all patterns are possible lengths
    if len(removedArrows) > 9:
        print("Invalid length of password found: " + key)
        raise (Exception)

    #Ensure there are no duplications of points (e.g. MM->TR->MM->...)
    for point in allPoints:
        if point in removedArrows:
            removedArrows.remove(point)

    if len(removedArrows) > 0:
        print("Point duplication found in pattern: " + key)
        raise (Exception)

print("Total number of combinations with length > 0 possible: " + str(total))
print("Total number of combinations with length > 3 possible: " + str(total4))