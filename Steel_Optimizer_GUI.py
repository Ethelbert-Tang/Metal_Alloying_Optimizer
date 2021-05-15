# -*- coding: utf-8 -*-

# Run this app with `python Steel_Optimizer_GUI.py` and
# visit http://127.0.0.1:5000/ in your web browser.

import pandas as pd
from pulp import *
import PySimpleGUIWeb as sg


# Scrape/search website(s) to find pricing for different alloys
# Using "static" numbers found from prior for deployment testing

Al = 3010.42
Cu = 10592.50
HC_Cr = 1120.66
LC_Cr = 1765.42
SiCr = 1274.17
Ni = 598.71
Mg = 3375
Nb = 30702.91
Mo = 30050
Si =  3278
Ti = 8600
V = 35750
NV = 26941.80
Mn = 2555
LC_Mn = 1711.69
MC_Mn = 1350.93
HC_Mn = 1043.90
SiMn = 1345
Prices = [Al, Cu, HC_Cr, LC_Cr, SiCr, Ni, Mg, Nb, Mo, Si, Ti, V, NV, Mn, LC_Mn, MC_Mn, HC_Mn, SiMn]

df = pd.read_csv("Metal_Weight_Per_Ton.csv") # Values in kg

df["Price ($/t)"] = Prices

target = pd.read_csv('Metal_Grades.csv') # Set of preset/predetermined Steel grades

# convert weight % to weight/100 tons
target[["C", "Al", "Cu", "Cr", "Ni", "Mg", "Nb", "Mn", "Mo", "Si", "Ti", "V", "N", "P", "S", "Fe"]] = (target[["C", "Al", "Cu", "Cr", "Ni", "Mg", "Nb", "Mn", "Mo", "Si", "Ti", "V", "N", "P", "S", "Fe"]]/100)*100000

layout = [
    [sg.Text('Please input your steel grade (xxxx)')],
    [sg.Text('Grade:', size=(15,1)), sg.InputText()],
    [sg.Output(size=(50,20), key='-OUTPUT-')],
    [sg.Button('Calculate'), sg.Button('Exit')]
]

window = sg.Window('Steel Optimizer Input', layout, web_port=5000, web_start_browser=False) # open browser and visit http://127.0.0.1:5000/ to access

while True:
    event, values = window.read()

    prob = LpProblem("Steel_Optimizer",LpMinimize)

    grade = int(values[0])  # Input value to call on specific grades from database
    
    print("Grade:",grade)
    
    Metal = list(df['Metal'])
    Price = dict(zip(Metal, df['Price ($/t)']))
    C = dict(zip(Metal, df['C']))
    Al = dict(zip(Metal, df['Al']))
    Cu = dict(zip(Metal, df['Cu']))
    Cr = dict(zip(Metal, df['Cr']))
    Ni = dict(zip(Metal, df['Ni']))
    Mg = dict(zip(Metal, df['Mg']))
    Nb = dict(zip(Metal, df['Nb']))
    Mn = dict(zip(Metal, df['Mn']))
    Mo = dict(zip(Metal, df['Mo']))
    Si = dict(zip(Metal, df['Si']))
    Ti = dict(zip(Metal, df['Ti']))
    V = dict(zip(Metal, df['V']))
    N = dict(zip(Metal, df['N']))
    P = dict(zip(Metal, df['P']))
    S = dict(zip(Metal, df['S']))

    Metal_Vars = LpVariable.dicts("Metal",Metal,lowBound=0,cat='Continuous')

    # Minimize price
    prob += lpSum([Price[i]*Metal_Vars[i] for i in Metal])

    # Optimize elements based on present grade limits
    prob += lpSum([C[f] * Metal_Vars[f] for f in Metal]) >= target.loc[target.Grade == grade].reset_index()['C'][0]
    prob += lpSum([C[f] * Metal_Vars[f] for f in Metal]) <= target.loc[target.Grade == grade].reset_index()['C'][1]

    prob += lpSum([Al[f] * Metal_Vars[f] for f in Metal]) >= target.loc[target.Grade == grade].reset_index()['Al'][0]
    prob += lpSum([Al[f] * Metal_Vars[f] for f in Metal]) <= target.loc[target.Grade == grade].reset_index()['Al'][1]

    prob += lpSum([Cu[f] * Metal_Vars[f] for f in Metal]) >= target.loc[target.Grade == grade].reset_index()['Cu'][0]
    prob += lpSum([Cu[f] * Metal_Vars[f] for f in Metal]) <= target.loc[target.Grade == grade].reset_index()['Cu'][1]

    prob += lpSum([Cr[f] * Metal_Vars[f] for f in Metal]) >= target.loc[target.Grade == grade].reset_index()['Cr'][0]
    prob += lpSum([Cr[f] * Metal_Vars[f] for f in Metal]) <= target.loc[target.Grade == grade].reset_index()['Cr'][1]

    prob += lpSum([Ni[f] * Metal_Vars[f] for f in Metal]) >= target.loc[target.Grade == grade].reset_index()['Ni'][0]
    prob += lpSum([Ni[f] * Metal_Vars[f] for f in Metal]) <= target.loc[target.Grade == grade].reset_index()['Ni'][1]

    prob += lpSum([Mg[f] * Metal_Vars[f] for f in Metal]) >= target.loc[target.Grade == grade].reset_index()['Mg'][0]
    prob += lpSum([Mg[f] * Metal_Vars[f] for f in Metal]) <= target.loc[target.Grade == grade].reset_index()['Mg'][1]

    prob += lpSum([Nb[f] * Metal_Vars[f] for f in Metal]) >= target.loc[target.Grade == grade].reset_index()['Nb'][0]
    prob += lpSum([Nb[f] * Metal_Vars[f] for f in Metal]) <= target.loc[target.Grade == grade].reset_index()['Nb'][1]

    prob += lpSum([Mn[f] * Metal_Vars[f] for f in Metal]) >= target.loc[target.Grade == grade].reset_index()['Mn'][0]
    prob += lpSum([Mn[f] * Metal_Vars[f] for f in Metal]) <= target.loc[target.Grade == grade].reset_index()['Mn'][1]

    prob += lpSum([Mo[f] * Metal_Vars[f] for f in Metal]) >= target.loc[target.Grade == grade].reset_index()['Mo'][0]
    prob += lpSum([Mo[f] * Metal_Vars[f] for f in Metal]) <= target.loc[target.Grade == grade].reset_index()['Mo'][1]

    prob += lpSum([Si[f] * Metal_Vars[f] for f in Metal]) >= target.loc[target.Grade == grade].reset_index()['Si'][0]
    prob += lpSum([Si[f] * Metal_Vars[f] for f in Metal]) <= target.loc[target.Grade == grade].reset_index()['Si'][1]

    prob += lpSum([Ti[f] * Metal_Vars[f] for f in Metal]) >= target.loc[target.Grade == grade].reset_index()['Ti'][0]
    prob += lpSum([Ti[f] * Metal_Vars[f] for f in Metal]) <= target.loc[target.Grade == grade].reset_index()['Ti'][1]

    prob += lpSum([V[f] * Metal_Vars[f] for f in Metal]) >= target.loc[target.Grade == grade].reset_index()['V'][0]
    prob += lpSum([V[f] * Metal_Vars[f] for f in Metal]) <= target.loc[target.Grade == grade].reset_index()['V'][1]

    prob += lpSum([N[f] * Metal_Vars[f] for f in Metal]) >= target.loc[target.Grade == grade].reset_index()['N'][0]
    prob += lpSum([N[f] * Metal_Vars[f] for f in Metal]) <= target.loc[target.Grade == grade].reset_index()['N'][1]

    prob += lpSum([P[f] * Metal_Vars[f] for f in Metal]) >= target.loc[target.Grade == grade].reset_index()['P'][0]
    prob += lpSum([P[f] * Metal_Vars[f] for f in Metal]) <= target.loc[target.Grade == grade].reset_index()['P'][1]

    prob += lpSum([S[f] * Metal_Vars[f] for f in Metal]) >= target.loc[target.Grade == grade].reset_index()['S'][0]
    prob += lpSum([S[f] * Metal_Vars[f] for f in Metal]) <= target.loc[target.Grade == grade].reset_index()['S'][1]

    prob.solve()

    print("Status:", LpStatus[prob.status], "\n")

    print("Additions to use:")

    for v in prob.variables():
        print(v.name, "=", round(v.varValue, 2), "metric tons")
        
    print("\nTotal Cost of Alloying(USD) = $",format(value(prob.objective), ',.2f'))
    print("\n\n\n\n")

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
window.close() # Also automatically exits server