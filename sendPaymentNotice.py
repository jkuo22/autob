
#token = '5488502800:AAEUlnO0EI5gNfqqFHph8bZPNc9n57mBk-0' # Token of telegram user 'autobilling_2svpn'

# link: https://api.telegram.org/bot5488502800:AAEUlnO0EI5gNfqqFHph8bZPNc9n57mBk-0/getUpdates
# to see the message which 'autobilling_2svpn' is receiving from; it's used to locate sender_id,
# and in turn to be used as receiver_id when sending message back.

#receiver_id = 1649016499 # telegram id of "Tech 2svpn"
#document='autobilling.pdf'
import telepot

def send( message, document, sender_token, receiver_id ):
    bot = telepot.Bot( sender_token )

    with open( document, 'rb' ) as document:
        bot.sendMessage( receiver_id, message )
        bot.sendDocument( receiver_id, document )
