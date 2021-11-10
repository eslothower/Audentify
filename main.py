#Authors: Senam Anagalte, Eladio Andujar, Amira Johnson, Eli Slothower

from cmu_112_graphics import *
import random
import os
from requests import *
import requests
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import speech_recognition as sr
from selenium import webdriver
import time
from selenium.webdriver.chrome.webdriver import WebDriver



#########################################################################################################################
#appStarted
#########################################################################################################################

def appStarted(app):
    app.mode = 'homescreen'
    app.previousModeWasStandardIdentifyer = False
    app.targetWordIsInSpeech = False
    app.timerDelay = 300
    app.points = 0
    app.counter = 10
    app.timeElapsed = 0
    app.round = 0
    app.wordList = ['love', 'me', 'sugar', 'girlfriend', 'summer', 'fall', 'perfect', 'smile', 'time', 'someone', 'boys', 'USA', 'boyfriend', 'mamma', 'run', 'dream', 'shape', 'you', 'why', 'girls', 'boys', 'girlfriend', 'black', 'mind', 'knew', 'this', 'december', 'kill', 'show', 'rain', 'main', 'when', 'lost', 'mind', 'blue', 'remind', 'believe', 'heard', 'send', 'myself', 'hurt', 'deny', 'location', 'keep', 'falling', 'never', 'found', 'know', 'open', 'fear', 'into', 'pressure', 'listen', 'getting']
    #app.wordList = ['send']
    app.songName = ''
    app.songArtist = ''
    app.image = ''
    url = 'https://www.pikpng.com/pngl/b/40-404161_1760-x-2560-5-fl-studio-fruity-dance.png'
    spritestrip = app.loadImage(url)
    app.sprites = []
    for i in range(8):
        sprite = spritestrip.crop((20+200*i, 250, 100+235*i, 500))
        app.sprites.append(sprite)
    app.spriteCounter = 0


#########################################################################################################################
#Selenium/Music Playback
#########################################################################################################################


#adpated from https://youtube.com/watch?v=YhedkJxxFuU&ab_channel=ApniCoding
driver = webdriver.Chrome(r"/Users/eslothower/Desktop/hack112_v2/chromedriver")
driver.get('https://www.youtube.com/')


def musicPlayback(app):
    

    input = app.songName
    
    search_box = driver.find_element_by_name('search_query')
    search_box.send_keys(f'{input} lyrics')

    search_box.submit()
    time.sleep(1)

    driver.find_element_by_id('video-title').click()
    time.sleep(17)
    driver.get('https://www.youtube.com/')

#########################################################################################################################
# Core Logic
#########################################################################################################################

#Sets random word for game
def getWord(app):
    app.targetWord = app.wordList[random.randint(0, len(app.wordList)-1)]


#Adapted from (but with heavy changes) https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
#Turns speech into text (i.e. a string of lyrics) using a speech recognition algorithm
def getSongLyricsFromSpeech(app):

    # Sampling frequency
    freq = 44100

    # Recording duration
    duration = 10

    print("recording")

    # Start recorder with the given values
    # of duration and sample frequency
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)

    # Record audio for the given number of seconds
    sd.wait()

    print("done recording")

    # This will convert the NumPy array to an audio
    # file with the given sampling frequency
    write("recording0.wav", freq, recording)

    # Convert the NumPy array to audio file
    file = wv.write("recording1.wav", recording, freq, sampwidth=2)

    print("done audio to wav")

    filename = "recording1.wav"
    r = sr.Recognizer()

    # open the file
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
    try:
        lyrics = r.recognize_google(audio_data)
        print(lyrics)
        if app.previousModeWasStandardIdentifyer == False:
            lyrics = lyrics.lower()
            splitLyrics = lyrics.split(" ")
            print(splitLyrics)

            app.targetWordIsInSpeech = False

            for word in splitLyrics:
                if word == app.targetWord:
                    app.targetWordIsInSpeech = True
                    print("The target word was in the speech")
                    break
            
            if app.targetWordIsInSpeech == False: 
                app.mode = 'targetWordMissed'
                return

        #print(text)
        result = getInfo(lyrics)

        if (len(result[0]) == 0):
            print("It went here at empty list")
            app.mode = 'noSongDetected'
        else:



            app.songName = result[0][0]
            app.songArtist = result[1][0]
            app.image = app.loadImage(result[2][0])
            app.mode = 'showSong'
            musicPlayback(app)
            return
        #return text
    except Exception as e:
        print("It went here at exception")
        app.mode = 'noSongDetected'


#Adapted from https://melaniewalsh.github.io/Intro-Cultural-Analytics/04-Data-Collection/07-Genius-API.html
#Retrieves song title, song artist, and song album art from Genius based off of spoken lyrics
def getInfo(lyrics):
    searchTerm = lyrics
    accessToken = 'JVfO6-IbkvPvyKt39NzaZiqvcpyoHucGBu8qxCr8P1utrjeOZZhFs875q9bkfMA8'
    url = f"http://api.genius.com/search?q={searchTerm}&access_token={accessToken}"

    response = requests.get(url)  # gets the webpage
    jsonData = response.json()  # turns it into a json file

    songImageLinks = []
    songNames = []
    songArtists = []

    # loop through json data and retrieve links to images, song names, and the artists
    for song in jsonData['response']['hits']:
        songImageLinks.append(song['result']['song_art_image_url'])
        songNames.append(song['result']['title'])
        songArtists.append(song['result']['artist_names'])

    #print("This is songNames:", songNames)
    return (songNames, songArtists, songImageLinks)

#########################################################################################################################
# Homescreen                       
#########################################################################################################################


#draw homescreen/main menu
def homescreen_redrawAll(app, canvas):

    #Background and title
    canvas.create_rectangle(0, 0, app.width, app.height, fill='black')
    canvas.create_text(app.width/2, app.height/6, text="Audentify", fill='white', font='Arial 50')

    # play button
    canvas.create_rectangle(app.width/2-250, app.height/4, app.width/2-50, app.height/4 + 50, fill='green')
    canvas.create_text(app.width/2-150, app.height/3-25, text="Play Game", fill='white', font='Arial 16')

    # normal song identifyer button
    canvas.create_rectangle(app.width/2+50, app.height/4, app.width/2+250, app.height/4 + 50, fill='green')
    canvas.create_text(app.width/2+150, app.height/3-25, text="Song Identifyer", fill='white', font='Arial 16')

    # instructions button
    canvas.create_rectangle(app.width/2-100, app.height/4+75, app.width/2 + 100, app.height/4 + 125, fill='white')
    canvas.create_text(app.width/2, app.height/2-55, text="Instructions", fill='black', font='Arial 16')

    #Snoop Dog
    sprite = app.sprites[app.spriteCounter]
    canvas.create_image(app.width/2.1, app.height/1.3, image=ImageTk.PhotoImage(sprite))


#if the buttons on the homescreen/main menu are pressed
def homescreen_mousePressed(app, event):
    currentX, currentY = event.x, event.y

    #Play game
    homescreenPlayTopX = app.width/2 - 50
    homescreenPlayTopY = app.height/4 + 50
    homescreenPlayBottomX = app.width/2 - 250
    homescreenPlayBottomY = app.height/4
    if (homescreenPlayBottomX < currentX < homescreenPlayTopX and homescreenPlayBottomY < currentY < homescreenPlayTopY):

        getWord(app)
        app.mode = 'gamePlay'
        app.previousModeWasStandardIdentifyer = False


    #Normal Song Identifyer
    homescreenIdentifyTopX = app.width/2+250
    homescreenIdentifyTopY = app.height/4 + 50
    homescreenIdentifyBottomX = app.width/2+50
    homescreenIdentifyBottomY = app.height/4
    if (homescreenIdentifyBottomX < currentX < homescreenIdentifyTopX and homescreenIdentifyBottomY < currentY < homescreenIdentifyTopY):

        getWord(app)
        app.mode = 'normalSongIdentifyer'
        app.previousModeWasStandardIdentifyer = True
        

    #Instructions
    instructionsTopX = app.width/2 + 100
    instructionsTopY = app.height/4 + 125
    instructionsBottomX = app.width/2 - 100
    instructionsBottomY = app.height/4+75
    if (instructionsBottomX < currentX < instructionsTopX and
            instructionsBottomY < currentY < instructionsTopY):
        app.mode = 'instructions'
        app.previousModeWasStandardIdentifyer = False


#Updates Snoop Dog
def homescreen_timerFired(app):
    app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)
    app.timeElapsed += app.timerDelay


#########################################################################################################################
#Instructions Screen
#########################################################################################################################

#draws instructions screen
def instructions_redrawAll(app, canvas):

    #Backdrop
    canvas.create_rectangle(0, 0, app.width, app.height, fill='black')

    #Title
    canvas.create_text(app.width/2, app.height/6, text="Instructions for Audentify", fill='white', font='Arial 40')

    #Instructions for the game
    canvas.create_text(app.width/2, app.height/3.8, text="To play, select 'Play Game' and sing a song with the provided word on the screen within 10 seconds! You get a point for every song you find that contains the word!", fill='white', font='Arial 16')
    
    #Instructions for the song identifyer
    canvas.create_text(app.width/2, app.height/3, text="You can also use Audentity to identify songs based off of your lyrics by selcting 'Song Identifyer'!", fill='white', font='Arial 16')
    
    #Homescreen/Main Menu button
    canvas.create_rectangle(app.width/3, app.height/1.3, app.width/1.5, app.height/1.15, fill = 'green', outline = 'black')

    canvas.create_text(app.width/2, app.height/1.225, text = 'Main Menu', fill = 'white', font = 'Arial 17')


def instructions_mousePressed(app, event):
    getWord(app)
    currentX, currentY = event.x, event.y

    #This button takes you to the homescreen/main menu
    instructionsMenuTopX = app.width/1.5
    instructionsMenuTopY = app.height/1.15
    instructionsMenuBottomX = app.width/3
    instructionsMenuBottomY = app.height/1.3
    
    if (instructionsMenuBottomX < currentX < instructionsMenuTopX and
            instructionsMenuBottomY < currentY < instructionsMenuTopY):

        app.mode = 'homescreen'
        app.round = 0
        app.points = 0

#########################################################################################################################
#gamePlay Screen
#########################################################################################################################

#draws gamePlay screen
def gamePlay_redrawAll(app, canvas):

    #Backdrop
    canvas.create_rectangle(0, 0, app.width, app.height, fill='black')  

    # show points
    canvas.create_text(app.width/6, app.height/10, text = f'Score: {app.points}', fill = 'white', font = 'Arial 17')

    #show round
    canvas.create_text(app.width/1.2, app.height/10, text = f'Round: {app.round}/10', fill = 'white', font = 'Arial 17')
    
    canvas.create_text(app.width/2, app.height/6, text="Sing a song with the word:", fill='white', font='Arial 30')

    canvas.create_text(app.width/2, app.height/4, text=app.targetWord, fill='white', font='Arial 35')  # onscreen text


#Gets song lyrics via the speech-to-text algorithm once the screen successfully drew the gamePlay screen, also calculates points
def gamePlay_timerFired(app):
    if app.mode == 'gamePlay':
        getSongLyricsFromSpeech(app)


    #app.timeElapsed += app.timerDelay
    if app.mode == 'noSongDetected':
        app.points += 0
    else:
        app.points += 1
        # if app.timeElapsed < 2000:
        #     app.points += 2
        # else:
        #     app.points += 1
    # app.timeElapsed = 0


   

    




#########################################################################################################################
#targetWordMissed (i.e. the target word wasn't said in the proposed lyrics)
#########################################################################################################################

#draws targetWordMissed screen (i.e. telling the player they didn't say lyrics with the target word)
def targetWordMissed_redrawAll(app, canvas):

    #Backdrop
    canvas.create_rectangle(0, 0, app.width, app.height, fill='black')  

    canvas.create_text(app.width/2, app.height/2, text=f'The word \'{app.targetWord}\' was not used in the lyrics!', fill='white', font='Arial 26')

    #Essentially a 'replay' button
    canvas.create_rectangle(app.width/3, app.height/1.3, app.width/1.5, app.height/1.15, fill = 'green', outline = 'black')

    #Chooses what (essentially) 'replay' button to display based off of mode picked from homescreen/main menu
    if app.previousModeWasStandardIdentifyer == False:
        canvas.create_text(app.width/2, app.height/1.225, text = 'Next Round', fill = 'white', font = 'Arial 17')
    else:
        canvas.create_text(app.width/2, app.height/1.225, text = 'Identify Again', fill = 'white', font = 'Arial 17')

    #Homescreen/Main Menu button
    canvas.create_rectangle(app.width/3, app.height/1.55, app.width/1.5, app.height/1.365, fill = 'green', outline = 'black')

    canvas.create_text(app.width/2, app.height/1.45, text = 'Main Menu', fill = 'white', font = 'Arial 17')

def targetWordMissed_mousePressed(app, event):
    getWord(app)
    currentX, currentY = event.x, event.y

    #This button starts a new game or song identifyer
    targetWordTopx = app.width/3
    targetWordTopY = app.height/1.3
    targetWordBottomX = app.width/1.5
    targetWordBottomY = app.height/1.15

    if (targetWordBottomX > currentX > targetWordTopx and
            targetWordBottomY > currentY > targetWordTopY):
        if app.previousModeWasStandardIdentifyer == False:
            app.mode = 'gamePlay'
            app.round += 1

            if app.round >= 11:
                app.mode = 'gameOver'

        else:
            app.mode = 'normalSongIdentifyer'

    #This button takes you to the homescreen/main menu
    targetWordMenuTopX = app.width/1.5
    targetWordMenuTopY = app.height/1.365
    targetWordMenuBottomX = app.width/3
    targetWordMenuBottomY = app.height/1.55

    if (targetWordMenuBottomX < currentX < targetWordMenuTopX and
            targetWordMenuBottomY < currentY < targetWordMenuTopY):

            app.mode = 'homescreen'
            app.round = 0
            app.points = 0


#########################################################################################################################
#showSong Screen
#########################################################################################################################

#draws showSong/result screen
def showSong_redrawAll(app, canvas):

    
    #Backdrop
    canvas.create_rectangle(0, 0, app.width, app.height, fill='black')

    #Album art
    newImage = app.scaleImage(app.image, 1/4)
    canvas.create_image(app.width/2, app.height/3, image=ImageTk.PhotoImage(newImage))  

    #song name and artist
    canvas.create_text(app.width/2, app.height/1.7, text=f'"{app.songName}" by {app.songArtist}', font="Arial 23", fill='white')
    
    # show points only for game mode
    if app.previousModeWasStandardIdentifyer == False:
        # show points
        canvas.create_text(app.width/6, app.height/10, text = f'Score: {app.points}', fill = 'white', font = 'Arial 17')

        #show round
        canvas.create_text(app.width/1.2, app.height/10, text = f'Round: {app.round}/10', fill = 'white', font = 'Arial 17')

    #Essentially a 'replay' button
    canvas.create_rectangle(app.width/3, app.height/1.3, app.width/1.5, app.height/1.16, fill = 'green', outline = 'black')

    #Chooses what (essentially) 'replay' button to display based off of mode picked from homescreen/main menu
    if app.previousModeWasStandardIdentifyer == False:
        canvas.create_text(app.width/2, app.height/1.225, text = 'Next Round', fill = 'white', font = 'Arial 17')
    else:
        canvas.create_text(app.width/2, app.height/1.225, text = 'Identify Again', fill = 'white', font = 'Arial 17')

    #Homescreen/Main Menu button
    canvas.create_rectangle(app.width/3, app.height/1.55, app.width/1.5, app.height/1.355, fill = 'green', outline = 'black')

    canvas.create_text(app.width/2, app.height/1.45, text = 'Main Menu', fill = 'white', font = 'Arial 17')

    # show similar songs option only for normal song identifyer mode
    #if app.previousModeWasStandardIdentifyer:

        #Show similar songs
        #canvas.create_rectangle(app.width/3, app.height/1.12, app.width/1.5, app.height/1.02, fill = 'green', outline = 'black')

        #canvas.create_text(app.width/2, app.height/1.065, text = 'Show Next Similar Song', fill = 'white', font = 'Arial 17')


#if the buttons on the showSong/result screen are pressed
def showSong_mousePressed(app, event):
    getWord(app)
    currentX, currentY = event.x, event.y
    

    #This button starts a new game or song identifyer
    showSongTopX = app.width/3
    showSongTopY = app.height/1.3
    showSongBottomX = app.width/1.5
    showSongBottomY = app.height/1.15

    if (showSongBottomX > currentX > showSongTopX and showSongBottomY > currentY > showSongTopY):

        if app.previousModeWasStandardIdentifyer == False:
            app.mode = 'gamePlay'
            app.round += 1

            if app.round >= 11:
                app.mode = 'gameOver'
            
        else:
            app.mode = 'normalSongIdentifyer'

    #This button takes you to the homescreen/main menu
    showSongMenuTopX = app.width/1.5
    showSongMenuTopY = app.height/1.365
    showSongMenuBottomX = app.width/3
    showSongMenuBottomY = app.height/1.55

    if (showSongMenuBottomX < currentX < showSongMenuTopX and showSongMenuBottomY < currentY < showSongMenuTopY):

            app.mode = 'homescreen'
            app.round = 0
            app.points = 0

#########################################################################################################################
#noSongDetected (i.e. no lyrics were detected)
#########################################################################################################################


def noSongDetected_redrawAll(app, canvas):

    #Backdrop
    canvas.create_rectangle(0, 0, app.width, app.height, fill='black')  

    # show points/rounds only for game mode
    if app.previousModeWasStandardIdentifyer == False:

        canvas.create_text(app.width/6, app.height/10, text = f'Score: {app.points}', fill = 'white', font = 'Arial 17')

        canvas.create_text(app.width/1.2, app.height/10, text = f'Round: {app.round}/10', fill = 'white', font = 'Arial 17')

    canvas.create_text(app.width/2, app.height/2, text="No song detected :(", fill='white', font='Arial 26')

    #Essentially a 'replay' button
    canvas.create_rectangle(app.width/3, app.height/1.3, app.width/1.5, app.height/1.15, fill = 'green', outline = 'black')

    #Chooses what (essentially) 'replay' button to display based off of mode picked from homescreen/main menu
    if app.previousModeWasStandardIdentifyer == False:
        canvas.create_text(app.width/2, app.height/1.225, text = 'Next Round', fill = 'white', font = 'Arial 17')
    else:
        canvas.create_text(app.width/2, app.height/1.225, text = 'Identify Again', fill = 'white', font = 'Arial 17')

    #Homescreen/Main Menu button
    canvas.create_rectangle(app.width/3, app.height/1.55, app.width/1.5, app.height/1.365, fill = 'green', outline = 'black')
    
    canvas.create_text(app.width/2, app.height/1.45, text = 'Main Menu', fill = 'white', font = 'Arial 17')

def noSongDetected_mousePressed(app, event):
    getWord(app)
    currentX, currentY = event.x, event.y

    #This button starts a new game or song identifyer
    noSoundTopX = app.width/3
    noSoundTopY = app.height/1.3
    noSoundBottomX = app.width/1.5
    noSoundBottomY = app.height/1.15

    if (noSoundBottomX > currentX > noSoundTopX and
            noSoundBottomY > currentY > noSoundTopY):
        if app.previousModeWasStandardIdentifyer == False:
            app.mode = 'gamePlay'
            app.round += 1

            if app.round >= 11:
                app.mode = 'gameOver'

        else:
            app.mode = 'normalSongIdentifyer'

    #This button takes you to the homescreen/main menu
    noSoundMenuTopX = app.width/1.5
    noSoundMenuTopY = app.height/1.365
    noSoundMenuBottomX = app.width/3
    noSoundMenuBottomY = app.height/1.55

    if (noSoundMenuBottomX < currentX < noSoundMenuTopX and
            noSoundMenuBottomY < currentY < noSoundMenuTopY):

            app.mode = 'homescreen'
            app.round = 0
            app.points = 0


#########################################################################################################################
#normalSong Screen
#########################################################################################################################

#draws normalSongIdentifyer screen
def normalSongIdentifyer_redrawAll(app, canvas):

    #Backdrop
    canvas.create_rectangle(0, 0, app.width, app.height, fill='black') 

    canvas.create_text(app.width/2, app.height/2.5, text="Sing some lyrics!", fill='white', font='Arial 30')

    canvas.create_text(app.width/2, app.height/2, text= 'You have 10 seconds!', fill='white', font='Arial 20')  # onscreen text

#Gets song lyrics via the speech-to-text algorithm once the screen successfully drew the normalSongIdentifyer screen
def normalSongIdentifyer_timerFired(app):
    if app.mode == 'normalSongIdentifyer':
        app.previousModeWasStandardIdentifyer = True
        getSongLyricsFromSpeech(app)


#########################################################################################################################
#gameOver Screen
#########################################################################################################################

#draws gameOver screen
def gameOver_redrawAll(app, canvas):

    #Backdrop
    canvas.create_rectangle(0, 0, app.width, app.height, fill='black') 

    canvas.create_text(app.width/2, app.height/2.5, text="Game Over!", fill='white', font='Arial 30')

    canvas.create_text(app.width/2, app.height/2, text= f'Points: {app.points}', fill='white', font='Arial 20')  # onscreen text

    #Homescreen/Main Menu button
    canvas.create_rectangle(app.width/3, app.height/1.55, app.width/1.5, app.height/1.365, fill = 'green', outline = 'black')
    
    canvas.create_text(app.width/2, app.height/1.45, text = 'Main Menu', fill = 'white', font = 'Arial 17')



def gameOver_mousePressed(app, event):
    getWord(app)
    currentX, currentY = event.x, event.y

    #This button takes you to the homescreen/main menu
    noSoundMenuTopX = app.width/1.5
    noSoundMenuTopY = app.height/1.365
    noSoundMenuBottomX = app.width/3
    noSoundMenuBottomY = app.height/1.55

    if (noSoundMenuBottomX < currentX < noSoundMenuTopX and
            noSoundMenuBottomY < currentY < noSoundMenuTopY):

            app.mode = 'homescreen'
            app.round = 0
            app.points = 0
#########################################################################################################################
#runApp
#########################################################################################################################

runApp(width=1300, height=615)


