# -*- coding: utf-8 -*-

# Run this app with `python Steel_Optimizer_GUI.py` and
# visit http://127.0.0.1:5000/ in your web browser.

import pandas as pd
from pulp import *
import PySimpleGUIWeb as sg


# Using "static" data here for testing deployment
data = {'Metal':['Al', 'Cu', 'HC_Cr', 'LC_Cr', 'SiCr', 'Ni', 'Mg', 'Nb', 'Mo', 'Si', 'Ti','V', 'NV', 'Mn', 'LC_Mn', 'MC_Mn', 'HC_Mn', 'SiMn'],
         'C':[0.0, 0.0, 80.0, 1.0, 10.0, 0.6, 0.0, 1.4, 1.0, 0.5, 1.5, 1.0, 60.0, 0.0, 7.0, 15.0, 80.0, 25.0],
         'Al':[997.0, 0.0, 0.0, 0.0, 10.0, 0.0, 0.0, 3.3, 0.0, 5.0, 50.0, 20.0, 1.5, 0.0, 0.0, 0.0, 0.0, 0.0],
         'Cu':[0, 990, 0, 0, 0, 2, 0, 0, 5, 0, 0, 1, 0, 0, 0, 0, 0, 0], 
         'Cr':[0.0, 0.0, 520.0, 550.0, 300.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
         'Ni':[0, 0, 0, 0, 0, 350, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
         'Mg':[0, 0, 0, 0, 0, 0, 999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
         'Nb':[0, 0, 0, 0, 0, 0, 0, 660, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
         'Mn':[0.0, 0.0, 0.0, 0.0, 15.0, 0.0, 0.0, 3.2, 0.0, 0.0, 0.0, 4.0, 0.0, 997.0, 800.0, 780.0, 750.0, 650.0], 
         'Mo':[0, 0, 0, 0, 0, 0, 0, 0, 700, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
         'Si':[0.0, 0.0, 15.0, 15.0, 420.0, 6.0, 0.0, 28.3, 15.0, 760.0, 2.5, 8.0, 0.0, 0.0, 15.0, 15.0, 15.0, 170.0],
         'Ti':[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.7, 0.0, 0.0, 700.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
         'V':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 800, 790, 0, 0, 0, 0, 0], 
         'N':[0, 0, 30, 30, 0, 0, 0, 0, 0, 0, 5, 0, 140, 0, 0, 0, 0, 0], 
         'P':[0.0, 0.0, 0.3, 0.3, 0.5, 0.3, 0.0, 1.6, 0.5, 0.2, 0.0, 0.5, 0.0, 0.0, 3.5, 3.5, 3.5, 3.0], 
         'S':[0.0, 0.0, 0.3, 0.3, 0.3, 0.6, 0.0, 0.8, 1.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.5, 0.5, 0.5, 0.4], 
         'Fe':[3.0, 10.0, 354.5, 403.5, 244.2, 640.0, 1.0, 298.7, 277.5, 234.3, 241.0, 165.0, 8.5, 3.0, 174.0, 186.0, 151.0, 151.7], 
         'Price ($/t)':[3064.150339451199, 10638.558042282972, 1105.3047316657633, 1719.3629159245206, 1258.8192777304525, 598.7067296522885, 3175.0, 30702.90921293787, 28850.0, 3278.0, 8600.0, 35750.0, 26634.773742223602, 2555.0, 1711.687188621286, 1350.9280053692662, 1028.5474586334185, 1325.0]
    }
    
tar = {'Grade':[1000, 1000, 2000, 2000, 3000, 3000, 4000, 4000, 5000, 5000, 6000, 6000, 7000, 7000, 8000, 8000, 9000, 9000, 10000, 10000],
         'Min/Max':['Min', 'Max', 'Min', 'Max', 'Min', 'Max', 'Min', 'Max', 'Min', 'Max', 'Min', 'Max', 'Min', 'Max', 'Min', 'Max', 'Min', 'Max', 'Min', 'Max'],
         'C':[400.0, 460.0, 50.0, 230.0, 50.0, 170.0, 150.0, 230.0, 400.0, 500.0, 50.0, 180.0, 50.0, 170.0, 469.99999999999994, 550.0, 50.0, 80.0, 0.0, 29.999999999999996],
         'Al':[20.0, 40.0, 20.0, 40.0, 20.0, 40.0, 20.0, 40.0, 699.9999999999999, 1200.0, 20.0, 40.0, 20.0, 40.0, 20.0, 40.0, 20.0, 40.0, 20.0, 40.0],
         'Cu':[0.0, 300.0, 0.0, 300.0, 0.0, 300.0, 0.0, 200.0, 0.0, 300.0, 0.0, 349.99999999999994, 300.0, 500.0, 0.0, 300.0, 0.0, 300.0, 100.0, 600.0],
         'Cr':[349.99999999999994, 699.9999999999999, 0.0, 300.0, 1000.0, 1500.0, 0.0, 200.0, 1300.0000000000002, 1700.0000000000002, 0.0, 250.0, 400.0, 699.9999999999999, 800.0, 1100.0, 18000.0, 20000.0, 22000.0, 24000.0],
         'Ni':[0.0, 250.0, 0.0, 300.0, 0.0, 300.0, 400.0, 800.0, 250.0, 250.0, 0.0, 300.0, 0.0, 400.0, 0.0, 300.0, 8000.0, 11000.0, 3500.0000000000005, 5500.0],
         'Mg':[0.0, 1000.0, 0.0, 1000.0, 0.0, 1000.0, 0.0, 1000.0, 0.0, 1000.0, 0.0, 1000.0, 0.0, 1000.0, 0.0, 1000.0, 0.0, 1000.0, 0.0, 1000.0],
         'Nb':[0.0, 300.0, 0.0, 300.0, 0.0, 300.0, 0.0, 300.0, 0.0, 300.0, 14.999999999999998, 59.99999999999999, 5.0, 50.0, 0.0, 300.0, .0, 300.0, 0.0, 300.0],
         'Mn':[1350.0000000000002, 1650.0, 0.0, 1350.0000000000002, 400.0, 650.0000000000001, 1000.0, 1500.0, 0.0, 600.0, 900.0000000000001, 1600.0, 500.0, 1200.0, 600.0, 1000.0, 0.0, 2000.0, 0.0, 2000.0],
         'Mo':[0.0, 300.0, 0.0, 300.0, 450.00000000000006, 650.0000000000001, 450.00000000000006, 600.0, 150.0, 300.0, 0.0, 100.0, 0.0, 300.0, 0.0, 300.0, 0.0, 300.0, 100.0, 600.0],
         'Si':[150.0, 349.99999999999994, 150.0, 400.0, 500.0, 800.0, 0.0, 400.0, 150.0, 500.0, 0.0, 500.0, 250.0, 500.0, 100.0, 400.0, 0.0, 1000.0, 0.0, 1000.0],
         'Ti':[0.0, 300.0, 6.0, 40.0, 0.0, 300.0, 0.0, 300.0, 0.0, 300.0, 20.0, 200.0, 0.0, 300.0, 0.0, 300.0, 0.0, 300.0, 0.0, 300.0],
         'V':[0.0, 300.0, 0.0, 59.99999999999999, 0.0, 300.0, 0.0, 20.0, 0.0, 300.0, 20.0, 100.0, 0.0, 300.0, 100.0, 250.0, 0.0, 300.0, 0.0, 300.0],
         'N':[0.0, 10.0, 3.0, 14.999999999999998, 0.0, 10.0, 0.0, 12.0, 0.0, 10.0, 0.0, 10.0, 0.0, 10.0, 0.0, 10.0, 0.0, 10.0, 50.0, 200.0],
         'P':[0.0, 29.999999999999996, 0.0, 40.0, 0.0, 14.999999999999998, 0.0, 20.0, 0.0, 29.999999999999996, 0.0, 29.999999999999996, 0.0, 40.0, 0.0, 35.00000000000001, 0.0, 45.0, 0.0, 35.00000000000001],
         'S':[0.0, 29.999999999999996, 0.0, 50.0, 0.0, 5.0, 0.0, 10.0, 0.0, 29.999999999999996, 0.0, 29.999999999999996, 0.0, 50.0, 0.0, 35.00000000000001, 0.0, 29.999999999999996, 0.0, 14.999999999999998],
         'Fe':[0.0, 100000.0, 0.0, 100000.0, 0.0, 100000.0, 0.0, 100000.0, 0.0, 100000.0, 0.0, 100000.0, 0.0, 100000.0, 0.0, 100000.0, 0.0, 100000.0, 0.0, 100000.0]
    }
    
df = pd.DataFrame(data)

target = pd.DataFrame(tar)

layout = [
    [sg.Text('Please input your steel grade (xxxx)')],
    [sg.Text('Grade:', size=(15,1)), sg.InputText()],
    [sg.Output(size=(50,20), key='-OUTPUT-')],
    [sg.Button('Calculate'), sg.Button('Clear'), sg.Button('Exit')]
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
    print("\n")

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Clear':
        window['-OUTPUT-'].update('')
window.close()
