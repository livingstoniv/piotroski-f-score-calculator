import yahoo_fin.stock_info as yf



# ticker and financial information
ticker = input('Enter Your Ticker Here: ')
balance_sheet = yf.get_balance_sheet(ticker)
income_statement = yf.get_income_statement(ticker)
cfs = yf.get_cash_flow(ticker)

#uncomment to look at individual financials of a ticker

# print(income_statement)
# print(balance_sheet)
# print(cfs)

#profitability variables
years_is = income_statement.columns
years_cfs = cfs.columns
years_bs = balance_sheet.columns


net_income = income_statement[years_is[0]]['netIncome']
net_income_previous = income_statement[years_is[1]]['netIncome']

op_cf = cfs[years_cfs[0]]['totalCashFromOperatingActivities']

average_assets = balance_sheet[years_bs[0]]['totalAssets'] + balance_sheet[years_bs[1]]['totalAssets'] / 2
average_assets_py = balance_sheet[years_bs[1]]['totalAssets'] + balance_sheet[years_bs[2]]['totalAssets'] / 2

RoA = net_income / average_assets
RoA_py = net_income_previous / average_assets_py

total_assets = balance_sheet[years_bs[0]]['totalAssets']
accruals = op_cf / total_assets - RoA

ni_score = []
ni_score_2 = []
op_cf_score = []
RoA_score = []
ac_score = []

#return on assets score
if net_income > 0 and net_income > net_income_previous:
    ni_score = 1
    ni_score_2 = 1
elif net_income > 0 and net_income < net_income_previous:
    ni_score = 1
    ni_score_2 = 0
elif net_income < 0 and net_income > net_income_previous:
    ni_score = 0
    ni_score_2 = 1
else:
    ni_score = 0
    ni_score_2 = 0

#operating cash flow score
if op_cf > 0:
    op_cf_score = 1
else:
    op_cf_score = 0

#change in RoA score
if RoA > RoA_py:
    RoA_score = 1
else:
    RoA_score = 0

#accruals score
if accruals > 0:
    ac_score = 1
else:
    ac_score = 0

#profitability score
profitability_score = ni_score + ni_score_2 + op_cf_score + RoA_score + ac_score
print("The profitability score is: ")
print(profitability_score)

# leverage variables
lt_debt = balance_sheet[years_bs[0]]['longTermDebt']
debt_ratio = lt_debt / total_assets
debt_ratio_score = []

current_assets = balance_sheet[years_bs[0]]['totalCurrentAssets']
current_liab = balance_sheet[years_bs[0]]['totalCurrentLiabilities']
current_ratio = current_assets / current_liab
current_ratio_score = []


#leverage score

if debt_ratio < 0.4:
    debt_ratio_score = 1
else:
    debt_ratio_score = 0
if current_ratio > 1:
    current_ratio_score = 1
else:
    current_ratio_score = 0
leverage_score = debt_ratio_score + current_ratio_score
print("The leverage score is:")
print(leverage_score)

#operating efficiency variables
gp = income_statement[years_is[0]]['grossProfit']
gp_py = income_statement[years_is[1]]['grossProfit']
revenue = income_statement[years_is[0]]['totalRevenue']
revenue_py = income_statement[years_is[1]]['totalRevenue']

gm = gp / revenue
gm_py = gp_py / revenue_py
gm_score = []

asset_turnover = revenue / average_assets
asset_turnover_py = revenue_py / average_assets_py
asset_turnover_score = []

#operating efficiency score

if gm > gm_py:
    gm_score = 1
else:
    gm_score = 0

if asset_turnover > asset_turnover_py:
    asset_turnover_score = 1
else:
    asset_turnover_score = 0


operating_efficiency_score = gm_score + asset_turnover_score
print("The operating efficiency score is:")
print(operating_efficiency_score)

#This is the addition of all scores together

piotroski_f_score = profitability_score + leverage_score + operating_efficiency_score
print("The Piotroski F-score is: ")
print(piotroski_f_score)