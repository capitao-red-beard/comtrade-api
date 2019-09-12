import comtrade_manager as cm
import xlrd


years = "201907-201908"

dict_countries_reporter = {
    40: "austria",
    112: "belarus",
    56: "belgium",
    100: "bulgaria",
    191: "croatia",
    196: "cyprus",
    203: "czechia",
    208: "denmark",
    233: "estonia",
    246: "finland",
    251: "france",
    276: "germany",
    300: "greece",
    348: "hungary",
    352: "iceland",
    372: "ireland",
    381: "italy",
    428: "latvia",
    440: "lithuania",
    442: "luxembourg",
    470: "malta",
    528: "netherlands",
    579: "norway",
    616: "poland",
    620: "portugal",
    642: "romania",
    643: "russian federation",
    703: "slovakia",
    705: "slovenia",
    724: "spain",
    752: "sweden",
    757: "switzerland",
    792: "turkey",
    826: "united kingdom"
}

dict_countries_partner = {
    40: "austria",
    112: "belarus",
    56: "belgium",
    100: "bulgaria",
    191: "croatia",
    196: "cyprus",
    203: "czechia",
    208: "denmark",
    233: "estonia",
    246: "finland",
    251: "france",
    276: "germany",
    300: "greece",
    348: "hungary",
    352: "iceland",
    372: "ireland",
    381: "italy",
    428: "latvia",
    440: "lithuania",
    442: "luxembourg",
    470: "malta",
    528: "netherlands",
    579: "norway",
    616: "poland",
    620: "portugal",
    642: "romania",
    643: "russian federation",
    703: "slovakia",
    705: "slovenia",
    724: "spain",
    752: "sweden",
    757: "switzerland",
    792: "turkey",
    826: "united kingdom"
}

product_list = [f"{i:02d}" for i in range(1, 100) if i != 98]
wb = xlrd.open_workbook('data\HS4_codes.xlsx')
sheet = wb.sheet_by_index(0)
products = sheet.col_values(0, 1)

to_remove_products = [i[0:2] for i in products]
to_remove_products = list(set(to_remove_products))
subtracted_list = [i for i in product_list if i not in to_remove_products]
product_list = subtracted_list + products

for k in dict_countries_reporter:
    print(f"{dict_countries_reporter[k]}_{years}")

    cm.download_trade_data(
        filename=f"{dict_countries_reporter[k]}_{years}",
        period=years,
        frequency="M",
        reporter=k,
        partner=list(dict_countries_partner),
        product=product_list
    )
