import cv2
from whichcluster3 import convertsmall
from whichcluster2 import whichcluster
import numpy as np                       #importing libraries


def blob(filename):
    im = cv2.imread('images/'+str(filename)+".jpg",1)
    img = cv2.rectangle(im,(384,0),(510,128),(0,255,0),3)
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print contours
    cv2.drawContours(im2, contours, -1, (0,255,0), 3)
    cv2.imshow('contours',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''crop_img = img[200:400, 100:300] # Crop from x, y, w, h -> 100, 200, 300, 400
    # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
    cv2.imshow("cropped", crop_img)
    cv2.waitKey(0)'''
motion = -1

def getMotion():
    global motion
    cap = cv2.VideoCapture(0)                #creating camera object
    filename = 178
    is10 = 0
    while( cap.isOpened() ) :
        ret,frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        '''ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_MASK)
        cv2.imshow('OTSU',thresh1)                  #displaying the frames'''
        ret,thresh2 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        thresh1 = thresh2[thresh2.shape[0]/3:thresh2.shape[0],thresh2.shape[0]/8:thresh2.shape[1]/8*7]
        cv2.imwrite("input.jpg",thresh1)    
        array =convertsmall("input.jpg")
        list1=[]
        for i in range(array.shape[0]):
            list1.extend(array[i])
        result=whichcluster(list1)
        if (result == 1):
            motion = 1
        if (result == 2) :
            motion = 2    
        if (result == 3):
            motion = 3
        if (result == 4) :
            motion = 4
        if (result == 5):
            motion= 5
        if (result == 6) :
            motion = 6
        if (result == 7):
            motion = 7
        cv2.imshow('256',thresh1)   #good for dark bacground
        print motion
        '''if (is10  == 10) :
            filePath = 'images/' + str(filename)
            cv2.imwrite(filePath+".jpg",thresh1)
            filename += 1
            is10 = 0
            file = open(filePath+".txt.",'w')
            for x in range(thresh1.shape[0]):
                for y in range(thresh1.shape[1]) :
                    number = thresh1[x][y];
                    if (number == 255) :
                        file.write("1,")
                    else :
                        file.write("0,");
                file.write("\n");'''
                
        is10 += 1

        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        if cv2.waitKey(1)& 0xFF == ord('p'):
            cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()
    #blob(12)

while (True):
    getMotion()
    if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
