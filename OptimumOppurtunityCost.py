import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Variables
households = 0 # No of households
solar = 0.31 # % of solar
avesolargen = 25 # Average solar generation (kWh)
aveelecuse = 9 # Average electricity usage between 9-3pm (kWh)
bateff = 0.9 # Battery round-trip efficiency
retail = 0.29 # Retail cost of electricity ($)
buygrid = 0.135 # buy price from battery
sellgrid = 0.07 # sell price to battery
degredation = 0.02 # per year
lifetime = 10 # yearly
batterycost = 200 # $ per kWh
emmissions = 0.6564 # kg


# Functions
def HouseholdsWithSolar(): # Determines households with solar
    return households * solar

def TotalExcessPower(): # Determines maximum power
    return (avesolargen-aveelecuse) * HouseholdsWithSolar()

def ActualExcessPower(): # Determines actual power
    return round(TotalExcessPower() * bateff)

def OptimumBatterySize(): # Determines the optimum battery size
    return 1

def BatteryCost(): # Determines the battery cost
    return OptimumBatterySize() * 1000 * batterycost

def CheckDegredationCapacity(a, iteration):
    if (OptimumBatterySize() * 1000 * (1 - iteration * degredation)) > a:
        return a
    else: 
        return OptimumBatterySize() * 1000 * (1 - iteration * degredation)

def BuybackSaving(): # Creates lists of separate data
    savinglistyear = []
    savinglistday = []
    lifetimelist = []
    accumalatedsaving = []
    degradation = []
    councilsaving = []
    totalsaving = 0
    totalcouncil = 0
    ctotalsaving = 0
    oppurtunitycost = []

    totalcouncilsaving = []
    for i in range(0,lifetime):
        lifetimelist.append(i + 1)
        degradation.append((1 - i * degredation))
        savinglistday.append(round((retail - buygrid) * CheckDegredationCapacity(ActualExcessPower(), i), 5))
        savingyear = (retail - buygrid) * CheckDegredationCapacity(ActualExcessPower(), i) * 365
        savinglistyear.append(round(savingyear, 5))
        totalsaving = totalsaving + savingyear
        accumalatedsaving.append(totalsaving)
        ctotalsaving = (buygrid-sellgrid)*CheckDegredationCapacity(ActualExcessPower(), i)*365
        councilsaving.append(ctotalsaving)
        totalcouncil = totalcouncil + ctotalsaving
        totalcouncilsaving.append(totalcouncil)
        oppurtunitycost.append((retail-sellgrid) * (ActualExcessPower()-CheckDegredationCapacity(ActualExcessPower(), i))* 365)
        totsaving = []
        for i in range(0, len(totalcouncilsaving)):
            totsaving.append(councilsaving[i] + savinglistyear[i])    



    return lifetimelist, degradation, savinglistday, savinglistyear, accumalatedsaving, councilsaving, totalcouncilsaving, oppurtunitycost, totsaving

def Optimum(): # iterated through households until oppurtunity cost is reached when degredation starts to max out the capacity
   
    global households
    while True:
        lifetimelist, degradation, savinglistday, savinglistyear, accumalatedsaving, councilsaving, totalcouncilsaving, oppurtunitycost, totsaving = BuybackSaving() 
        count = 0; x = 0        
        for i in range(0, len(totsaving)):
            if oppurtunitycost[i] > 0:
                count += 1
                x += oppurtunitycost[i]
        if count > lifetime/2: # Change this value to however many years you want to maintain the towns maximum electricity usage
            break
        households += 1
    print(f"Ideal amount of: {households}.")
    print(f"Oppurtunity cost lost: {x}.")

def Graph():
    Optimum()
    lifetimelist, degradation, savinglistday, savinglistyear, accumalatedsaving, councilsaving, totalcouncilsaving, oppurtunitycost, totsaving = BuybackSaving()    
    totsaving = []
    for i in range(0, len(totalcouncilsaving)):
        totsaving.append(councilsaving[i] + savinglistyear[i])

    plt.plot(lifetimelist, councilsaving, lifetimelist, savinglistyear, lifetimelist, oppurtunitycost, lifetimelist, totsaving)
    plt.show()

def GraphSave():
    Optimum()
    lifetimelist, degradation, savinglistday, savinglistyear, accumalatedsaving, councilsaving, totalcouncilsaving, oppurtunitycost, totsaving = BuybackSaving()    
    totsaving = []
    for i in range(0, len(totalcouncilsaving)):
        totsaving.append(councilsaving[i] + savinglistyear[i])

    plt.plot(lifetimelist, councilsaving, lifetimelist, savinglistyear, lifetimelist, oppurtunitycost, lifetimelist, totsaving)
    plt.savefig("Optimum Oppurtunity Cost.png")

Optimum()
Graph()
#GraphSave()
