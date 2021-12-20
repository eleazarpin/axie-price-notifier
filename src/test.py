from dotenv import load_dotenv
import os
from datetime import datetime
import requests, os

load_dotenv()  # take environment variables from .env.

payload = {"operationName":"GetAxieBriefList","variables":{"from":0,"size":24,"sort":"PriceAsc","auctionType":"Sale","owner":None,"criteria":{"region":None,"parts":None,"bodyShapes":None,"classes":None,"stages":[4],"numMystic":None,"pureness":None,"title":None,"breedable":None,"breedCount":[0,0],"hp":[],"skill":[],"speed":[],"morale":[]}},"query":"query GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieBrief\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieBrief on Axie {\n  id\n  name\n  stage\n  class\n  breedCount\n  image\n  title\n  battleInfo {\n    banned\n    __typename\n  }\n  auction {\n    currentPrice\n    currentPriceUSD\n    __typename\n  }\n  parts {\n    id\n    name\n    class\n    type\n    specialGenes\n    __typename\n  }\n  __typename\n}\n"}


try:
    print('console 1')
    response = requests.post(
        'https://axieinfinity.com/graphql-server-v2/graphql', json=payload)
    print('console 2')
    if response != None:
        print('console 3')
        print(response)
        # json_response = response.json()
        # axies = json_response['data']['axies']
        # total = axies['total']
        # results = axies.get('results')
        # cheaperAxie = results[0]
        # id = cheaperAxie['id']
        # current_axie_price = cheaperAxie['auction']['currentPriceUSD']
        # if id != previousId:
        #     now = datetime.now()
        #     is_gift = determine_is_gift(previous_axie_price, float(current_axie_price))
        #     print('previous: ' + str(previous_axie_price))
        #     print('current: ' + str(current_axie_price))

        #     # Porque pasa esto??
        #     if float(current_axie_price) <= previous_axie_price:
        #         cheaper_percentage = 100.00 - ((float(current_axie_price) * 100) / previous_axie_price)

        #     if is_gift:

        #         message = "*Hora:* {} ⌚\n".format(now.strftime("%d/%m/%Y %H:%M:%S"))
        #         message += "*Filtro:* {} \n".format(filter)
        #         message += "*Precio:* {} USD 🎁🎁🎁\n".format(current_axie_price)
        #         message += "*Análisis precio:* El siguiente axie mas bárato sale {} USD. Este axie es un {:.2f}% más barato\n".format(previous_axie_price, cheaper_percentage)
        #         message += "*Link:* https://marketplace.axieinfinity.com/axie/{}".format(id)

        #         print(message + '\n')
        #         console = telegram_bot_sendtext(message)
        #         print(console)
        #     else:
        #         if all_prices:

        #             message = "*Hora:* {} ⌚\n".format(now.strftime("%d/%m/%Y %H:%M:%S"))
        #             message += "*Filtro:* {} \n".format(filter)
        #             message += "*Precio:* {} USD 💵\n".format(current_axie_price)
        #             message += "*Análisis precio:* axie más barato de la lista de un total de {}.".format(total)
        #             if previous_axie_price != -1 and float(current_axie_price) <= previous_axie_price:
        #                 message += "El siguiente sale {} USD. Este axie es un {:.2f}% más barato.".format(previous_axie_price, cheaper_percentage)
        #             message += "\n*Link:* https://marketplace.axieinfinity.com/axie/{}".format(id)

        #             print(message + '\n')
        #             console = telegram_bot_sendtext(message)
        #             print(console)

        #     previousId = id

        # # Pequeña mejora para dejar siempre actualizado el precio del axie
        # previous_axie_price = float(current_axie_price)

except Exception as e:
    print("{} -- {}".format(datetime.now(), e))
