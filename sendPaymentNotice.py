
import telepot

def send( message, document, sender_token, receiver_id ):
    bot = telepot.Bot( sender_token )

    with open( document, 'rb' ) as document:
        bot.sendMessage( receiver_id, message )
        bot.sendDocument( receiver_id, document )
