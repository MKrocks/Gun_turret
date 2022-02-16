from pyfirmata import Arduino,SERVO,util
import  time
import cv2
import numpy as np
def returnp(x,y):

    if (x-320)*(x-320)+(y-240)*(y-240)>1600:
        return ((((x-320)/320)+1)/2,(((y-320)/320)+1)/2)
    else:
        return (0,0)
def mousePoints(event,p,q,flags,parameters):


    global  i,j
    i=i
    j=j

    p,q=returnp(p,q)
    if event==cv2.EVENT_LBUTTONDOWN:

        if p<0.4:
            i+=2
            pin1.write(i/100)
        if p>0.6:
            i-=2
            pin1.write(i/100)
        if q<0.4:
            j-=2
            pin2.write(j/100)
        if q>0.6:
            j+=2
            pin2.write(j/100)
    if event==cv2.EVENT_RBUTTONDOWN:

        pin3.write(0.1)
        time.sleep(1)
    if event== cv2.EVENT_MBUTTONDOWN:
        pin3.write(0.99)
        time.sleep(1)



def returnPoints(x,y,w,h):
     if (x-320)*(x-320)+(y-240)*(y-240)>1600:
      return ((((x-320)/320)+1)/2,(((y-320)/320)+1)/2,(((w-240)/240)+1)/2,(((h-240)/240)+1)/2)
     else:
       return(0,0,0,0)



faceCascate = cv2.CascadeClassifier('resources/haarcascade_frontalface_alt2.xml')
board=Arduino('COM6')
iterator=util.Iterator(board)
iterator.start()
tvl=board.get_pin('a:0:i')
pin1=board.get_pin('d:3:p')
pin2=board.get_pin('d:9:p')
pin3=board.get_pin('d:5:p')

cmt=cv2.VideoCapture(1)
cmt.set(3,640)
cmt.set(4,480)
i=50
j=50
pin1.write(0.50)
pin2.write(0.50)
while True:

    success, img = cmt.read()
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascate.detectMultiScale(imgGrey, 1.1, 4)
    pin1.write(i/100)
    for (x, y, w, h) in faces:
        cv2.circle(img, (x+w//2, y+h//2),h//2 , (255, 0, 0), 3)
        p,q,r=x+w//2, y+h//2,h//2
        cv2.putText(img,'Target Lock',(x+w//2,y+10),cv2.FONT_ITALIC,1,(0,0,255),2)
        cv2.line(img,(int(p-r//1.4),int(q-r//1.4)),(int(p+r//1.4),int(q+r//1.4)),(0,0,255),2)
        cv2.line(img, (int(p + r // 1.4),int( q - r // 1.4)), (int(p - r // 1.4),int( q + r // 1.4)), (0, 0, 255), 2)
        x,y,w,h=returnPoints(x,y,w,h)
        y=y+h/2
        x=x+w/2
        if y<0.35:
            j-=1
            pin2.write(j/100)
            time.sleep(0.001)
        if j<1:
            j=2

        if j>98:
            j=95
        if i<1:
            i=2
        if x<0.51:
            i+=1
            pin1.write(i/100)
            time.sleep(0.001)
        if i>98:
            i=95
        if y > 0.45:
            j += 1
            pin2.write(j / 100)
            time.sleep(0.001)

        if x>0.61:
            i-=1
            pin1.write(i/100)
            time.sleep(0.001)
        if i<1:
            i=2
        if j>98:
            j=95
        if i>98:
            i=95
        print(i , j)

    cv2.setMouseCallback('image', mousePoints)
    cv2.imshow('image', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
