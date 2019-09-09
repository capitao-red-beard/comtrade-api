import comtrade_manager as cm

years = "201806-201906"

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
