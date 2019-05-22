import comtrade_manager as cm

# years = '201601-201812'

years = '201601-201602'

dict_countries = {40: 'austria', 112: 'belarus', 56: 'belgium', 100: 'bulgaria', 191: 'croatia', 196: 'cyprus',
                  203: 'czechia', 208: 'denmark', 233: 'estonia', 246: 'finland', 251: 'france', 276: 'germany',
                  300: 'greece', 348: 'hungary', 352: 'iceland', 372: 'ireland', 381: 'italy', 428: 'latvia',
                  440: 'lithuania', 442: 'luxembourg', 470: 'malta', 528: 'netherlands', 579: 'norway', 616: 'poland',
                  620: 'portugal', 642: 'romania', 643: 'russian federation', 703: 'slovakia', 705: 'slovenia',
                  724: 'spain', 752: 'sweden', 757: 'switzerland', 792: 'turkey', 826: 'united kingdom'}

product_list = ['02', '03', '04', '10', '07', '17', '09', '21', '22', '24', '12', '44', '45', '48', '31', '41', '4301',
                '2701', '2704', '15', '1515', '29', '28', '32', '30', '33', '31', '39', '72', '8472', '903081', '40',
                '903040', '85', '87', '94', '9406', '83', '64', '9018', '37', '93', '8715', '97', '71', '92', '96']

for k in dict_countries:
    print(dict_countries[k] + '_' + years)

    cm.download_trade_data(filename=dict_countries[k] + '_' + years, period=years, frequency='M', reporter=k,
                           partner=list(dict_countries), product=product_list)
