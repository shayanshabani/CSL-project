import cv2 as cv2
import face_recognition as fr
import base64
import cv2
import zmq
import simple_facerec

def streamVideo(cap,sfr,footage_socket):
    try:
        ret, frame = cap.read()
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            top, right, bottom, left = face_loc
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)
            cv2.putText(frame, name, (left, top), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 2)
        frame = cv2.resize(frame, (640, 480))  # resize the frame
        encoded, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        footage_socket.send(jpg_as_text)

    except Exception as e:
        cap.release()
        cv2.destroyAllWindows()



def zangBokhor(mode,frame,sfr):
    print(mode)
    print("mode---")
    face_locations, face_names = sfr.detect_known_faces(frame)
    if mode == 2:
        # open door, send name or picture
        cv2.imwrite('man.png',frame)
        sendPicmail()
        if face_names is None or len(face_names) == 0:
            return False
        for name in face_names:
            if(name != "Unknown"):
                print("open door")
                return True
        return False
    elif mode == 1:
        cv2.imwrite('man.png',frame)
        sendPicmail()
        return False
        # send picture dont open door
    elif mode == 0:
        if face_names is None or len(face_names) == 0:
            print("who's this?")
            return False
        for name in face_names:
            if(name != "Unknown"):
                print("open door")
                return True
        return False


    print("alale")
    return False
    # cap.release()
    # cv2.destroyAllWindows()

#import os
#from email.message import EmailMessage
#import ssl
#import smtplib
def sendEmail(name):
    gmail_user = 'parhamix@gmail.com'
    gmail_password = 'lrbrdjqysugsevcd'

    sent_from = gmail_user
    to = ['parhamix@gmail.com']
    subject = 'Lorem ipsum dolor sit amet'
    body = name

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(sent_from, to, email_text)
    smtp_server.close()
    print("Email sent successfully!")
    
    
    
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def sendPicmail():
    fromaddr = "parhamix@gmail.com"
    toaddr = "parhamix@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Subject of the Mail"
    body ="This dude is at your door"
    msg.attach(MIMEText(body, 'plain'))
    filename = "man.png"
    attachment = open("man.png", "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "jsmhphltpdjgzxvb")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
