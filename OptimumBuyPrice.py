import matplotlib.pyplot as plt
import numpy as np
# Variables
households = 202 # No of households
solar = 0.31 # % of solar
avesolargen = 25 # Average solar generation (kWh)
aveelecuse = 9 # Average electricity usage between 9-3pm (kWh)
bateff = 0.9 # Battery round-trip efficiency
retail = 0.29 # Retail cost of electricity ($)
buygrid = 0.00 # buy price from battery
sellgrid = 0.07 # sell price to battery
degredation = 0.02 # per year
lifetime = 10 # yearly
batterycost = 200 # $ per kWh
efficiency = 0.9

# Functions
def HouseholdsWithSolar(): # Determines households with solar
    return households * solar

def TotalExcessPower(): # Determines maximum power
    return (avesolargen-aveelecuse) * HouseholdsWithSolar()

def ActualExcessPower(): # Determines actual power
    return round(TotalExcessPower() * bateff)

def OptimumBatterySize(): # Determines the optimum battery size
    return int(round(ActualExcessPower(), -3) / 1000)

def BatteryCost(): # Determines the battery cost
    return OptimumBatterySize() * 1000 * batterycost

def CheckDegredationCapacity(a, iteration):
    if (OptimumBatterySize() * 1000 * (1 - iteration * degredation)) > a:
        return a
    else: 
        return OptimumBatterySize() * 1000 * (1 - iteration * degredation)
def TotalCouncilSavings():

    totalcouncil = 0
    ctotalsaving = 0
    totalcouncilsaving = []
    for i in range(0,lifetime):
            ctotalsaving = (buygrid-sellgrid)*CheckDegredationCapacity(ActualExcessPower(), i)*365
            totalcouncil = totalcouncil + ctotalsaving
            totalcouncilsaving.append(totalcouncil)
    return totalcouncilsaving


def OptimumBuyBack(): 
    x = []
    y = []
    global buygrid    
    while True:
        x.append(buygrid)        
        y.append(TotalCouncilSavings()[-1])
        if TotalCouncilSavings()[-1] > BatteryCost():
            break
        else:
            buygrid += 0.005
    print(f"Optimum Buy Price: {round(buygrid, 3)}, Total Council Savings: {round(TotalCouncilSavings()[-1], 3)}, Battery Cost: {BatteryCost()}")

def OptimumBuyBackGraph(): 
    x = []
    y = []
    global buygrid    
    while True:
        x.append(buygrid)        
        y.append(TotalCouncilSavings()[-1])
        if TotalCouncilSavings()[-1] > BatteryCost():
            break
        else:
            buygrid += 0.005
    plt.xlabel("Sell Price ($)")
    plt.ylabel("Council Gain over Lifetime ($)")
    plt.plot(x, y, label = "Savings")
    plt.plot(x, np.full(len(x), BatteryCost()), label = "Battery Cost")
    plt.title("Buy Price vs Savings")
    plt.legend(loc = "lower right", fontsize = "10")
    plt.show()

def OptimumBuyBackGraphSave(): 
    x = []
    y = []
    global buygrid    
    while True:
        x.append(buygrid)        
        y.append(TotalCouncilSavings()[-1])
        if TotalCouncilSavings()[-1] > BatteryCost():
            break
        else:
            buygrid += 0.005
    plt.xlabel("Sell Price ($)")
    plt.ylabel("Council Gain over Lifetime ($)")
    plt.plot(x, y, label = "Savings")
    plt.plot(x, np.full(len(x), BatteryCost()), label = "Battery Cost")
    plt.title("Buy Price vs Savings")
    plt.legend(loc = "lower right", fontsize = "10")
    plt.savefig("OptimumBuyBack.png")
    


#OptimumBuyBack()
OptimumBuyBackGraph()
#OptimumBuyBackGraphSave()