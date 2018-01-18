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

'''
Robot Actions
'''


def lowTemp(ofNum):
    rooms[ofNum][0] = rooms[ofNum][0] - 1.


def raiseTemp(ofNum):
    rooms[ofNum][0] = rooms[ofNum][0] + 1.

def raiseHum(ofNum):
    # print("Before going through hig ", rooms[ofNum][1])
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


def adjustAverage(curTem, curHum, temPercent, humPercent, office):
    if curHum > 48. and curTem > 73.:
        if temPercent > humPercent:
            lowTemp(office)
        else:
            lowHum(office)
    if curHum < 48. and curTem < 73.:
        if temPercent > humPercent:
            raiseTemp(office)
        else:
            raiseHum(office)

    if curHum < 48. and curTem > 73.:
        if temPercent > humPercent:
            lowTemp(office)
        else:
            raiseHum(office)

    if curHum > 48. and curTem < 73.:
        if temPercent > humPercent:
            raiseTemp(office)
        else:
            lowHum(office)



def adjustStd(curTem, curHum, temPercent, humPercent,office):
    if stdRooms("Tem") > 1.5 and stdRooms("Hum") > 1.7:

        if curHum > 47 and curTem > 72:
            if temPercent > humPercent:
                lowTemp(office)
            else:
                lowHum(office)
        if curHum < 47 and curTem < 72:
            if temPercent > humPercent:
                raiseTemp(office)
            else:
                raiseHum(office)

        if curHum < 47 and curTem > 72:
            if temPercent > humPercent:
                lowTemp(office)
            else:
                raiseHum(office)

        if curHum > 47 and curTem < 72:
            if temPercent > humPercent:
                raiseTemp(office)
            else:
                lowHum(office)
    elif stdRooms("Tem") > 1.5:
        if curTem > 72.:
            lowTemp(office)
        elif curTem < 71.:
            raiseTemp(office)
    else:

        if curHum > 47.:
            lowHum(office)
        elif curHum < 46.:
            raiseHum(office)

while (math.ceil(averageRooms("Tem")) != 73 or math.ceil(averageRooms("Hum")) != 48 or stdRooms(
        "Tem") > 1.5 or stdRooms("Hum") > 1.7):
    curTem = rooms[office][0][0]
    curHum = rooms[office][1][0]
    temPercent = math.fabs(72. - curTem) / math.fabs(maxTem - minTem)
    humPercent = math.fabs(47. - curHum) / math.fabs(maxHum - minHum)
    if math.ceil(averageRooms("Tem")) not in range(72, 73) and math.ceil(averageRooms("Hum")) not in range(47, 48):
        adjustAverage(curTem,curHum,temPercent, humPercent, office)
        print("it reached")
    elif stdRooms("Tem") > 1.5 or stdRooms("Hum") > 1.7:
        adjustStd(curTem,curHum,temPercent, humPercent,office)

    print("This is the std  ", stdRooms())
    print("This is the temperature", averageRooms())

    office += 1
    if office == 11:
        trialCount += 1
        office = 0
#
# while (stdRooms("Tem") > 1.5 or stdRooms("Hum") > 1.7):
#     curTem = rooms[office][0][0]
#     curHum = rooms[office][1][0]
#     temPercent = math.fabs(72 - curTem) / math.fabs(maxTem - minTem)
#     humPercent = math.fabs(47 - curHum) / math.fabs(maxHum - minHum)
#
#     if stdRooms("Tem") > 1.5 and stdRooms("Hum") > 1.7:
#
#         if curHum > 47 and curTem > 72:
#             if temPercent > humPercent:
#                 lowTemp(office)
#             else:
#                 lowHum(office)
#         if curHum < 47 and curTem < 72:
#             if temPercent > humPercent:
#                 raiseTemp(office)
#             else:
#                 raiseHum(office)
#
#         if curHum < 47 and curTem > 72:
#             if temPercent > humPercent:
#                 lowTemp(office)
#             else:
#                 raiseHum(office)
#
#         if curHum > 47 and curTem < 72:
#             if temPercent > humPercent:
#                 raiseTemp(office)
#             else:
#                 lowHum(office)
#     elif stdRooms("Tem") > 1.5:
#         if curTem > 72.:
#             lowTemp(office)
#         elif curTem < 71.:
#             raiseTemp(office)
#     else:
#
#         if curHum > 47.:
#             lowHum(office)
#         elif curHum < 46.:
#             raiseHum(office)
#     # print(rooms)
#     office += 1
#     if office == 11:
#         trialCount += 1
#         office = 0
#     # print(rooms[office])
#     print("This is the std  ", stdRooms())
#     #if math.ceil(averageRooms("Tem")) not in range(72, 73) and math.ceil(averageRooms("Hum")) not in range(47, 48):

print(trialCount)
print(stdRooms())
print(averageRooms())

'''


Questions:

do we have to go to all rooms to get the average of the general?
it knows only the temperature  an humidity of the average
knows the new 

if we were able to give him the information of all the rooms to him it would be better?

clueless with the exception of the average and standard deviation. 

'''





