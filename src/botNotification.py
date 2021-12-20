import requests, os
from datetime import datetime
from dotenv import load_dotenv
# from plyer import notification #for getting notification on your PC

load_dotenv()  # take environment variables from .env.

GIFT_PRICE_PERCENTAGE = float(os.environ.get("GIFT_PRICE_PERCENTAGE"))

def telegram_bot_sendtext(bot_message):
    bot_token = os.environ.get("BOT_TOKEN")
    # bot_chatID = '1646866991'
    bot_chatID = os.environ.get("BOT_CHAT_ID")
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def determine_is_gift(first_price, second_price):
    gift_price = second_price * GIFT_PRICE_PERCENTAGE
    print('gift price ->' + str(gift_price))
    if first_price <= gift_price:
        return True
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
    previous_id = -1
    while True:
        try:
            response = requests.post('https://axieinfinity.com/graphql-server-v2/graphql', json=payload)
            response.raise_for_status()
            if response != None:
                json_response = response.json()
                axies = json_response['data']['axies']
                total = axies['total']

                if total == 1:
                    results = axies.get('results')
                    first_axie = results[0]
                    first_id = first_axie['id']
                    first_axie_price = first_axie['auction']['currentPriceUSD']

                    message = "*Hora:* {} ⌚\n".format(now.strftime("%d/%m/%Y %H:%M:%S"))
                    message += "*Filtro:* {} \n".format(filter.replace('&', '%26'))
                    message += "*Precio:* {} USD 💵\n".format(first_axie_price)
                    message += "*Análisis precio:* existe un sólo axie listado para este filtro."
                    message += "\n*Link:* https://marketplace.axieinfinity.com/axie/{}".format(first_id)

                    print(message + '\n')
                    console = telegram_bot_sendtext(message)
                    print(console)
                else:

                    if total > 1:
                        results = axies.get('results')
                        first_axie = results[0]
                        first_id = first_axie['id']
                        first_axie_price = first_axie['auction']['currentPriceUSD']

                        second_axie = results[1]
                        second_id = second_axie['id']
                        second_axie_price = second_axie['auction']['currentPriceUSD']

                        if first_id != previous_id:
                            now = datetime.now()
                            is_gift = determine_is_gift(float(first_axie_price), float(second_axie_price))
                            
                            print('first: ' + str(first_axie_price))
                            print('second: ' + str(second_axie_price))

                            cheaper_percentage = 100.00 - ((float(first_axie_price) * 100) / float(second_axie_price))

                            if is_gift:

                                message = "*Hora:* {} ⌚\n".format(now.strftime("%d/%m/%Y %H:%M:%S"))
                                message += "*Filtro:* {} \n".format(filter.replace('&', '%26'))
                                message += "*Precio:* {} USD 🎁🎁🎁\n".format(first_axie_price)
                                message += "*Análisis precio:* axie más barato de la lista de un total de {}.".format(total)
                                message += " El siguiente sale {} USD. Este axie es un {:.2f}% más barato.\n".format(second_axie_price, cheaper_percentage)
                                message += "*Link:* https://marketplace.axieinfinity.com/axie/{}".format(first_id)

                                print(message + '\n')
                                console = telegram_bot_sendtext(message)
                                print(console)
                            else: 
                                if all_prices:
                                    
                                    message = "*Hora:* {} ⌚\n".format(now.strftime("%d/%m/%Y %H:%M:%S"))
                                    message += "*Filtro:* {} \n".format(filter.replace('&', '%26'))
                                    message += "*Precio:* {} USD 💵\n".format(first_axie_price)
                                    message += "*Análisis precio:* axie más barato de la lista de un total de {}.".format(total)
                                    message += " El siguiente sale {} USD. Este axie es un {:.2f}% más barato.\n".format(second_axie_price, cheaper_percentage)
                                    message += "*Link:* https://marketplace.axieinfinity.com/axie/{}".format(first_id)

                                    print(message + '\n')
                                    console = telegram_bot_sendtext(message)
                                    print(console)

                            previous_id = first_id

        except requests.exceptions.HTTPError as e:
            print("{} -- {}".format(datetime.now(), e))
        except Exception as e:
            print("{} -- {}".format(datetime.now(), e))