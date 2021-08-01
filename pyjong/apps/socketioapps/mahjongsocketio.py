from flask_socketio import join_room,leave_room,emit
from pyjong import socketio
from flask_login import current_user
from flask import session,redirect
from time import time


#data will be stored in a universal variable as a dictionary
#the dictionary will have the current status of a game in a room saved
#{'room1':[kyoku,player1,player2......]}
room_dict = dict()

#room dict is used in Kyoku so import must be done after creation
from pyjong.apps.mahjong.yama import Yama
from pyjong.apps.mahjong.game import Game


@socketio.on('start',namespace='/main/game')
def startgame():
    global room_dict
    if session['players'] == 1:
        game = Game()
        game.create_players(session['username'])
        game.oya_gime()
        room_dict[session['room']] = [game,'']
        room_dict[session['room']][0].kyoku_start()
        #kyoku.game will set index 1 value of room dict to define what the next input will be




@socketio.on('gamecheck',namespace='/main/game')
def gamecheck():
    global room_dict
    emit('gameupdate',{'msg':str(room_dict[session['room']][0].kyoku.yama.all_yama[0][0][0])})

@socketio.on('gamecontrol',namespace='/main/game')
def gamecontrol(choice):
    choice = choice.upper()
    print(choice)
    #check what the next input type will be
    if room_dict[session['room']][1] == 'kyokustart_yesno':
        room_dict[session['room']][0].kyoku.kyoku_start_non_computer(choice)
    elif room_dict[session['room']][1] == 'kyoku_yesno':
        room_dict[session['room']][0].kyoku.player_turn_input(choice)
