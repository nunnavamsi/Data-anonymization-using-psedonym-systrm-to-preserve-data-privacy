from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import numpy as np
import os
import cv2
import scipy.spatial.distance as dist
import hmac
import hashlib 
import binascii
import ftplib

main = Tk()
main.title("Data Anonymization Using Pseudonym System to Preserve Data Privacy")
main.geometry("1300x1200")

global filename
ids = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']

def create_sha256_signature(key, message):
    byte_key = key
    message = message.encode()
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()

def upload():
    global filename
    text.delete('1.0', END)
    filename = askopenfilename(initialdir = "dataset")

def userRegister():
    username = tf1.get()
    message = tf2.get()
    text.delete('1.0', END)
    if len(username) > 0 and len(message) > 0:
        filename = askopenfilename(initialdir = "images")
        img = cv2.imread(filename)
        img_filter = cv2.GaussianBlur(img,(5,5),0)
        img_filter = cv2.medianBlur(img_filter,5)
        img_filter = cv2.cvtColor(img_filter, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=6.0, tileGridSize=(30,30))
        img_filter = clahe.apply(img_filter)
        img_filter = cv2.Canny(img_filter,10,120)
        cv2.imwrite("test.png",img_filter)
        img_filter = cv2.imread("test.png",0)
        gray = np.float32(img_filter)
        dst = cv2.cornerHarris(gray,2,3,0.20)
        dst = cv2.dilate(dst,None)
        img_filter = cv2.imread("test.png")
        img_filter[dst>0.20*dst.max()]=[0,255,0]
        temp1 = cv2.cvtColor(img_filter, cv2.COLOR_BGR2GRAY)
        temp2 = dst
        distance = dist.euclidean(temp1.flatten(), temp2.flatten())
        points = temp1[0:1,0:30]
        points = (points/255)[0]
        text.insert(END,"Binary Vector : "+str(points)+"\n")
        master_key = 0
        for i in range(len(points)):
            if points[i] == 1:
                master_key = master_key + pow(2, i)
        text.insert(END,"Master Key from Binary Vector : "+str(master_key)+"\n")
        user = username
        random_userid = ''
        for i in range(len(user)):
            ch = user[i]
            for j in range(len(ids)):
                if ids[j] == ch:
                    random_userid+=str(j)
            
        text.insert(END,"Random data from user ID : "+str(random_userid)+"\n")
        secret_key = str(master_key).encode()
        hmac = create_sha256_signature(secret_key,random_userid+str(points.ravel()[0]))
        text.insert(END,"Generated Pseudonym : "+str(hmac)+"\n")
        f = open(username+".txt", "w")
        f.write(hmac+","+message)
        f.close()
        print(hmac+","+message) 
        ftp = ftplib.FTP_TLS("ftp.drivehq.com")
        ftp.login("truprojects01", "Projects123@#")
        ftp.prot_p()
        file = open(username+".txt", "rb")
        ftp.storbinary("STOR "+username+".txt", file)
        file.close()
        ftp.close()
        
        os.remove(username+".txt")
        text.insert(END,"Pseudonym data stored at DRIVEHQ using filename as "+username+".txt\n")
        cv2.imshow("Image with Key Points",img_filter)
        cv2.waitKey(0)
        
def userRecognition():
    username = tf1.get()
    text.delete('1.0', END)
    if len(username) > 0:
        filename = askopenfilename(initialdir = "images")
        img = cv2.imread(filename)
        img_filter = cv2.GaussianBlur(img,(5,5),0)
        img_filter = cv2.medianBlur(img_filter,5)
        img_filter = cv2.cvtColor(img_filter, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=6.0, tileGridSize=(30,30))
        img_filter = clahe.apply(img_filter)
        img_filter = cv2.Canny(img_filter,10,120)
        cv2.imwrite("test.png",img_filter)
        img_filter = cv2.imread("test.png",0)
        gray = np.float32(img_filter)
        dst = cv2.cornerHarris(gray,2,3,0.20)
        dst = cv2.dilate(dst,None)
        img_filter = cv2.imread("test.png")
        img_filter[dst>0.20*dst.max()]=[0,255,0]
        temp1 = cv2.cvtColor(img_filter, cv2.COLOR_BGR2GRAY)
        temp2 = dst
        distance = dist.euclidean(temp1.flatten(), temp2.flatten())
        points = temp1[0:1,0:30]
        points = (points/255)[0]
        text.insert(END,"Binary Vector : "+str(points)+"\n")
        master_key = 0
        for i in range(len(points)):
            if points[i] == 1:
                master_key = master_key + pow(2, i)
        text.insert(END,"Master Key from Binary Vector : "+str(master_key)+"\n")
        user = username
        random_userid = ''
        for i in range(len(user)):
            ch = user[i]
            for j in range(len(ids)):
                if ids[j] == ch:
                    random_userid+=str(j)
            
        text.insert(END,"Random data from user ID : "+str(random_userid)+"\n")
        secret_key = str(master_key).encode()
        hmac = create_sha256_signature(secret_key,random_userid+str(points.ravel()[0]))
        try:
            ftp = ftplib.FTP_TLS("ftp.drivehq.com")
            ftp.login("truprojects01", "Projects123@#")
            #ftp.login("cloudfilestorageacademic", "Offenburg965#")
            ftp.prot_p()
            name = username+".txt"
            with open(name, 'wb' ) as file :
                ftp.retrbinary('RETR %s' % name, file.write)
            file.close()
            drive_data = ''
            with open(name, "r") as file:
                for line in file:
                    line = line.strip('\n')
                    line = line.strip()
                    drive_data+=line+" "
            file.close()
            os.remove(name)
            drive_data = drive_data.strip()
            arr = drive_data.split(",")
            if arr[0] == hmac:
                text.insert(END,"User recognized successfully\n")
                text.insert(END,"User Message : "+arr[1]+"\n\n")
            else:
                text.insert(END,"User Recognition Failed\n")
        except:
            text.delete('1.0', END)
            text.insert(END,"Username does not exists")

    
font = ('times', 15, 'bold')
title = Label(main, text='Data Anonymization Using Pseudonym System to Preserve Data Privacy')
title.config(bg='mint cream', fg='olive drab')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 14, 'bold')
ff = ('times', 12, 'bold')

l1 = Label(main, text='Username')
l1.config(font=font1)
l1.place(x=50,y=100)

tf1 = Entry(main,width=20)
tf1.config(font=font1)
tf1.place(x=230,y=100)

l2 = Label(main, text='Message')
l2.config(font=font1)
l2.place(x=50,y=150)

tf2 = Entry(main,width=40)
tf2.config(font=font1)
tf2.place(x=230,y=150)

registerButton = Button(main, text="Registration Module", command=userRegister)
registerButton.place(x=50,y=200)
registerButton.config(font=ff)

recognitionButton = Button(main, text="Recognition Module", command=userRecognition)
recognitionButton.place(x=350,y=200)
recognitionButton.config(font=ff)


font1 = ('times', 13, 'bold')
text=Text(main,height=15,width=100)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=250)
text.config(font=font1)

main.config(bg='gainsboro')
main.mainloop()
