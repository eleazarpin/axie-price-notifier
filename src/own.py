import requests, json, os
from datetime import datetime
from dotenv import load_dotenv
from plyer import notification #for getting notification on your PC

load_dotenv()  # take environment variables from .env.

# BreedCount 0
payload = {"operationName":"GetAxieBriefList","variables":{"from":0,"size":24,"sort":"PriceAsc","auctionType":"Sale","owner":None,"criteria":{"region":None,"parts":None,"bodyShapes":None,"classes":None,"stages":[4],"numMystic":None,"pureness":None,"title":None,"breedable":None,"breedCount":[0,0],"hp":[],"skill":[],"speed":[],"morale":[]}},"query":"query GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieBrief\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieBrief on Axie {\n  id\n  name\n  stage\n  class\n  breedCount\n  image\n  title\n  battleInfo {\n    banned\n    __typename\n  }\n  auction {\n    currentPrice\n    currentPriceUSD\n    __typename\n  }\n  parts {\n    id\n    name\n    class\n    type\n    specialGenes\n    __typename\n  }\n  __typename\n}\n"}
previousId = -1
last_axie_price = -1.00
GIFT_PRICE_PERCENTAGE = 0.85
min_price = 0.00

def telegram_bot_sendtext(bot_message):
    bot_token = os.environ.get("BOT_TOKEN")
    bot_chatID = '1646866991' # my chat con Axie bot
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

# def determine_is_gift(last_axie_price, current_axie_price):
#     if last_axie_price != -1.00:
#         gift_price = last_axie_price * GIFT_PRICE_PERCENTAGE
#         print('gift price ->' + str(gift_price))
#         if current_axie_price <= gift_price:
#             return True
#         else:
#             return False
#     else:
#         return False

# def set_today_gift_price():
#     response = requests.post('https://axieinfinity.com/graphql-server-v2/graphql', json=payload)
#     json_response = response.json()
#     axies = json_response['data']['axies']
#     total = axies['total']
#     results = axies.get('results')
#     cheaperAxie = results[0]
#     current_axie_price = cheaperAxie['auction']['currentPriceUSD']
#     gift_price = float(current_axie_price) * GIFT_PRICE_PERCENTAGE
#     print('\nGood morning 👋!\nGift price 🎁 for today ' +
#           datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' is: ' + str(gift_price) + ' USD')
#     print('Today there is a total of: ' + str(total) + ' Axies listed for this filter')
#     print('----')


### BEGIN ###

# notification.notify(
#     #title of the notification,
#     title = "Axie Gift now {}".format(datetime.now()),
#     #the body of the notification
#     message = "Axie Gift!",  
#     #creating icon for the notification
#     #we need to download a icon of ico file format
#     app_icon = "images\\axie-infinity.ico",
#     # the notification stays for 50sec
#     timeout  = 5)


while True:
    try:
        response = requests.post('https://axieinfinity.com/graphql-server-v2/graphql', json=payload)
        json_response = response.json()
        axies = json_response['data']['axies']
        total = axies['total']
        results = axies.get('results')
        cheaperAxie = results[0]
        id = cheaperAxie['id']
        current_axie_price = cheaperAxie['auction']['currentPriceUSD']
        if id != previousId:
            now = datetime.now()
            # is_gift = determine_is_gift(last_axie_price, float(current_axie_price))

            # if is_gift:
            message = "*Hora:* {} ⌚\n".format(now.strftime("%d/%m/%Y %H:%M:%S"))
            message += "*Filtro:* [Breedcount 0](https://marketplace.axieinfinity.com/axie?stage=4%26breedCount=0%26breedCount=0) \n"
            message += "*Precio:* {} USD 💵\n".format(current_axie_price)
            message += "*Link:* https://marketplace.axieinfinity.com/axie/{}".format(id)

            print(message)
            console = telegram_bot_sendtext(message)

            print(console)
            previousId = id
            last_axie_price = float(current_axie_price)
    except Exception as e:
        print(e)






