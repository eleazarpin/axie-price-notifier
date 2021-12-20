import requests, os
from datetime import datetime
from dotenv import load_dotenv
# from plyer import notification #for getting notification on your PC

load_dotenv()  # take environment variables from .env.

GIFT_PRICE_PERCENTAGE = float(os.environ.get("GIFT_PRICE_PERCENTAGE"))

def telegram_bot_sendtext(bot_message):
    bot_token = os.environ.get("BOT_TOKEN")
    bot_chatID = '1646866991'
    # bot_chatID = os.environ.get("BOT_CHAT_ID")
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def determine_is_gift(last_axie_price, current_axie_price):
    if last_axie_price != -1.00 and current_axie_price <= last_axie_price:
        gift_price = last_axie_price * GIFT_PRICE_PERCENTAGE
        print('gift price ->' + str(gift_price))
        if current_axie_price <= gift_price:
            return True
        else:
            return False
    else:
        return False

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

def send_message(payload, filter, all_prices):
    previousId = -1
    previous_axie_price = -1.00
    while True:
        try:
            response = requests.post('https://axieinfinity.com/graphql-server-v2/graphql', json=payload)
            response.raise_for_status()
            if response != None:
                json_response = response.json()
                axies = json_response['data']['axies']
                total = axies['total']
                if total > 0:
                    results = axies.get('results')
                    first_cheaper_axie = results[0]
                    id = first_cheaper_axie['id']
                    current_axie_price = first_cheaper_axie['auction']['currentPriceUSD']
                    if id != previousId:
                        now = datetime.now()
                        is_gift = determine_is_gift(previous_axie_price, float(current_axie_price))
                        print('previous: ' + str(previous_axie_price))
                        print('current: ' + str(current_axie_price))

                        # Porque pasa esto??
                        if float(current_axie_price) < previous_axie_price:
                            cheaper_percentage = 100.00 - ((float(current_axie_price) * 100) / previous_axie_price)

                        if is_gift:

                            message = "*Hora:* {} ⌚\n".format(now.strftime("%d/%m/%Y %H:%M:%S"))
                            message += "*Filtro:* {} \n".format(filter.replace('&', '%26'))
                            message += "*Precio:* {} USD 🎁🎁🎁\n".format(current_axie_price)
                            message += "*Análisis precio:* El siguiente axie mas bárato sale {} USD. Este axie es un {:.2f}% más barato\n".format(previous_axie_price, cheaper_percentage)
                            message += "*Link:* https://marketplace.axieinfinity.com/axie/{}".format(id)

                            print(message + '\n')
                            console = telegram_bot_sendtext(message)
                            print(console)
                        else: 
                            if all_prices:
                                
                                message = "*Hora:* {} ⌚\n".format(now.strftime("%d/%m/%Y %H:%M:%S"))
                                message += "*Filtro:* {} \n".format(filter.replace('&', '%26'))
                                message += "*Precio:* {} USD 💵\n".format(current_axie_price)
                                message += "*Análisis precio:* axie más barato de la lista de un total de {}.".format(total)
                                if previous_axie_price != -1 and float(current_axie_price) < previous_axie_price:
                                    message += "El siguiente sale {} USD. Este axie es un {:.2f}% más barato.".format(previous_axie_price, cheaper_percentage)
                                message += "\n*Link:* https://marketplace.axieinfinity.com/axie/{}".format(id)

                                print(message + '\n')
                                console = telegram_bot_sendtext(message)
                                print(console)

                        previousId = id

                    # Pequeña mejora para dejar siempre actualizado el precio del axie
                    previous_axie_price = float(current_axie_price)

        except requests.exceptions.HTTPError as e:
            print("{} -- {}".format(datetime.now(), e))
        except Exception as e:
            print("{} -- {}".format(datetime.now(), e))