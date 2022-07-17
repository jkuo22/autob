
import telepot

def send( message, document, sender_token, receiver_id ):
    bot = telepot.Bot( sender_token )

    bot.sendMessage( receiver_id, message )
    if document:
        with open( document, 'rb' ) as document:
            bot.sendDocument( receiver_id, document )
