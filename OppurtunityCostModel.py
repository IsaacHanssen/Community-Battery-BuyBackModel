import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Variables
households = 202 # No of households
solar = 0.31 # % of solar
avesolargen = 25 # Average solar generation (kWh)
aveelecuse = 9 # Average electricity usage between 9-3pm (kWh)
bateff = 0.9 # Battery round-trip efficiency
retail = 0.29 # Retail cost of electricity ($)
buygrid = 0.20 # buy price from battery
sellgrid = 0.13 # sell price to battery
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
    return int(round(ActualExcessPower(), -3) / 1000) # Can comment the auto battery and replace with your own value in MW

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


    return lifetimelist, degradation, savinglistday, savinglistyear, accumalatedsaving, councilsaving, totalcouncilsaving, oppurtunitycost

def Graph():
    lifetimelist, degradation, savinglistday, savinglistyear, accumalatedsaving, councilsaving, totalcouncilsaving, oppurtunitycost = BuybackSaving()    
    totsaving = []
    for i in range(0, len(totalcouncilsaving)):
        totsaving.append(councilsaving[i] + savinglistyear[i])

    plt.plot(lifetimelist, councilsaving, label = "Council Savings")
    plt.plot(lifetimelist, savinglistyear, label = "Community Savings")
    plt.plot(lifetimelist, oppurtunitycost, label = "Oppurtunity Costs")
    plt.plot(lifetimelist, totsaving, label = "Total Savings")
    plt.title("Oppurtunity Costs of Battery")
    plt.xlabel("Years")
    plt.ylabel("Cost ($)")
    plt.legend(loc = "upper left", fontsize = "5")
    plt.show()

def GraphSave():
    lifetimelist, degradation, savinglistday, savinglistyear, accumalatedsaving, councilsaving, totalcouncilsaving, oppurtunitycost = BuybackSaving()    
    totsaving = []
    for i in range(0, len(totalcouncilsaving)):
        totsaving.append(councilsaving[i] + savinglistyear[i])

    plt.plot(lifetimelist, councilsaving, label = "Council Savings")
    plt.plot(lifetimelist, savinglistyear, label = "Community Savings")
    plt.plot(lifetimelist, oppurtunitycost, label = "Oppurtunity Costs")
    plt.plot(lifetimelist, totsaving, label = "Total Savings")
    plt.title("Oppurtunity Costs of Battery")
    plt.xlabel("Years")
    plt.ylabel("Cost ($)")
    plt.legend(loc = "upper left", fontsize = "5")
    plt.savefig("Optimum Oppurtunity Cost.png")

Graph()
#GraphSave()