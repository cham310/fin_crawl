import telegram

cham_token = ''

cham = telegram.Bot(token=cham_token)
updates = cham.getUpdates()
for u in updates:
    print(u.message.text)