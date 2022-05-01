import cv2
import cvzone
from pynput.keyboard import Controller
from cvzone.HandTrackingModule import HandDetector
from time import sleep
#opencv version: latest
#cvzone version: 1.4.1
#mediapipe version: 0.8.7

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8)
keys = [['Q','W','E','R','T','Y','U','I','O','P'],
        ['A','S','D','F','G','H','J','K','L','+'],
        ['Z','X','C','V','B','N','M','-','*','/'],
        ['1','2','3','4','5','6','7','8','9','0']]

finalText = ""

keyboard = Controller()

def drawAll(img,buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[0]), 20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


class Button():
    def __init__(self,pos,text,size=[85,85]):
        self.pos=pos
        self.size=size
        self.text=text

buttonList=[]
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img=cap.read()
    img=detector.findHands(img)
    lmlist, bboxInfo=detector.findPosition(img)
    img = drawAll(img, buttonList)

    if lmlist:
        for button in buttonList:
            x,y = button.pos
            w,h = button.size

            #Hover
            if x<lmlist[8][0]<x+w and y<lmlist[8][1]<y+h: #point 8 is index finger
                cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l,_,_ = detector.findDistance(8,12,img,draw=False) #To ignore something in python, just add underscore
                #print(l)

                #Click
                if l<70: #I play Volleyball and my hands and fingers are big
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 255), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    sleep(0.15)

    cv2.rectangle(img, (50,450), (700,550), (0, 0, 255), cv2.FILLED)
    cv2.putText(img, finalText, (60, 525), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow('Result',img)
    cv2.waitKey(1)