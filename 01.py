from struct import pack
from tkinter import *
import tkinter.messagebox
from cv2 import reprojectImageTo3D
from matplotlib.pyplot import text
from pyexpat import model
from tkinter import Frame
import cv2
from matplotlib.patches import Polygon
from sklearn.preprocessing import scale
from playsound import playsound
import pyttsx3
import numpy as np
import mysql.connector
import tkinter  as tk 
from tkinter import *
import datetime
import os



engine = pyttsx3.init()

def login():
    global root2
    root2 = Toplevel(root)
    root2.title("Login page")
    root2.geometry("450x300")
    root2.config(bg="white")

    global username_verification
    global password_verification
    Label(root2, text='Please Enter your Username and Password', bd=5,font=('arial', 12, 'bold'), relief="groove", fg="black",
                   bg="white",width=300).pack()
    username_verification = StringVar()
    password_verification = StringVar()
    Label(root2, text="").pack()
    Label(root2, text="Username :", fg="black", font=('arial', 12, 'bold')).pack()
    Entry(root2, text="admin").pack()
    Label(root2, text="").pack()
    Label(root2, text="Password :", fg="black", font=('arial', 12, 'bold')).pack()
    Entry(root2, text="", show="*").pack()
    Label(root2, text="").pack()
    Button(root2, text="Login", bg="black", fg='white', relief="groove", font=('arial', 12, 'bold') ,command=next).pack()
    Label(root2, text="")

def logged_destroy():
    logged_message.destroy()
    root2.destroy()

def failed_destroy():
    failed_message.destroy()

def next():
    global root3
    root3 = Toplevel(root2)
    root3.title("Detected page ")
    root3.geometry("450x300")
    root3.config(bg="white")
    Button(root3,text='Trase Object', height="1",width="20", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="black",
                   bg="white",command=trass).pack()
    Label(root3,text="").pack()
    Button(root3,text='Detected Age', height="1",width="20", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="black",
                   bg="white",command=age).pack()
    Label(root3,text="").pack()
    Button(root3,text='Detected Gender', height="1",width="20", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="black",
                   bg="white",).pack()
    Label(root3,text="").pack()
    Button(root3,text='Detected Age and Gender', height="1",width="20", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="black",
                   bg="white",).pack()
    Label(root3,text="").pack()


def age():
   os.system('age.py')

#def gender():
   # os.system('gender.py')

#def detection():
    #os.system('detection.py')


def trass():
    net =cv2.dnn.readNet("dnn_model/yolov4-tiny.weights","dnn_model/yolov4-tiny.cfg")
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(320,320),scale=1/255)

    
    classes=[]
    with open("dnn_model/classes.txt","r") as file_object:
     for class_name in file_object.readlines():
        class_name = class_name.strip()
        classes.append(class_name)
        

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,300)

    while True:
        ret,frame= cap.read()

        (class_ids,scores,bboxes)=model.detect(frame)
        for class_id,scores,bbox in zip(class_ids,scores,bboxes):
           x,y,w,h =bbox
           class_name = classes[class_id]
           cv2.putText(frame,class_name,(x,y-10),cv2.FONT_HERSHEY_PLAIN,2,(200,0,50),2)
           cv2.rectangle(frame,(x,y),(x + w,y + h),(200,0,50,),3)

           if(class_name):
               print("Object Name:-",class_name)
               engine.say("this is a"+class_name)
               time_date = datetime.datetime.now()
              
               print (time_date.strftime("Current date and time : %H:%M %d-%M-%Y"))

               if class_name:
                   my_connect = mysql.connector.connect(
                   host="localhost",
                   user="root", 
                   passwd="Bhushan@123",
                   database="detection"
               )
                   my_conn = my_connect.cursor()
                   try:
                       my_conn.execute("insert into object values('%s','%s');"%(class_name,time_date))
                       my_connect.commit()
                   except:
                       print("not intrested")

               engine.runAndWait() 

                    
            

           elif(class_name):
                  print("object is not detected")

           else:
            print("________________")
        cv2.imshow("Object Detection",frame)
        cv2.waitKey(1)


#def age():
    
   # my_w = Toplevel(root3)
    #my_w.title("View page")
   # my_w.geometry("450x300")
   # my_connect = mysql.connector.connect(
   # host="localhost",
   # user="root", 
   # passwd="root",
   # database="detection"
   # )
   # my_conn = my_connect.cursor()
   # my_conn.execute("SELECT * FROM object limit 0,100")
   # i=0 
   # for object in my_conn: 
   #     for j in range(len(object)):
   #         e = Label(my_w,width=20, text=object[j])
   #         e.grid(row=i, column=j)
   #     i=i+2
   # my_w.mainloop()



   


def logged():
    global logged_message
    logged_message = Toplevel(root2)
    logged_message.title("Welcome")
    logged_message.geometry("500x100")
    Label(logged_message, text="Login Successfully!... Welcome {} ".format(username_verification.get()), fg="green", font="bold").pack()
    Label(logged_message, text="").pack()
    Button(logged_message, text="Logout", bg="black", fg='white', relief="groove", font=('arial', 12, 'bold'), command=logged_destroy).pack()


def failed():
    global failed_message
    failed_message = Toplevel(root2)
    failed_message.title("Invalid Message")
    failed_message.geometry("500x100")
    Label(failed_message, text="Invalid Username or Password", fg="red", font="bold").pack()
    Label(failed_message, text="").pack()
    Button(failed_message,text="Ok", bg="black", fg='white', relief="groove", font=('arial', 12, 'bold'), command=failed_destroy).pack()




def Exit():
    wayOut = tkinter.messagebox.askyesno("Login System", "Do you want to exit the system")
    if wayOut > 0:
        root.destroy()
        return

def main_display():
    global root
    root = Tk()
    root.config(bg="white")
    root.title("Login System")
    root.geometry("500x500")
    Label(root,text='Welcome to The Detector',  bd=20, font=('arial', 20, 'bold'), relief="groove", fg="black",
                   bg="white",width=300).pack()
    Label(root,text="").pack()
    Button(root,text='Log In', height="1",width="20", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="black",
                   bg="white",command=login).pack()
    Label(root,text="").pack()
    Button(root,text='Exit', height="1",width="20", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="black",
                   bg="white",command=Exit).pack()
    Label(root,text="").pack()

main_display()
root.mainloop()


