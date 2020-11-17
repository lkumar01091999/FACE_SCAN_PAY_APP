# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 11:15:19 2020

@author: Mr. LOKESH
"""

import tkinter as tk
from tkinter import font
from functools import partial
import numpy as np
import cv2
import imutils
import threading
import face_recognition
from PIL import ImageTk, Image
import dlib
import os
import time
import sys

#-------------------------------------------------------------------------------------------------------------------------------------#
# SELF ASSUMED DATA FROM BANK WEBSITE
img_1 = face_recognition.load_image_file(os.path.abspath('sample_test_image.png'))
img_1_face_encodings = face_recognition.face_encodings(img_1)[0]

known_faces = [img_1_face_encodings]
phone_numbers=['9560449581']
names=['LOKESH KUMAR']
account_balances=[20000]

#-------------------------------------------------------------------------------------------------------------------------------------#
# Intialize face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor =dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

#video capturing.....
video_scan_cap = cv2.VideoCapture('scanned_testing_video.mp4')
# codec
codec = int(video_scan_cap.get(cv2.CAP_PROP_FOURCC))
fps = int(video_scan_cap.get(cv2.CAP_PROP_FPS))
frame_width = int(video_scan_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_height = int(video_scan_cap.get(cv2.CAP_PROP_FRAME_WIDTH))

#videowriter object
out = cv2.VideoWriter('output.mp4', codec, fps, (frame_width,frame_height))

#FONT
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

# Geometry for tkinter window
SETWIDTH = 650
SETHEIGHT = 507

#----------------------------------------------------------------------------------------------------------------------------------------#
# FUNCTIONS FOR LIVENESS ALGORITHM     
def midpoint(p1,p2):
    mid_x = int((p1.x+p2.x)/2)
    mid_y = int((p1.y+p2.y)/2)
    return mid_x,mid_y

def euclidean_distance(l_x,l_y,r_x,r_y):
    length = np.sqrt((l_x-r_x)**2+(l_y-r_y)**2)
    return length

def eye_aspect_ratio(eye_points,facial_landmarks,frame):
    #left point of eye
    left_point = [facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y]
    
    #right point of eye
    right_point = [facial_landmarks.part(eye_points[3]).x,facial_landmarks.part(eye_points[3]).y]
    
    # mid_top point of eye
    mid_top_point = midpoint(facial_landmarks.part(eye_points[1]),facial_landmarks.part(eye_points[2]))
    
    # mid bottom point of eye
    mid_bottom_point = midpoint(facial_landmarks.part(eye_points[5]),facial_landmarks.part(eye_points[4]))
    
    
    # DRAW HORIZONTAL AND VERTICAL LINES
    HL = cv2.line(frame,(left_point[0],left_point[1]),(right_point[0],right_point[1]),(0,0,255),1)
    VL = cv2.line(frame,(mid_top_point[0],mid_top_point[1]),(mid_bottom_point[0],mid_bottom_point[1]),(0,0,255),1)
    
    # calculate length OF HL AND VL
    H_LENGTH = euclidean_distance(left_point[0],left_point[1],right_point[0],right_point[1])
    V_LENGTH = euclidean_distance(mid_top_point[0],mid_top_point[1],mid_bottom_point[0],mid_bottom_point[1])
    
    # Finally calculating eye aspect ratio
    ear = V_LENGTH/H_LENGTH
    return ear

#----------------------------------------------------------------------------------------------------------------------------------------#
# This function is for identifying face match b/w system and scanned images
def img_matching_screen():
    print("MATCHING PROCESS STARTS...........")
    #screenshot taken from video
    single_captured_frame=screenshot
    canvas_1=tk.Canvas(APP_win,bg='white',width=SETWIDTH,height=348)
    canvas_1.grid(row=0,column=0,sticky=tk.NW)
    resized_single_captured_frame=imutils.resize(single_captured_frame,width=250,height=350)
    resized_single_captured_frame=ImageTk.PhotoImage(image=Image.fromarray(resized_single_captured_frame))
    canvas_1.image=resized_single_captured_frame
    canvas_1.create_image(485,185,image=resized_single_captured_frame)
    
    # image data from website
    canvas_2=tk.Canvas(APP_win,bg='white',width=SETWIDTH/2,height=348)
    canvas_2.grid(row=0,column=0,sticky=tk.NW)
    resized_img_1 = imutils.resize(img_1,width=250,height=350)
    resized_img_1=ImageTk.PhotoImage(image=Image.fromarray(resized_img_1))
    canvas_2.image=resized_img_1
    canvas_2.create_image(160,185,image=resized_img_1)
    
    canvas_3=tk.Canvas(APP_win,bg='white',width=SETWIDTH,height=100)
    canvas_3.grid(row=1,column=0,sticky=tk.W)
    match_identify=tk.PhotoImage(file='match_identify.png')
    canvas_3.create_image(0,0,ancho=tk.NW,image=match_identify)
    canvas_3.image=match_identify
    

    rgb_frame=single_captured_frame[:,:,::-1]
    
    facial_points = face_recognition.face_locations(rgb_frame, model='cnn')
    print(f'facial_points = {facial_points}')
    facial_encodings = face_recognition.face_encodings(rgb_frame,facial_points)
    facial_names = []
    
    for encoding in facial_encodings:
        matches = face_recognition.compare_faces(known_faces,encoding, tolerance=0.50)
        
        name=""
        for match in matches:
            if match:
                name=names[0]
                canvas_match=tk.Canvas(APP_win,width=SETWIDTH,height=100,bg='white')
                canvas_match.grid(row=1,column=0,sticky=tk.W)
                match_successful=tk.PhotoImage(file='match_successfully.png')
                canvas_match.create_image(0,0,ancho=tk.NW,image=match_successful)
                canvas_match.image=match_successful
                print("MATCHED SUCCESSFULLY")
        facial_names.append(name)
        print(facial_names)
    time.sleep(5)
    canvas_match.delete('all')
    return

#-----------------------------------------------------------------------------------------------------------------------------------------#
# This function is for submitting the details.
def submit(pay_var,phone_var):
    print(int(pay_var.get()))
    print(phone_var.get())
    if int(pay_var.get())<=account_balances[0] and (phone_var.get())==phone_numbers[0]:
        canvas_final=tk.Canvas(APP_win,bg='white',width=SETWIDTH,height=100)
        canvas_final.grid(row=1,column=0,sticky=tk.W)
        pay_confirm=tk.PhotoImage(file='pay_success.png')
        canvas_final.image=pay_confirm
        canvas_final.create_image(0,0,ancho=tk.NW,image=pay_confirm)
    
    elif int(pay_var.get())>account_balances[0] or (phone_var.get())!=phone_numbers[0]:
        canvas_final_1=tk.Canvas(APP_win,bg='white',width=SETWIDTH,height=100)
        canvas_final_1.grid(row=1,column=0,sticky=tk.W)
        pay_unsuccess=tk.PhotoImage(file='transaction_failed.png')
        canvas_final_1.image=pay_unsuccess
        canvas_final_1.create_image(0,0,ancho=tk.NW,image=pay_unsuccess)

        

# This function is for blitting out required details for making paymnet.
def made_payment():
    
    canvas_pay=tk.Canvas(APP_win,bg='white',width=SETWIDTH,height=348)
    canvas_pay.grid(row=0,column=0,sticky=tk.NW)
    canvas_pay.create_image(0,0,ancho=tk.NW,image=welcome_screen)
    canvas_pay.image=welcome_screen
    
    
    canvas_detail=tk.Canvas(APP_win,width=SETWIDTH,height=100,bg='white')
    canvas_detail.grid(row=1,column=0,sticky=tk.W)
    phone_label=tk.Label(canvas_detail,text='ENTER PHONE NUMBER: ',font='times 15 bold')
    phone_label.grid(row=0,column=0,sticky=tk.W,padx=2,pady=1)
    phone_var=tk.StringVar()
    phone_entry=tk.Entry(canvas_detail,textvariable=phone_var,font=("Times", "15", "bold italic"),bg='green',fg='white',bd=5,width=12)
    phone_entry.grid(row=0,column=1,padx=2,pady=1)
    
    pay_label = tk.Label(canvas_detail,text='ENTER PAY AMOUNT: ',font='times 15 bold')
    pay_label.grid(row=1,column=0,padx=2,pady=2)
    pay_var=tk.IntVar()
    pay_entry=tk.Entry(canvas_detail,textvariable=pay_var,font=("Times", "15", "bold italic"),bg='green',fg='white',bd=5,width=5)
    pay_entry.grid(row=1,column=1,padx=2)
    
    font=cv2.FONT_HERSHEY_SIMPLEX
    submit_btn= tk.Button(APP_win,text='SUBMIT',width=71,height=2,bg='#FF9999',fg='red',command=partial(submit,pay_var,phone_var))
    submit_btn['font']=font
    submit_btn.grid(row=2,column=0,sticky=tk.W,padx=0.5)
    
    return

#-----------------------------------------------------------------------------------------------------------------------------------------#
# This is deactivate buttons   
def disable(button):
    button['state']='disabled'
#------------------------------------------------------------------------------------------------------------------------------------------#  
#This function is responsible for playing scanned video, which shows no. of eye_blinks
# and also responsible foor calling img_matching_screen, made_payment function.
def video_play(speed):
    
    disable(start_btn)
    output_scan_vid_cap = cv2.VideoCapture('output.mp4')
    flag = True
    while True:
        if flag:
            canvas_text = tk.Canvas(APP_win,bg='white',width=SETWIDTH,height=100)
            canvas_text.grid(row=1,column=0,sticky=tk.NW)
            scan_in_progress_text = tk.PhotoImage(file='scan_in_progress.png')
            canvas_text.create_image(0,0,ancho=tk.NW,image=scan_in_progress_text)
            canvas_text.image=scan_in_progress_text
        else:
            canvas_text.delete('all')
        flag = not flag
        frame=output_scan_vid_cap.get(cv2.CAP_PROP_POS_FRAMES)
        output_scan_vid_cap.set(cv2.CAP_PROP_POS_FRAMES,frame+speed)
        grabbed,frame1=output_scan_vid_cap.read()
        print(frame1)
        if not grabbed:
            print('call returned')
            break
        frame1=imutils.resize(frame1,width=SETWIDTH,height=348)
        frame1=ImageTk.PhotoImage(image=Image.fromarray(frame1))
        canvas=tk.Canvas(APP_win,bg='white',width=SETWIDTH,height=348)
        canvas.grid(row=0,column=0,sticky=tk.NW)
        canvas.image=frame1
        canvas.create_image(0,0,ancho=tk.NW,image=frame1)
    canvas_text = tk.Canvas(APP_win,bg='white',width=SETWIDTH,height=100)
    canvas_text.grid(row=1,column=0,sticky=tk.NW)
    liveness_detection = tk.PhotoImage(file='liveness_detection_complete.png')
    canvas_text.create_image(0,0,ancho=tk.NW,image=liveness_detection)
    canvas_text.image=liveness_detection
    time.sleep(5)
    img_matching_screen()
    made_payment()
    return
        
def thread_video_play(speed):
    thread=threading.Thread(target=video_play, args=(speed,))
    thread.daemon=1
    thread.start()
        

#---------------------------------------------------------------------------------------------------------------------------------------------#    

# This is function is for calculating no. of eye blinks. This function also gives us the screenshot of scanned video
# MAIN EYE BLINKS FUNCTION
def scanned_video():
    eye_blink_ratio_list =[]
    blink_count = 0
    previous_ratio = 100
    while True:
        grabbed, frame = video_scan_cap.read()
        if not grabbed:
            break
        # color frame into grayscale
        # win_name='image'
        frame = cv2.rotate(frame,cv2.ROTATE_90_COUNTERCLOCKWISE)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
       
        # No. of detected faces
        faces = detector(gray_frame)
        print(faces)
    
        n_faces=0
        for face in faces:
            x=face.left()
            y=face.top()
            x1=face.right()
            y1=face.bottom()
            # ALL 68 facial landmarks
            landmarks = predictor(gray_frame,face)
            print(landmarks.part(37))
            
            # left eye aspect ratio
            left_eye_aspect_ratio = eye_aspect_ratio([36,37,38,39,40,41],landmarks,frame)
            
            # right eye aspect ratio
            right_eye_aspect_ratio = eye_aspect_ratio([42,43,44,45,46,47],landmarks,frame)
            
            eye_blink_ratio = ((left_eye_aspect_ratio+right_eye_aspect_ratio)/2)*100
            eye_blink_ratio = np.round(eye_blink_ratio)
            eye_blink_ratio = eye_blink_ratio/100
            # cv2.imshow(win_name,frame)
            
            eye_blink_ratio_list.append(eye_blink_ratio)
            print(eye_blink_ratio)
            if eye_blink_ratio<0.20:
                if previous_ratio>0.20:
                    blink_count+=1
            previous_ratio=eye_blink_ratio
            
            n_faces+=1
        if n_faces>1:
            print('MORE THAN ONE FACE, NOT VALID, TRY AGAIN!')
            APP_win.destroy()
            sys.exit()
            
        
        # play scanned video on tkinter
        # frame_resize = imutils.resize(frame,width=SETWIDTH,height=SETHEIGHT)
        # frame_resize = ImageTk.PhotoImage(image=Image.fromarray(frame_resize))
        # canvas.image=frame_resize
        # canvas.create_image(0,0,ancho=tk.NW,image=frame_resize)
        cv2.putText(frame,'No. OF BLINKS : '+str(blink_count),(10,50),font,1,(0,255,0),2)
        
        out.write(frame)
        if blink_count==2 and previous_ratio>0.30:
            captured_frame = frame
            break
    video_scan_cap.release()
    out.release()
    cv2.destroyAllWindows()    
    return (captured_frame, blink_count)

#--------------------------------------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
#Function call before creating tkinter window-----------------------------------------------------------------------------#
    screenshot,eye_blink_count = scanned_video()
    print(eye_blink_count)

#-------------------------------------------------------------------------------------------------------------------------#

    # Main application window
    APP_win = tk.Tk()
    APP_win.geometry(str(SETWIDTH)+'x'+str(SETHEIGHT))
    # APP_win.resizable(0,0)
    APP_win.title('Face scan secure payment system')

#-------------------------------------------------------------------------------------------------------------------------#
    # canvas for welcome screen
    canvas =tk.Canvas(APP_win,bg='white',width=SETWIDTH,height=348)
    canvas.grid(row=0,column=0,sticky=tk.NW)
    welcome_screen = tk.PhotoImage(file='welcome_1.png')
    canvas.create_image(0,0,ancho=tk.NW,image=welcome_screen)
    canvas.image=welcome_screen

#-------------------------------------------------------------------------------------------------------------------------#
    # Canvas for welcome text
    canvas_text = tk.Canvas(APP_win,bg='white',width=SETWIDTH,height=100)
    canvas_text.grid(row=1,column=0,sticky=tk.NW)
    welcome_text = tk.PhotoImage(file='welcome_text.png')
    canvas_text.create_image(25,0,ancho=tk.NW,image=welcome_text)
    canvas_text.image=welcome_text

#-------------------------------------------------------------------------------------------------------------------------#
    # CREATE start face scanning button
    font=cv2.FONT_HERSHEY_SIMPLEX
    start_btn = tk.Button(APP_win,text='START FACE SCANNING',width=71,height=2,bg='#FF9999',fg='red',command=partial(thread_video_play,1))
    start_btn['font']=font
    start_btn.grid(row=2,column=0,sticky=tk.NW,padx=0.5)
    

#-------------------------------------------------------------------------------------------------------------------------#

    APP_win.mainloop()
    
    
#---------------------------------------FINISHED---------------------------------------------------------------------------#


