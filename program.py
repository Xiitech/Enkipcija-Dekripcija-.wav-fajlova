##### Autor: Mateja Radojičić #####

######################## Imports ########################
import sys,os
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import (QWidget,QApplication,QPushButton,
                             QVBoxLayout,QFileDialog,QHBoxLayout)
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np
import wave
import hashlib 
from scipy.io.wavfile import write 
import pygame   # +++
######################## End of Imports ########################
    
######################## Init ########################
pygame.mixer.pre_init(frequency=44100)
pygame.init()                                                     
pygame.mixer.init()
######################## End of Init ########################

class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.playsound = None                                     
        self.pause     = None                                     
        self.left = 100 
        self.top = 100
        self.title = 'Enkripcija/Dekripcija .wav fajlova'
        self.width = 660
        self.height = 600
        
        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.initUI()
        
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.canvas = PlotCanvas(self, width=6, height=2)
        self.canvas.move(80,90)
        
        self.canvasEnc = PlotCanvasEnc(self, width=6, height=2)
        self.canvasEnc.move(80,370)
        
        self.nameLabelTittle = QLabel(self)
        self.nameLabelTittle.setText('Enkripcija/Dekripcija .wav fajlova')
        self.nameLabelTittle.setStyleSheet("color: grey; font-size: 22px;font-family: Verdana Bold;")
        self.nameLabelTittle.move(20, 20)
        self.nameLabelTittle.resize(350, 40)

        self.song1 = QPushButton("Učitaj", self)
        self.song1.setStyleSheet("font-size: 15px;font-family: Verdana Bold;")
        self.song1.move(20,110)
        self.song1.resize(100,30)
        
        self.play_it = QPushButton("Pusti", self)
        self.play_it.setStyleSheet("background-color: green; color: white;font-size: 15px;font-family: Verdana Bold;")
        self.play_it.move(20,190)
        self.play_it.resize(100,30)
        
        self.pause = QPushButton("Pauziraj", self)
        self.pause.setStyleSheet("font-size: 15px;font-family: Verdana Bold;")
        self.pause.move(20,240)
        self.pause.resize(100,30)
        
        self.save = QPushButton("Sačuvaj", self)
        self.save.setStyleSheet("font-size: 15px;font-family: Verdana Bold;")
        self.save.move(20,390)
        self.save.resize(100,30)
        
        self.play_itEnc = QPushButton("Pusti", self)
        self.play_itEnc.setStyleSheet("background-color: green; color: white;font-size: 15px;font-family: Verdana Bold;")
        self.play_itEnc.move(20,470)
        self.play_itEnc.resize(100,30)
        
        self.pauseEnc = QPushButton("Pauziraj", self)
        self.pauseEnc.setStyleSheet("font-size: 15px;font-family: Verdana Bold;")
        self.pauseEnc.move(20,520)
        self.pauseEnc.resize(100,30)
        
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Šifra:')
        self.nameLabel.setStyleSheet("font-size: 15px;font-family: Verdana Bold;")
        self.nameLabel.move(180, 300)
        
        self.line = QLineEdit(self)  
        self.line.setStyleSheet("font-size: 15px;font-family: Verdana Bold;")
        self.line.move(220, 300)
        self.line.resize(150, 30)
               
        self.encrypt = QPushButton("Enkriptuj", self)
        self.encrypt.setStyleSheet("background-color: blue; color: white;font-size: 15px;font-family: Verdana Bold;")
        self.encrypt.move(380,300)
        self.encrypt.resize(100,30)
        
        self.decrypt = QPushButton("Dekriptuj", self)
        self.decrypt.setStyleSheet("background-color: blue; color: white;font-size: 15px;font-family: Verdana Bold;")
        self.decrypt.move(490,300)
        self.decrypt.resize(100,30)
        
        h_box = QHBoxLayout()
        h_box.addWidget(self.song1)
        h_box.addWidget(self.play_it)
        h_box.addWidget(self.pause)
        h_box.addWidget(self.encrypt) 
        h_box.addWidget(self.decrypt) 
        h_box.addWidget(self.save)        
        h_box.addWidget(self.play_itEnc)
        h_box.addWidget(self.pauseEnc)
        v_box = QVBoxLayout()
        v_box.addLayout(h_box)
        self.setLayout(v_box)
        self.setWindowTitle("Enkripcija")

        self.song1.clicked.connect(self.song1_open)
        self.pause.clicked.connect(self.pause_the_songs)            
        self.play_it.clicked.connect(self.play_the_songs)
        self.encrypt.clicked.connect(self.encrypt_songs)
        self.decrypt.clicked.connect(self.decrypt_songs)
        self.save.clicked.connect(self.save_the_songs)
        self.play_itEnc.clicked.connect(self.play_the_songsEnc)
        self.pauseEnc.clicked.connect(self.pause_the_songsEnc)                   

        self.show()
 
    def pause_the_songs(self):
        if self.playsound is None:
            self.pause.setText("UnPause")
            self.playsound = "pause"
            pygame.mixer.music.pause()
        else:
            self.pause.setText("Pause")
            self.playsound = None  
            pygame.mixer.music.unpause()    
        
    def song1_open(self):
        file_name = QFileDialog.getOpenFileName(self,"Open",os.getenv("HOME"))
        self.data1 = file_name[0]
        musicfile = pygame.mixer.Sound(self.data1)
        frames = pygame.sndarray.samples(musicfile)[:]
        self.canvas.plot(frames)
        
    def play_the_songs(self):                                     
        self.playsound = pygame.mixer.init() 
        
        musicfile = pygame.mixer.Sound(self.data1)
        frames = pygame.sndarray.samples(musicfile)[:]
        #sound = pygame.sndarray.make_sound(frames)
        #sound.play()
        pygame.mixer.music.load(self.data1)
        pygame.mixer.music.play()
                
    def encrypt_songs(self):                                     
        spf = wave.open(self.data1,'r')
        signal = spf.readframes(-1)
        self.frames = np.fromstring(signal, 'Int16')

        for i in range(len(self.frames)):
            var = self.line.text() + str(i)
            x = hashlib.sha256(var.encode('ascii')).hexdigest()
            self.frames[i] = (int(self.frames[i]) + ((int(x[:4], 16))))

        self.canvasEnc.plot(self.frames)        
        write('output.wav', 96000,  self.frames)

    def decrypt_songs(self):                                     
        spf = wave.open(self.data1,'r')
        signal = spf.readframes(-1)
        
        self.frames = np.fromstring(signal, 'Int16')
        for i in range(len(self.frames)):
            var = self.line.text() + str(i)
            x = hashlib.sha256(var.encode('ascii')).hexdigest()
            self.frames[i] = (int(self.frames[i]) - ((int(x[:4], 16))))

        self.canvasEnc.plot(self.frames)        
        write('output.wav', 96000,  self.frames)
        
    def save_the_songs(self):  
        formats = "WAV (*.wav)"
        output_file = QFileDialog.getSaveFileName(self, "Save", "", formats)
        write(output_file[0], 96000,  self.frames)
        
    def play_the_songsEnc(self):                                     
        self.playsound = pygame.mixer.init() 
        pygame.mixer.music.load('output.wav')
        pygame.mixer.music.play()
                
    def pause_the_songsEnc(self):                                     
        print(self.frames)
        if self.playsound is None:
            self.pauseEnc.setText("UnPause")
            self.playsound = "pause"
            pygame.mixer.music.pause()
        else:
            self.pauseEnc.setText("Pause")
            self.playsound = None  
            pygame.mixer.music.unpause()   

class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=14, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(25)
 
    def plot(self,X):
        ax = self.figure.add_subplot(111)
        ax.cla()
        ax.plot(X,'C2')
        ax.set_title('Učitan .wav fajl')
        ax.spines['top'].set_visible(1.5)
        ax.spines['right'].set_visible(1.5)
        ax.spines['bottom'].set_visible(1.5)
        ax.spines['left'].set_visible(1.5)
        ax.axes.get_xaxis().set_ticks([])
        ax.axes.get_yaxis().set_ticks([])
        plt.rcParams['axes.linewidth'] = 0.1 
        self.draw()
        
class PlotCanvasEnc(FigureCanvas):
 
    def __init__(self, parent=None, width=14, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(25)
  
    def plot(self,Y):
        ax = self.figure.add_subplot(111)
        ax.cla()
        ax.plot(Y,'C2')
        ax.set_title('Enkriptovan/Dekriptovan .wav fajl')
        ax.spines['top'].set_visible(1.5)
        ax.spines['right'].set_visible(1.5)
        ax.spines['bottom'].set_visible(1.5)
        ax.spines['left'].set_visible(1.5)
        ax.axes.get_xaxis().set_ticks([])
        ax.axes.get_yaxis().set_ticks([])
        plt.rcParams['axes.linewidth'] = 0.1 
        self.draw()
                             
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())