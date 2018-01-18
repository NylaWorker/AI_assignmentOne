import numpy as np
import math
import decimal
import csv

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


def baseAlgorithm(curTem, curHum, temPercent, humPercent, office):
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
        # raiseHum(office)
        if temPercent > humPercent:
            lowTemp(office)
        else:
            raiseHum(office)

    elif curHum > 48. and curTem < 73.:
        ##raiseTemp(office)
        if temPercent > humPercent:
            raiseTemp(office)
        else:
            lowHum(office)


'''
Simmulation

'''
trialCount = 0
office = 0
n = 1 # to fix convergence issue

'''
In this solution HeatMiser will change the temperature or humidity of each room it visits, so long it is not in the desired range.
The distance is evaluated in each room. Which one is farther from the ideal average?
For that the following formula is used:
abs(idealAverage - current office value)/abs(maximum value and minimum value)

'''
runs = 0
humAveIss = 0
temAveIss = 0
humStdIss = 0
humStdIss = 0
with open('dataHeatMiser.csv', 'w') as csvfile:
    datawriter = csv.writer(csvfile)
    # spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    # spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
    datawriter.writerow(["Number of Run"," Trial Count", "Initial Average Hum","Average hum after algorithm", " Initial Standard hum deviation", "Standard deviation hum after algorithm",  "Initial Average tem","Average tem after algorithm", " Initial Standard tem deviation", "Standard deviation tem after algorithm", "humAveIss ", "humStdIss","temAveIss","temStdIss"])

    for x in range(0,100):
        temps = np.random.uniform(low=minTem, high=maxTem, size=(12,))[np.newaxis]
        humidity = np.random.uniform(low=minHum, high=maxHum, size=(12,))[np.newaxis]
        rooms = np.stack((temps.T, humidity.T), axis=1)

        trialCount = 0
        office = 0
        prevRooms = rooms
        initialStdHum = stdRooms("Hum")
        initialAveragesHum = averageRooms("Hum")
        initialStdTem = stdRooms("Tem")
        initialAveragesTem = averageRooms("Tem")

        humAveIss = 0
        temAveIss = 0
        humStdIss = 0
        temStdIss = 0

        while (math.ceil(averageRooms("Tem")) != 73 or math.ceil(averageRooms("Hum")) != 48 or stdRooms(
                "Tem") > 1.5 or stdRooms("Hum") > 1.7):
            curTem = rooms[office][0][0]
            curHum = rooms[office][1][0]
            temPercent = math.fabs(73. - curTem) / math.fabs(maxTem - minTem + 4.)
            humPercent = math.fabs(48. - curHum) / math.fabs(maxHum - minHum + 4.)

            if trialCount > 100:
                runs = runs +1
                if math.ceil(averageRooms("Tem")) != 73:
                    temAveIss = 1
                if math.ceil(averageRooms("Hum")) != 48:
                    humAveIss = 1
                if stdRooms("Tem") > 1.5:
                    temStdIss = 1
                if stdRooms("Hum") > 1.7:
                    humStdIss = 1

                break
            #     if math.ceil(averageRooms("Tem")) != 73 and math.ceil(averageRooms("Hum")) != 48:
            #     '''
            #     there are issues with convergence with the initial algorithm.
            #     This is why I need another version.
            #     '''

            '''This is the base algorithm'''
            baseAlgorithm(curTem, curHum, temPercent, humPercent, office)
            # if curHum > 48. and curTem > 73.:
            #     if temPercent > humPercent:
            #         lowTemp(office)
            #     else:
            #         lowHum(office)
            # elif curHum < 47. and curTem < 73.:
            #     if temPercent > humPercent:
            #         raiseTemp(office)
            #     else:
            #         raiseHum(office)
            #
            # elif curHum < 47. and curTem > 73.:
            #     #raiseHum(office)
            #     if temPercent > humPercent:
            #         lowTemp(office)
            #     else:
            #         raiseHum(office)
            #
            # elif curHum > 48. and curTem < 73.:
            #     ##raiseTemp(office)
            #     if temPercent > humPercent:
            #         raiseTemp(office)
            #     else:
            #         lowHum(office)
            office += 1
            if office == 11:
                trialCount += 1
                office = 0
        datawriter.writerow([x+1,trialCount,initialAveragesHum, averageRooms("Hum"), initialStdHum, stdRooms("Hum"),initialAveragesTem, averageRooms("Tem"), initialStdTem, stdRooms("Tem"),humAveIss,humStdIss,temAveIss,temStdIss])

    print(runs)
            # if math.ceil(averageRooms("Tem")) != 73 :
            #     print("fixing ave tem")
            #
            # if math.ceil(averageRooms("Hum")) != 48:
            #     print("fixing hum ave")
            # if stdRooms("Tem") > 1.5:
            #     print("need to fix std tem")
            # if stdRooms("Hum") > 1.7:
            #     print("need to fix std hum")

    # print(trialCount)
    # print("This is the final std", stdRooms())
    # print("This is the final ave", averageRooms())
    # print(" This is the final condition of the rooms")
    # print(rooms.T)
