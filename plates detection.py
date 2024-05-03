#!/usr/bin/python
# -*- coding: utf-8 -*-


import numpy as np
import sys
if "Tkinter" not in sys.modules:
    from tkinter import *
from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename
from tkinter import filedialog, ttk
import cv2
import os
import tkinter as tk
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import pickle
import time
import subprocess
from subprocess import Popen
import argparse
import mysql.connector
import sqlite3

#import face_recognition



from subprocess import Popen,PIPE,STDOUT,call

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str,
	help="path to output video")
ap.add_argument("-y", "--display", type=int, default=1,
	help="whether or not to display output frame to screen")
args = vars(ap.parse_args())

#data = pickle.loads(open('C:\\Python_CV\\Python37\\FACE_RECOGNITION_PROJECTS\\In a Live VideoPicture\\face-recognition-opencv\\encodings.pickle', "rb").read())

class Test():

    def __init__(self):
        
        self.root = Tk()
        self.root.title('VEHICLE NUMBER PLATE RECOGINITION SYSTEM')
        self.root.geometry('850x567+0+0')
        #self.root.attributes("-fullscreen", True)


    
        def get_data():
            
            
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                port="3306",
                password="ASA#60kjk_@",
                database="v_prj"
            ) 
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM number_plate order by id desc limit 20")
            myresult = mycursor.fetchall()
            
        #     # # Create a popup window to display data
            top0 = tk.Toplevel()
            top0.title("Number Plates Database")
            top0.geometry("400x300+440+200")
            
        #    # Create a treeview widget
           # Create a treeview widget
            tree = ttk.Treeview(top0)
            tree["columns"] = ("numberplate", "timestamp")
            tree.heading("#0", text="ID")
            tree.heading("numberplate", text="Number Plate")
            tree.heading("timestamp", text="Timestamp")
            tree.pack(expand=True, fill=tk.BOTH)

            tree.column("#0", width=50)  # Adjust the width of the ID column
            tree.pack(expand=True, fill=tk.BOTH)

        #     # Insert data into the treeview
            for i, row in enumerate(myresult, start=1):
                tree.insert("", "end", text=row[0], values=(row[1], row[2]))

        #     # Update the width of the numberplate and timestamp columns
            tree.column("numberplate", width=150)  # Adjust width as needed
            tree.column("timestamp", width=150)  # Adjust width as needed
 # this want to share with her and above get data 
        def clear_data():
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    port="3306",
                    password="ASA#60kjk_@",
                    database="v_prj"
                )
                mycursor = mydb.cursor()
                mycursor.execute("DELETE FROM number_plate")
                mydb.commit()
                print("Data cleared successfully!")
            except mysql.connector.Error as error:
                print("Error clearing data:", error)
            finally:
                if mydb.is_connected():
                    mycursor.close()
                    mydb.close()
            




        def select_image():

            name = askopenfilename(initialdir="C:/Users/NITIN/Documents/Vehicle-Plate-Recognition-main/back.png",filetypes =(("Image File", "*.jpg"),("All Files","*.*")),title = "Choose a file.")

            image = cv2.imread(name)

            print(name)
            top0 = tk.Toplevel()
            top0.title("Number Plate Extracted")
            top0.geometry("300x150+440+200")
            small = Canvas(top0, bg="white", height=150, width=300)
            small.pack()

            
            small.create_text(52,12, text="Plates Database", font=('Times New Roman', '20', 'bold italic'), fill="black", anchor='nw')

            apna = "alpr "+name+ " --c pk -n 1"

            proc=Popen(apna, stdout=PIPE, shell=True)
            output=proc.communicate()[0]
            b = (str(output))


            plate= (b[29:35])

            
            plate = (plate.replace("\\",""))

            print(plate)
            
            mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            port="3306",
            password="ASA#60kjk_@",
            database="v_prj"
            )
            # from datetime import datetime
            # now = datetime.now()  
            # datetime = now.strftime("%Y-%m-d %H:%M:%S")

            from datetime import datetime

            datetime = datetime.now()
 
            # print(mydb)
            # INSERT INTO `v_prj`.`number_plate` (`id`, `numberplate`, `timestamp`) VALUES ('', 'hjgf', 'kjhg');
            mycursor = mydb.cursor() 
            sql = "INSERT INTO number_plate(`numberplate`, `timestamp`) VALUES (%s, %s)"
            val = ( plate, datetime)
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")


            small.create_text(90,60, text=plate, font=('Times New Roman', '28', 'bold underline'), fill="black", anchor='nw')

            


            

            
        def about():
            top = tk.Toplevel()
            top.title("Guidance For Execution")
            top.geometry("400x200+180+200")
            t_lbl = tk.Label(top, text="\n\n1. Select the Image and wait for process...")
            t_lbl.pack()


            t_lbl2 = tk.Label(top, text="\n\n2. Select the Video and wait for process...")
            t_lbl2.pack()


            t_lbl3 = tk.Label(top, text="\n\n3. For Real TIme Video Connect Webcam ...")
            t_lbl3.pack()

        
        def live_cam():
            frameWidth = 640    # Frame Width
            frameHeight = 480   # Frame Height

            plateCascade = cv2.CascadeClassifier("C:/Users/NITIN/Documents/platespotter-1/haarcascade_russian_plate_number.xml")
            minArea = 500

            cap = cv2.VideoCapture(0)
            cap.set(3, frameWidth)
            cap.set(4, frameHeight)
            cap.set(10, 150)
            count = 0
            while True:
                success, img = cap.read()
                if not success:
                   print("Failed to read frame")
                   break

                imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                numberPlates = plateCascade.detectMultiScale(imgGray, 1.1, 4)
                for (x, y, w, h) in numberPlates:
                    area = w * h
                    if area > minArea:
                       cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                       cv2.putText(img, "NumberPlate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                       imgRoi = img[y:y + h, x:x + w]
                       cv2.imshow("ROI", imgRoi)

                cv2.imshow("Result", img)
                key = cv2.waitKey(1)
                if key == ord('q'):  # Press 'q' to quit
                    break
                elif key == ord('s'):  # Press 's' to save the plate
                      cv2.imwrite("plates/scaned_img_" + str(count) + ".jpg", imgRoi)
                      cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
                      cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
                      cv2.imshow("Results", img)
                      cv2.waitKey(500)
                      count += 1
            cap.release()
            cv2.destroyAllWindows()     
        
        C = Canvas(self.root, bg="blue", height=850, width=567)
        filename = PhotoImage(file = "C:/Users/NITIN/Documents/Vehicle-Plate-Recognition-main/back.png")
        C.create_image(0, 0, image=filename, anchor='nw')

        

        C.create_text(285,50, text="PLATESPOTTER", font=('ALGERIAN', '35', 'bold'), fill="white")
        C.pack(fill=BOTH, expand=1)




        # button1 = Button(C, text = "Saved Execute", font=('Times', '14', 'bold italic'), borderwidth=4, highlightthickness=4, highlightcolor="#37d3ff", highlightbackground="#37d3ff",relief=RAISED,command=Camera)
        # button1.configure(width=15, activebackground = "#33B5E5")
        # button1.place(x=180, y=100)


        button2 = Button(C, text = "Image Analysis", font=('Times', '14', 'bold italic'), borderwidth=4, highlightthickness=4, highlightcolor="#37d3ff", highlightbackground="#37d3ff",relief=RAISED, command =select_image)
        button2.configure(width=15, activebackground = "#33B5E5")
        button2.place(x=50, y=100) 
        
        
        button3 = Button(C, text = "View Data", font=('Times', '14', 'bold italic'),borderwidth=4, highlightthickness=4, highlightcolor="#37d3ff", highlightbackground="#37d3ff",relief=RAISED, command =get_data)
        button3.configure(width=15, activebackground = "#33B5E5")
        button3.place(x=250, y=460)

      

        # button3 = Button(C, text = "Webcam Video", font=('Times', '14', 'bold italic'),borderwidth=4, highlightthickness=4, highlightcolor="#37d3ff", highlightbackground="#37d3ff",relief=RAISED, command =live_cam)
        # button3.configure(width=15, activebackground = "#33B5E5")
        # button3.place(x=180, y=260)


        # button4 = Button(C, text = "App Details", font=('Times', '14', 'bold italic'), borderwidth=4, highlightthickness=4, highlightcolor="#37d3ff", highlightbackground="#37d3ff",relief=RAISED, command =about)
        # button4.configure(width=15, activebackground = "#33B5E5")
        # button4.place(x=180, y=340)

        button5 = Button(C, text = "Closing All", font=('Times', '14', 'bold italic'), borderwidth=4, highlightthickness=4, highlightcolor="#37d3ff", highlightbackground="#37d3ff",relief=RAISED, command=self.quit)
        button5.configure(width=15, activebackground = "#33B5E5")
        button5.place(x=500, y=460)

        button6 = Button(C, text = "Webcam Video", font=('Times', '14', 'bold italic'),borderwidth=4, highlightthickness=4, highlightcolor="#37d3ff", highlightbackground="#37d3ff",relief=RAISED, command =live_cam)
        button6.configure(width=15, activebackground = "#33B5E5")
        button6.place(x=350, y=100)

##
##        self.about = Button(C, text="Saved Video Execution", width="30",font=('Helvetica', '12', 'italic'), command=Camera)
##        self.about.pack(padx=5, pady=40)
##
##        self.about_1 = Button(C, text="Image Analysis", width="30", font=('Helvetica', '12', 'italic'), command=select_image)
##        self.about_1.pack(padx=5, pady=45)
##
##        self.about = Button(C, text="Live Webcam Video", width="30",font=('Helvetica', '12', 'italic'), command=live_cam)
##        self.about.pack(padx=5, pady=50)
##
##        self.about = Button(C, text="About Application", width="30", font=('Helvetica', '12', 'italic'),command=about)
##        self.about.pack(padx=5, pady=55)
##
##        good = Button(C, text="Closing the Window", width="30",font=('Helvetica', '12', 'italic'), command=self.quit)
##        good.pack(padx=5, pady=60)

        self.root.mainloop()

    def quit(self):
        self.root.destroy()


app = Test()






