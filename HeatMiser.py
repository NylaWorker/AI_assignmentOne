import numpy as np
import math
import decimal

'''
Generating initial conditions of the 12 rooms. 
'''
maxTem = 75.
minTem = 65.
maxHum = 55.
minHum = 45.
temps = np.random.uniform(low=minTem, high=maxTem, size=(12,))[np.newaxis]
humidity = np.random.uniform(low=minHum, high=maxHum, size=(12,))[np.newaxis]
rooms = np.stack((temps.T, humidity.T), axis=1)
print("The initial condition of the offices")
print(rooms.T)

'''
Robot Actions
'''


def lowTemp(ofNum):
    rooms[ofNum][0] = rooms[ofNum][0] - 1.


def raiseTemp(ofNum):
    rooms[ofNum][0] = rooms[ofNum][0] + 1.


def raiseHum(ofNum):
    rooms[ofNum][1] = rooms[ofNum][1] + 1.


def lowHum(ofNum):
    rooms[ofNum][1] = rooms[ofNum][1] - 1.


def stdRooms(opt="Both"):
    if opt == "Tem":
        return np.std(rooms.T, axis=2)[0][0]
    elif opt == "Hum":
        return np.std(rooms.T, axis=2)[0][1]
    else:
        return np.std(rooms.T, axis=2)


def averageRooms(opt="Both"):
    if opt == "Tem":
        return np.average(rooms.T, axis=2)[0][0]
    elif opt == "Hum":
        return np.average(rooms.T, axis=2)[0][1]
    else:
        return np.average(rooms.T, axis=2)


'''
Simmulation

'''
trialCount = 0
office = 0
n = 0

'''
In this solution HeatMiser will change the temperature or humidity of each room it visits, so long it is not in the desired range.
The distance is evaluated in each room. Which one is farther from the ideal average?
For that the following formula is used:
abs(idealAverage - current office value)/abs(maximum value and minimum value)

'''

while (math.ceil(averageRooms("Tem")) != 73 or math.ceil(averageRooms("Hum")) != 48 or stdRooms(
        "Tem") > 1.5 or stdRooms("Hum") > 1.7):
    curTem = rooms[office][0][0]
    curHum = rooms[office][1][0]
    temPercent = math.fabs(72. - curTem) / math.fabs(maxTem - minTem)
    humPercent = math.fabs(47. - curHum) / math.fabs(maxHum - minHum)
    # print("This is he current room ")
    if math.ceil(averageRooms("Tem")) != 73 or math.ceil(averageRooms("Hum")):
        if curHum > 48. and curTem > 73.:
            if temPercent > humPercent:
                lowTemp(office)
            else:
                lowHum(office)
        elif curHum < 47. and curTem < 73.:
            if temPercent > humPercent:
                raiseTemp(office)
            else:
                raiseHum(office)

        elif curHum < 47. and curTem > 73.:
            if temPercent > humPercent:
                lowTemp(office)
            else:
                raiseHum(office)

        elif curHum > 48. and curTem < 73.:
            if temPercent > humPercent:
                raiseTemp(office)
            else:
                lowHum(office)

    elif stdRooms("Tem") > 1.5 and stdRooms("Hum") > 1.7:
        if curHum > 48. and curTem > 73.:
            if temPercent > humPercent:
                lowTemp(office)
            else:
                lowHum(office)
        elif curHum < 47. and curTem < 73.:
            if temPercent > humPercent:
                raiseTemp(office)
            else:
                raiseHum(office)

        elif curHum < 47. and curTem > 73.:
            if temPercent > humPercent:
                lowTemp(office)
            else:
                raiseHum(office)

        elif curHum > 48. and curTem < 73.:
            if temPercent > humPercent:
                raiseTemp(office)
            else:
                lowHum(office)
    elif stdRooms("Tem") > 1.5:
        if curTem > 73:
            lowTemp(office)
        else:
            raiseTemp(office)
    else:
        if curHum >48:
            lowHum(office)
        else:
            raiseHum(office)

    office += 1
    if office == 11:
        trialCount += 1
        office = 0
    # print("This is the trial count ", trialCount)
    # print("This is the current room after the run", rooms[office])
    print("This is std")
    print(stdRooms())
    print("this is the average")
    print(averageRooms())

print(trialCount)
print("This is the final std", stdRooms())
print("This is the final ave", averageRooms())
print(" This is the final condition of the rooms")
print(rooms.T)
