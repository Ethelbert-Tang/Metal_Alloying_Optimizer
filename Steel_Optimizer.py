import requests
from bs4 import BeautifulSoup
import pandas as pd
from currency_converter import CurrencyConverter
from pulp import *

from flask import Flask
app = Flask(__name__)

APP_NAME = 'steel_optimizer'
app = Flask(APP_NAME)
HTTP_ERROR_CLIENT = 400
HTTP_ERROR_SERVER = 500
EXPECTED_KEYS = ['grade']

def validate_json(j):
    """
    Validate that the input has the expected format
    """
    try:
        # Make input into a python dict
        if not isinstance(j, dict):
            d = json.loads(j)
        else:
            d = j
    except Exception as e:
        raise ValueError(e)
    for ek in EXPECTED_KEYS:
        if ek not in d:
            raise ValueError(
                f"Expected key {ek} not in JSON\n{j}"
            )
    return d

def optimize(j):
    c = CurrencyConverter()

    Al = (c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/AluminumPrice/Aluminum.html').content, 'html.parser'
        ).find(id="pricel12").get_text()), 'CNY', 'USD') + c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/AluminumPrice/Aluminum.html').content, 'html.parser'
        ).find(id="priceh12").get_text()), 'CNY', 'USD'))/2

    Cu = (c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/CopperPrice/Copper.html').content, 'html.parser'
        ).find(id="pricel5").get_text()), 'CNY', 'USD') + c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/CopperPrice/Copper.html').content, 'html.parser'
        ).find(id="priceh5").get_text()), 'CNY', 'USD'))/2

    HC_Cr = (c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/ChromiumPrice/Chromium.html').content, 'html.parser'
        ).find(id="pricel0").get_text()), 'CNY', 'USD') + c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/ChromiumPrice/Chromium.html').content, 'html.parser'
        ).find(id="priceh0").get_text()), 'CNY', 'USD'))/2

    LC_Cr = (c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/ChromiumPrice/Chromium.html').content, 'html.parser'
        ).find(id="pricel2").get_text()), 'CNY', 'USD') + c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/ChromiumPrice/Chromium.html').content, 'html.parser'
        ).find(id="priceh2").get_text()), 'CNY', 'USD'))/2

    SiCr = (c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/ChromiumPrice/Chromium.html').content, 'html.parser'
        ).find(id="pricel20").get_text()), 'CNY', 'USD') + c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/ChromiumPrice/Chromium.html').content, 'html.parser'
        ).find(id="priceh20").get_text()), 'CNY', 'USD'))/2

    Ni = (c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/NickelPrice/Nickel.html').content, 'html.parser'
        ).find(id="pricel0").get_text()), 'CNY', 'USD') + c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/NickelPrice/Nickel.html').content, 'html.parser'
        ).find(id="priceh0").get_text()), 'CNY', 'USD'))/2

    Mg = (int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/MagnesiumPrice/Magnesium.html').content, 'html.parser'
        ).find(id="pricel1").get_text()) + int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/MagnesiumPrice/Magnesium.html').content, 'html.parser'
        ).find(id="priceh1").get_text()))/2

    Nb = (c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/NiobiumPrice/Niobium.html').content, 'html.parser'
        ).find(id="pricel2").get_text()), 'CNY', 'USD') + c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/NiobiumPrice/Niobium.html').content, 'html.parser'
        ).find(id="priceh2").get_text()), 'CNY', 'USD'))/2

    Mn = (int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/ManganesePrice/Manganese.html').content, 'html.parser'
        ).find(id="pricel13").get_text()) + int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/ManganesePrice/Manganese.html').content, 'html.parser'
        ).find(id="priceh13").get_text()))/2

    Mo = int((float(BeautifulSoup(
        requests.get('http://www.asianmetal.com/MolybdenumPrice/Molybdenum.html').content, 'html.parser'
        ).find(id="pricel5").get_text()) + float(BeautifulSoup(
        requests.get('http://www.asianmetal.com/MolybdenumPrice/Molybdenum.html').content, 'html.parser'
        ).find(id="priceh5").get_text()))/0.002)

    Si = int((float(BeautifulSoup(
        requests.get('http://www.asianmetal.com/SiliconPrice/Silicon.html').content, 'html.parser'
        ).find(id="pricel20").get_text()) + float(BeautifulSoup(
        requests.get('http://www.asianmetal.com/SiliconPrice/Silicon.html').content, 'html.parser'
        ).find(id="priceh20").get_text()))*2200/2)

    Ti = int((float(BeautifulSoup(
        requests.get('http://www.asianmetal.com/TitaniumPrice/Titanium.html').content, 'html.parser'
        ).find(id="pricel7").get_text()) + float(BeautifulSoup(
        requests.get('http://www.asianmetal.com/TitaniumPrice/Titanium.html').content, 'html.parser'
        ).find(id="priceh7").get_text()))/0.002)

    V = int((float(BeautifulSoup(
        requests.get('http://www.asianmetal.com/VanadiumPrice/Vanadium.html').content, 'html.parser'
        ).find(id="pricel6").get_text()) + float(BeautifulSoup(
        requests.get('http://www.asianmetal.com/VanadiumPrice/Vanadium.html').content, 'html.parser'
        ).find(id="priceh6").get_text()))/0.002)

    NV = (c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/VanadiumPrice/Vanadium.html').content, 'html.parser'
        ).find(id="pricel8").get_text()), 'CNY', 'USD') + c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/VanadiumPrice/Vanadium.html').content, 'html.parser'
        ).find(id="priceh8").get_text()), 'CNY', 'USD'))/2

    LC_Mn = (c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/FerromanganesePrice/Ferromanganese.html').content, 'html.parser'
        ).find(id="pricel7").get_text()), 'CNY', 'USD') + c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/FerromanganesePrice/Ferromanganese.html').content, 'html.parser'
        ).find(id="priceh7").get_text()), 'CNY', 'USD'))/2

    MC_Mn = (c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/FerromanganesePrice/Ferromanganese.html').content, 'html.parser'
        ).find(id="pricel3").get_text()), 'CNY', 'USD') + c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/FerromanganesePrice/Ferromanganese.html').content, 'html.parser'
        ).find(id="priceh3").get_text()), 'CNY', 'USD'))/2

    HC_Mn = (c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/FerromanganesePrice/Ferromanganese.html').content, 'html.parser'
        ).find(id="pricel2").get_text()), 'CNY', 'USD') + c.convert(int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/FerromanganesePrice/Ferromanganese.html').content, 'html.parser'
        ).find(id="priceh2").get_text()), 'CNY', 'USD'))/2

    SiMn = (int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/SilicomanganesePrice/Silicomanganese.html').content, 'html.parser'
        ).find(id="pricel22").get_text()) + int(BeautifulSoup(
        requests.get('http://www.asianmetal.com/SilicomanganesePrice/Silicomanganese.html').content, 'html.parser'
        ).find(id="priceh22").get_text()))/2

    Prices = [Al, Cu, HC_Cr, LC_Cr, SiCr, Ni, Mg, Nb, Mo, Si, Ti, V, NV, Mn, LC_Mn, MC_Mn, HC_Mn, SiMn]

    df = pd.read_csv("Metal_Weight_Per_Ton.csv") # Values to be in kg

    df["Price ($/t)"] = Prices

    target = pd.read_csv('Metal_Grades.csv')

    #convert weight % to weight/100 tons
    target[["C", "Al", "Cu", "Cr", "Ni", "Mg", "Nb", "Mn", "Mo", "Si", "Ti", "V", "N", "P", "S", "Fe"]] = (target[["C", "Al", "Cu", "Cr", "Ni", "Mg", "Nb", "Mn", "Mo", "Si", "Ti", "V", "N", "P", "S", "Fe"]]/100)*100000

    prob = LpProblem("Steel_Optimizer",LpMinimize)

    grade = j['grade']  # Input value to call on specific grades from database

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

    print("\nTotal Cost of Alloying(USD) = $",format(value(prob.objective), ',.2f'), "to make below composition")

    return target.loc[target.Grade == grade].set_index(['Grade'])

@app.route('/', methods=['GET'])
def model_info():
    """
    Returns expected input format
    """
    return str(
        """
        Expected JSON input:
        {"grade" : NUMBER}
        """
    )

@app.route('/', methods=['POST'])
def model_computation_main():
    """
    Main Model server round trip method
    """
    try:
        # This gets the data field in the post request
        j = validate_json(request.data)
        # Return a JSON back out
        return json.dumps({"result": optimize(j)})
    except ValueError as ex:  # failed schema/values validation
        return json.dumps({ "Incorrect JSON format:\n": str(ex)}), HTTP_ERROR_CLIENT
    except Exception as ex:
        return json.dumps({ "Server Error:\n": str(ex)}), HTTP_ERROR_SERVER

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)