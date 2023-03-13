import cv2
import pickle
import requests
import time
import numpy as np
import cvzone
def image(file,width,height):
    img=cv2.imread("car_parking.jpeg")
    return cv2.resize(img,(width,height))
car_w,car_h=80,30
try:
    with open("Past_position","rb") as f:
        pos=pickle.load(f)
except:
    pos=[]
def mouseClick(event,x,y,flag,parm):
    if event==cv2.EVENT_LBUTTONDOWN:
            pos.append((x,y))
    if event==cv2.EVENT_RBUTTONDOWN:
        for i,p in enumerate(pos):

            x1,y1=p
            if x1<x<x1+car_w and y1<y<y1+car_h:
                print(i, p)
                pos.pop(i)

    with open("Past_position",'wb') as f:
        pickle.dump(pos,f)
space=0
def car_check(im):
    global space
    space=0
    for i in pos:
        x,y=i
        imgCrop=im[y:y+car_h,x:x+car_w]
        # cv2.imshow("Croped Image-"+str(x*y),imgCrop)
        count=cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+car_h-10))
        if count>20:
            color=(0,0,122)
            space+=1
        else:color=(255,20,100)
        cv2.rectangle(img, (i[0], i[1]), (i[0] + car_w, i[1] + car_h),color, 2)
    cvzone.putTextRect(img,f"Free:{space}/{len(pos)}",(50,50))

v=cv2.VideoCapture(1)
while True:
    _,img=v.read()
    # img=image("car_parking.jpeg",300,500)
    gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur_img=cv2.GaussianBlur(gray_img,(3,3),1)
    img_dilate=cv2.adaptiveThreshold(blur_img,250,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV,25,16)
    # img_median=cv2.medianBlur(img_threshold,5)
    # kernel=np.ones((3,3),np.int8)
    # img_dilate=cv2.dilate(img_median,kernel,iterations=1)

    car_check(img_dilate)
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image",mouseClick)

    cv2.imshow("gray",img_dilate)
    try:
        requests.get("http://192.168.1.5/occupied" + str(space))
    except:
        pass
    time.sleep(1)
    cv2.waitKey(1)


