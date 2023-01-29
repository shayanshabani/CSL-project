import base64
import socket
import time
##import RPi.GPIO as GPIO
import cv2
import zmq
import face_recognition as fr
import simple_facerec
import threading
from Controller import zangBokhor,streamVideo
global mode
mode = 0 # 0 = child, 1 = auto open, 2= no one home
from tkinter import Tk
from PIL import Image
from tkinter.filedialog import askopenfilename
# socket init
context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://localhost:5555')
global frame
global updating
updating = False
#########################
#server client text
import socket
global server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 12347))
server.listen(5)
#
#########################
global cap
cap = cv2.VideoCapture("http://172.20.10.6:8080/video")  # init the camera
cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
global sfr
sfr = simple_facerec.SimpleFacerec()
sfr.load_encoding_images("images/")

global stream
stream = True
###########
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzer = 23
led1 = 26
led2 = 13
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)
pushButton = 12
GPIO.setup(pushButton,GPIO.IN, pull_up_down=GPIO.PUD_UP)
L1 = 24
C1 = 22
C2 = 27
C3 = 4
C4 = 25
GPIO.setup(L1,GPIO.OUT)
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
def keypadCallback(channel):
    global mode
    if channel == C1:
        mode = 0
    elif channel == C4:
        mode = 1
    elif channel == C3:
        mode = 2
    print(mode)
GPIO.add_event_detect(C1, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C4, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C3, GPIO.RISING, callback=keypadCallback)

#########

###### input client app sockets######
# inputSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def zangSound():
    GPIO.output(buzzer,GPIO.HIGH) 
    time.sleep(0.5)
    GPIO.output(buzzer,GPIO.LOW)



def inputSocketThread(socket,cap):
    socket.connect(('127.0.0.1',12367))
    print("connected")
    while True:
        try:
            received = socket.recv(1024)
            name_input = received.decode()
            if name_input is not None and name_input != "":
                ret,frame = cap.read()
                cv2.imwrite("images/" + name_input + ".png", frame)
                global stream
                stream = False
                sfr = simple_facerec.SimpleFacerec()
                sfr.load_encoding_images("images/")
                stream = True
                thread1 = threading.Thread(target=stream_video_loop, args=(cap, sfr, footage_socket))
                thread1.start()
        except:
            print("error")
            time.sleep(10)
            inputSocketThread(socket,cap)
            break


###########
def stream_video_loop(cap,sfr,footage_socket):
    while stream:
        streamVideo(cap,sfr,footage_socket)
        time.sleep(0.5)
        
def getIncl():
    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address}")
        data = client_socket.recv(1024).decode()
        global cap
        global frame
        namedata = f"images/{data}.jpg"
        cv2.imwrite(namedata,frame)
        global sfr
        global updating
        updating = False
        sfr = simple_facerec.SimpleFacerec()
        sfr.load_encoding_images("images/")
        updating = True
        client_socket.sendall(b"ACK")
        client_socket.close()

thread1 = threading.Thread(target=getIncl)


def inputi(ccc,footage_socket):
    GPIO.setmode(GPIO.BCM)
    while True:
        ##doInputChar(L1)
        global frame
        global updating
        if not updating:
            ret, frame = cap.read()
        a="k"
        if GPIO.input(12) == False:
            global mode
            global sfr
            known = zangBokhor(mode,frame,sfr)
            GPIO.output(buzzer,GPIO.HIGH)
            if known:
                GPIO.output(led1,GPIO.HIGH)
            else:
                GPIO.output(led2,GPIO.HIGH)
            time.sleep(0.5)
            if known:
                GPIO.output(led1,GPIO.LOW)
            else:
                GPIO.output(led2,GPIO.LOW)
            GPIO.output(buzzer,GPIO.LOW)   
        
ccc=5
thread2 = threading.Thread(target=inputi,args=(ccc,footage_socket))

#thread3 = threading.Thread(target=inputSocketThread,args=(inputSocket,cap))
thread1.start()
thread2.start()
thread1.join()
thread2.join()
GPIO.output(L1,GPIO.LOW)
GPIO.cleanup()
#
# thread1.join()
# thread2.join()
#thread3.join()
# while True:
#         if 0>1:
#             zangBokhor(mode,cap,sfr)
#         # send video
#         streamVideo(cap,sfr,footage_socket)
#
#         if 0>1: # key pressed
#             mode = 1
#         if 2>5: # change pic key
#             Tk().withdraw()
#             filename = askopenfilename()
#             a = filename.split("/")[-1]
#             Image.open(filename).copy().save("images/"+a)

