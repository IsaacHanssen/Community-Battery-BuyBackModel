import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Variables
households = 200 # No of households
solar = 0.31 # % of solar
avesolargen = 25 # Average solar generation (kWh)
aveelecuse = 9 # Average electricity usage between 9-3pm (kWh)
bateff = 0.9 # Battery round-trip efficiency
retail = 0.29 # Retail cost of electricity ($)
buygrid = 0.27 # buy price from battery
sellgrid = 0.07 # sell price to battery
degredation = 0.02 # per year
lifetime = 10 # yearly
batterycost = 200 # $ per kWh
emmissions = 0.6564 # kg
retailsellgrid = 0

# Functions
def HouseholdsWithSolar(): # Determines households with solar
    return households * solar

def TotalExcessPower(): # Determines maximum power
    return (avesolargen-aveelecuse) * HouseholdsWithSolar()

def ActualExcessPower(): # Determines actual power
    return round(TotalExcessPower() * bateff)

def OptimumBatterySize(): # Determines the optimum battery size
    return 1#int(round(ActualExcessPower(), -3) / 1000) # If you want a set battery size just hash the return and just return your size in MW

def BatteryCost(): # Determines the battery cost
    return 1600000

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
    em = 0
    s=0
    totalemissions = []
    accumemissions = []
    sellerprofit = []

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
        em = em + CheckDegredationCapacity(ActualExcessPower(), i) * emmissions * 365
        totalemissions.append(CheckDegredationCapacity(ActualExcessPower(), i) * emmissions * 365)
        accumemissions.append(em)
        s = s + (sellgrid-retailsellgrid) * CheckDegredationCapacity(ActualExcessPower(), i)*365
        sellerprofit.append(s)
    return lifetimelist, degradation, savinglistday, savinglistyear, accumalatedsaving, councilsaving, totalcouncilsaving, totalemissions, accumemissions, sellerprofit

def PrintBuyBack(): # Prints the data in a DataFrame Structure
    lifetimelist, degradation, savinglistday, savinglistyear, accumalatedsaving, councilsaving, totalcouncilsaving, totalemissions, accumemissions, sellerprofit = BuybackSaving()
    df = pd.DataFrame({
    'Year':lifetimelist,
    'Degradation':degradation,
    'Com Savings Yearly ($)':savinglistyear,
    'Accum Com Saving ($)':accumalatedsaving,
    'Accum Seller Profit ($)':sellerprofit,
    'Council Saving ($)':councilsaving,
    'Accum Council Savings ($)':totalcouncilsaving,
    'Accumalated Emissions (kg)':accumemissions
    })
    return print(df)

def GraphSavings(): 
    lifetimelist, degradation, savinglistday, savinglistyear, accumalatedsaving, councilsaving, totalcouncilsaving, totalemissions, accumemissions, sellerprofit = BuybackSaving()
    plt.plot(num=None, figsize=(16, 20), dpi=80, facecolor='w', edgecolor='k')
    plt.plot(lifetimelist, totalcouncilsaving, label="Private Company Revenue ($)")
    plt.plot(lifetimelist, accumalatedsaving, label="Buyers Benefits ($)")
    plt.plot(lifetimelist, np.full(lifetimelist[-1], BatteryCost()), label = 'Battery Cost ($)')
    plt.plot(lifetimelist, sellerprofit, label = 'Sellers Benefits ($)')
    plt.xlabel("Lifetime of Battery (Years)", fontsize = '8')
    plt.ylabel("Savings ($)", fontsize = '8')
    plt.legend(loc='upper left', fontsize = '8')
    plt.title("Accumalated Savings Yearly")
    plt.show()

def GraphSavingsSave(): 
    lifetimelist, degradation, savinglistday, savinglistyear, accumalatedsaving, councilsaving, totalcouncilsaving, totalemissions, accumemissions, sellerprofit = BuybackSaving()
    plt.plot(lifetimelist, totalcouncilsaving, label="Total Council Savings (Accum Yearly)")
    plt.plot(lifetimelist, accumalatedsaving, label="Total Community Savings (Yearly)")
    plt.plot(lifetimelist, np.full(lifetimelist[-1], BatteryCost()), label = 'Battery Cost ($)')
    plt.xlabel("Lifetime of Battery (Years)")
    plt.ylabel("Savings ($)")
    plt.legend(loc='upper left', fontsize = '8')
    plt.title("Accumalated Savings Yearly")
    plt.savefig("graph.png")

def GraphEnvironment():
    lifetimelist, degradation, savinglistday, savinglistyear, accumalatedsaving, councilsaving, totalcouncilsaving, totalemissions, accumemissions, sellerprofit = BuybackSaving()
    plt.plot(lifetimelist, totalemissions, label="Total Emissions ( Yearly)")
    plt.plot(lifetimelist, accumemissions, label="Total Accum Emissions (Yearly)")
    plt.xlabel("Lifetime of Battery (Years)")
    plt.ylabel("CO2 Emissions Saved (kg)")
    plt.legend(loc='upper left', fontsize = '8')
    plt.title("Accumalated Emissions Saved Yearly")
    plt.show()

def GraphEnvironmentSave():
    lifetimelist, degradation, savinglistday, savinglistyear, accumalatedsaving, councilsaving, totalcouncilsaving, totalemissions, accumemissions, sellerprofit = BuybackSaving()
    plt.plot(lifetimelist, totalemissions, label="Total Emissions ( Yearly)")
    plt.plot(lifetimelist, accumemissions, label="Total Accum Emissions (Yearly)")
    plt.xlabel("Lifetime of Battery (Years)")
    plt.ylabel("CO2 Emissions Saved (kg)")
    plt.legend(loc='upper left', fontsize = '8')
    plt.title("Accumalated Emissions Saved Yearly")
    plt.savefig("graphenvironment.png")

def Analyse(): # Analyses the results, prints the data, and prints statements about the battery
    lifetimelist, degradation, savinglistday, savinglistyear, accumalatedsaving, councilsaving, totalcouncilsaving, totalemissions, accumemissions, sellerprofit = BuybackSaving()
    PrintBuyBack()
    def PayBack():
        for i in range(0, len(accumalatedsaving)):
            if totalcouncilsaving[i] > BatteryCost():
                return f", this will be paid back in {i + 1} years"
        return f", this will not be paid back."
    
    print(f"The optimum battery size will be {OptimumBatterySize()} MWh as a maximum of {ActualExcessPower()} kWh will be generated for the {households} households.")
    print(f"This is based on the fact {solar} of households have solar and the average power put into the grid per household per day is {avesolargen - aveelecuse} kWh.")
    print(f"This will cost approximately ${BatteryCost()}{PayBack()} with an average buy price of ${buygrid} off the battery, and a sell price of ${sellgrid}.")
    print(f"The remaining ${round(buygrid-sellgrid, 3)} will be for the council for ongoing maintenance.")
    print()
    print(f"A total of ${round(accumalatedsaving[-1])} will be saved across the lifetime of {lifetime} years of the battery and into the community.")

def DataFrametoCSV():
    lifetimelist, degradation, savinglistday, savinglistyear, accumalatedsaving, councilsaving, totalcouncilsaving, totalemissions, accumemissions, sellerprofit = BuybackSaving()
    df = pd.DataFrame({
    'Year':lifetimelist,
    'Degradation':degradation,
    'Com Savings Daily ($)':savinglistday,
    'Com Savings Yearly ($)':savinglistyear,
    'Accum Com Saving ($)':accumalatedsaving,
    'Council Saving ($)':councilsaving,
    'Accum Council Savings ($)':totalcouncilsaving,
    'Total Emissions Yearly (kg)':totalemissions,
    'Accumalated Emissions (kg)':accumemissions,
    'Sellers Profit Accumalated ($)':sellerprofit
    })
    df.to_csv("DataFrame.csv")

PrintBuyBack()
#Analyse()
#GraphSavings()
#GraphSavingsSave()
GraphEnvironment()
#GraphEnvironmentSave()
#DataFrametoCSV()