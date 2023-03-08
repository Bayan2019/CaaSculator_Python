import pandas as pd

yahoo_logo = 'https://raw.githubusercontent.com//Bayan2019/TCC/main/Yahoo-Finance-3.png'
tcc_logo = 'https://raw.githubusercontent.com//Bayan2019/TCC/main/Logo_Curve_BG-Blue1.png'

CaaSWalletIPhone_bg = 'url(https://raw.githubusercontent.com//Bayan2019/TCC_Dashboard/main/pictures/CaaSWallet2_2.png)'

InventoryCard = 'url(https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/pictures/InventoryCard.png)'
FactoringCard = 'url(https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/pictures/FactoringCard.png)'
SupplierCard = 'url(https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/pictures/SupplierCard.png)'

TCC = 'url(https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/pictures/Logo_Curve_BG-Blue1.png)'
header = 'url(https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/pictures/Header.png)'
header2='url(https://raw.githubusercontent.com/alexandre-tcc/CaaS_Calculator/CaaS Calculator header.png)'

Finance3 = 'url(https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/pictures/Finance3.png)'

ebitda = 'url(https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/pictures/ebitda2.png)'
debt = 'url(https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/pictures/debt2.png)'
wc = 'url(https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/pictures/WORKINGCAPITAL.png)'
revenue = 'url(https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/pictures/Revenue.jpeg)'
GP = 'url(https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/pictures/GrossProfit.png)'
cash = 'url(https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/pictures/cash2.png)'
yahoo = 'url(https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/pictures/Yahoo.png)'
inventory = 'url(https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/pictures/inventory.png)'

# Data Files

ucr_csv_annual = 'https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/Files_of_Data/fs_annual_ws.csv'
ucr_csv_annual_new = 'https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/Files_of_Data/fs_annual_new_ws.csv'
ucr_csv_quartal = 'https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/Files_of_Data/fs_quartal_ws.csv'

df_annual = pd.read_csv(ucr_csv_annual)
df_annual_new = pd.read_csv(ucr_csv_annual_new)
df_quartal = pd.read_csv(ucr_csv_quartal)


ucr_csv_annual_usd = 'https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/Files_of_Data/fs_annual_usd_ws.csv'
ucr_csv_annual_new_usd = 'https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/Files_of_Data/fs_annual_new_usd_ws.csv'
ucr_csv_quartal_usd = 'https://raw.githubusercontent.com/Bayan2019/TCC_Dashboard/main/Files_of_Data/fs_quartal_usd_ws.csv'

df_annual_usd = pd.read_csv(ucr_csv_annual_usd, verify=False)
df_annual_new_usd = pd.read_csv(ucr_csv_annual_new_usd, verify=False)
df_quartal_usd = pd.read_csv(ucr_csv_quartal_usd, verify=False)