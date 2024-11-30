from telebot import TeleBot
import db
from time import sleep
TOKEN = "7264000938:AAHincdm2zqWZWDQ2FsHDqAgOyAGirZoUlM"
bot = TeleBot(TOKEN) 
game = False
night = True


@bot.message_handler(commands=['play'])
def game_on(message):
    bot.send_message(message.chat.id, text='готов играть в лс')

@bot.message_handler(func=lambda m: m.text.lower() == 'готов играть')
def send_tetx(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name} играет')
    bot.send_message(message.from_user.id, 'Вы добавлены')
    db.insert_player(message.from_user.id, username=message.from_user.first_name)

@bot.message_handler(commands=['game'])
def game_start(message):
    global gamep
    players = db.players_amount()
    if players >= 5 and not game:
        db.set_roles(players)
        players_roles = db.get_palyers_roles()
        mafia_username = db.get_mafia_usernames() 
        for player_id, role in players_roles:
            bot.send_message(player_id, text=role)
            if role == 'mafia':
                bot.send_message(player_idtext=f'Все члены мафии:\n{mafia_username}' )
        game = True
        bot.send_message(message.chat.id, text='Игра началась!')
        return
    
    bot.send_message(message.chat.id, text='недостаточно людей')


@bot.message_handler(commands=["kick"])
def kick(message):
    username = ' '.join(message.text.split(' ')[1:])
    username = db.get_all_alive()
    if not night:
        if not username in username:
            bot.send_message(message.chat.id, 'Такого имени нет')
            return
        voted = db.vote("citizen_vote", username, message.from_user.id)
        if voted:
            bot.send_message(message.chat.id, 'Ваш голос учитан')
            return
        bot.send_message(message.chat.id, 'У вас больше нет право голосовать')
        return
    bot.send_message(message.chat.id, 'Сейчас ночь вы не можете никого выгнать')

@bot.message_handler(commands=["kill"])
def kill(message):
    usernames = db.get_all_alive()
    username = ' '.join(message.text.split(' ')[1:])
    mafia_username = db.get_mafia_usernames()
    if night and message.from_user.first_name in mafia_username:
        if not username in usernames:
            bot.send_message(message.chat.id, 'Такого имени нет')
            return
        voted = db.vote("mafia_vote", username, message.from_user.id)
        if voted:
            bot.send_message(message.chat.id, 'Ваш голос учитан')
            return
        bot.send_message(message.chat.id, 'У вас больше нет право голосовать')
        return
    bot.send_message(message.chat.id, 'Сейчас день вы не можете никого убить')

def get_killed(night):
    if not night:
        username_killed = db.citizen_kill()
        return f'Горожане выгнали: {username_killed}'
    username_killed = db.mafia_kill()
    return f'Мафия убила: {username_killed}'

def game_loop(message):
    global night
    bot.send_message(message.chat.id, "Добро пожаловать в игру! Вам дается 2 минуты, чтобы познакомится")
    sleep(120)
    while True:
        msg = get_killed(night)
        bot.send_message(message.chat.id, msg)
        if not night:
            bot.send_message(message.chat.id, "Город засыпает, просыпается мафия.Наступает ночь")
        else:
            bot.send_message(message.chat.id, "Город просыпается, наступает день")
        winner = db.check_winner()
        if winner == 'mafia' or winner == 'citizen':
            game = False
            bot.send_message(message.chat.id, text=f"Игра окончена победили: {winner}")
            return
        db.clear(dead=False)
        night = not night
        alive = db.get_all_alive
        alive = '\n'.join(alive)
        bot.send_message(message.chat.id, text=f"В игре:\n{alive}")
        sleep(120)




if __name__ == '__main__':
    bot.polling(non_stop=True)    