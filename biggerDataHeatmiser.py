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
        if temPercent > humPercent:
            lowTemp(office)
        else:
            raiseHum(office)

    elif curHum > 48. and curTem < 73.:
        if temPercent > humPercent:
            raiseTemp(office)
        else:
            lowHum(office)


def basicSolution(curTem, curHum, office):
    if math.fabs(curTem - 73) > math.fabs(curHum - 48):
        if curTem > 73.:
            lowTemp(office)
        else:
            raiseTemp(office)
    else:
        if curHum > 48.:
            lowHum(office)
        else:
            raiseHum(office)

'''
Simmulation

'''
trialCount = 0
office = 0

'''
In this solution HeatMiser will change the temperature or humidity of each room it visits, so long it is not in the desired range.
The distance is evaluated in each room. Which one is farther from the ideal average?
For that the following formula is used:
abs(idealAverage - current office value)/abs(maximum value and minimum value)

'''
runs = 0

with open('dataHeatNew1.csv', 'w') as csvfile:
    datawriter = csv.writer(csvfile)

    datawriter.writerow(["Number of Run"," Trial Count", "Initial Average Hum","Average hum after algorithm", " Initial Standard hum deviation", "Standard deviation hum after algorithm",  "Initial Average tem","Average tem after algorithm", " Initial Standard tem deviation", "Standard deviation tem after algorithm", "humAveIss ", "humStdIss","temAveIss","temStdIss"])
    for y in range(0,5):
        runs = 0
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

            while (
                math.ceil(averageRooms("Tem")) != 73 or math.ceil(averageRooms("Hum")) != 48 or stdRooms(
                    "Tem") > 1.5 or stdRooms("Hum") > 1.7):
                curTem = rooms[office][0][0]
                curHum = rooms[office][1][0]
                temPercent = math.fabs(73. - curTem) / math.fabs(maxTem - minTem + 4.)
                humPercent = math.fabs(48. - curHum) / math.fabs(maxHum - minHum + 4.)
                if trialCount ==  100:
                    runs = runs +1
                    break

                '''This is the base algorithm'''

                if trialCount < 20:
                    baseAlgorithm(curTem, curHum, temPercent, humPercent, office)
                else:

                    if math.ceil(averageRooms("Tem")) == 73 and math.ceil(averageRooms("Hum")) == 48 and stdRooms("Tem") > 1.5 and stdRooms("Hum") < 1.7:
                        if math.fabs(curTem - 73) > .5: #desired stdtemp =1.5
                            if curTem >73:
                                lowTemp(office)
                                if(math.ceil(averageRooms("Tem")) != 73):
                                    raiseTemp(office)
                            elif curTem < 73:
                                raiseTemp(office)
                                if (math.ceil(averageRooms("Tem")) != 73):
                                    lowTemp(office)
                    elif math.ceil(averageRooms("Tem")) == 73 or math.ceil(averageRooms("Hum")) == 48 or stdRooms("Tem") < 1.5 or stdRooms("Hum") > 1.7:
                        if math.fabs(curHum - 48) > .5:
                            if curHum > 48:
                                lowHum(office)
                                if (math.ceil(averageRooms("Hum")) != 48):
                                    raiseHum(office)
                            elif curHum < 48:
                                raiseHum(office)
                                if (math.ceil(averageRooms("Hum")) != 48):
                                    lowHum(office)
                    elif math.ceil(averageRooms("Tem")) != 73 or math.ceil(averageRooms("Hum")) == 48 or stdRooms("Tem") < 1.5 or stdRooms("Hum") < 1.7:
                        if math.fabs(curTem - 73) < 1.5:
                            if curTem > 73:
                                lowTemp(office)
                                if (stdRooms("Tem") > 1.5):
                                    raiseTemp(office)
                            elif curTem < 73:
                                raiseTemp(office)
                                if (stdRooms("Tem") > 1.5):
                                    lowTemp(office)
                    elif math.ceil(averageRooms("Tem")) == 73 or math.ceil(averageRooms("Hum")) != 48 or stdRooms("Tem") < 1.5 or stdRooms("Hum") < 1.7:
                        if math.fabs(curHum - 48) < 1.7:
                            if curHum > 48:
                                lowHum(office)
                                if ( stdRooms("Hum") > 1.7):
                                    raiseHum(office)
                            elif curHum < 48:
                                raiseHum(office)
                                if ( stdRooms("Hum") > 1.7):
                                    lowHum(office)
                    else:
                        basicSolution(curTem, curHum, office)



                office += 1
                if office == 11:
                    trialCount += 1
                    office = 0
            if x+1 == 100:
                datawriter.writerow( [x + 1, trialCount, initialAveragesHum, averageRooms("Hum"), initialStdHum, stdRooms("Hum"),initialAveragesTem, averageRooms("Tem"), initialStdTem, stdRooms("Tem"), humAveIss, humStdIss,temAveIss, temStdIss,y,runs])
            else:
                datawriter.writerow([x+1,trialCount,initialAveragesHum, averageRooms("Hum"), initialStdHum, stdRooms("Hum"),initialAveragesTem, averageRooms("Tem"), initialStdTem, stdRooms("Tem"),humAveIss,humStdIss,temAveIss,temStdIss])



