
import sqlite3
import random

def insert_player(player_id, username):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"insert into players (player_id, username) Values ('{player_id}', '{username}')"
    cur.execute(sql)
    con.commit()
    con.close

def players_amount():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"select * from players"
    cur.execute(sql)
    res = cur.fetchall()
    con.close()
    return len(res)

def get_mafia_usernames():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"select username from players where role = 'mafia' "
    cur.execute(sql)
    data = cur.fetchall()
    names = ''
    for row in data:
        name = row[0]
        names += name + '\n'
    con.close()
    return names
        
def get_palyers_roles():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"select player_id, role From players"
    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data

def get_all_alive():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT username FROM players WHERE dead = 0"
    cur.execute(sql)
    data = cur.fetchall()
    data = [row[0] for row in data]
    con.close()
    return data

def set_roles(players):
    game_roles = ['citizen']*players
    mafia = int(players*0.3)
    for i in range(mafia):
        game_roles[1] = 'mafia'
    random.shuffle(game_roles)
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute("select player_id, role From players")
    player_ids_rows = cur.fetchall()
    for role, row in zip(game_roles, player_ids_rows):
        sql = f"update players set role = '{role}' where player_id = {row[0]}"
        cur.execute(sql)
    con.commit()
    con.close()


def vote(type, username, player_id):
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute(f"SELECT username FROM players WHERE player_id = {player_id} and dead=0 and voted=0")
    can_vote = cur.fetchall()
    if can_vote:
        cur.execute(f"update players set {type}={type}+1 where username = '{username}' ")
        cur.execute(f"update players set voted=1 where player_id = '{player_id}'")
        con.commit()
        con.close()
        return True
    con.close()
    return False

def mafia_kill():
    con = sqlite3.connect('db.db')
    cur = con.cursor(  )
    cur.execute(f"select Max(mafia_vote) from players")
    max_votes = cur.fetchall()[0]
    cur.execute(f"select count(*) from players where dead = 0 and role = 'mafia' ")
    mafia_alive = cur.fetchall()[0]
    username_killed = 'никого'
    if max_votes == mafia_alive:
        cur.execute(f"select username from platers where mafia_vote = '{max_votes}' ")
        username_killed = cur.fetchall()[0]
        cur.execute(f"update players set dead=1 where username= '{username_killed}'")
        con.commit()
    con.close()
    return username_killed

def citizen_kill():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute(f"select max(citizen_vote) from players")
    max_votes = cur.fetchall()[0]
    cur.execute(f"select count(*) from players where citizen_vote = '{max_votes}' ")
    max_votes_count = cur.fetchall()[0]
    username_killed = 'никого'
    if max_votes_count == 1:
        cur.execute(f"select username from players where citizen_vote = '{max_votes}' ")
        username_killed = cur.fetchall()[0]
        cur.execute(f"update players set dead=1 where username = '{username_killed}' ")
        con.commit()
    con.close()
    return username_killed
