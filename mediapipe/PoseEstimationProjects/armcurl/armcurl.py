import cv2
import mediapipe as mp
import time
import armcurl_module as am
import numpy as np

cap = cv2.VideoCapture(0)
detector = am.poseDetector()
count = 0
dir = 0

pTime = 0
while True:
    success, img = cap.read()
    img = detector.findPose(img, draw=False)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) != 0:
        #right arm
        angle = detector.findAngle(img, 12, 14, 16)
        # #left arm
        # detector.findAngle(img, 11, 13, 15)
        
        per = np.interp(angle, (210, 335), (0, 100)) #covert angles into percentage
        bar = np.interp(angle, (210, 335), (900, 200))
        # print(angle, per)
        
        #Check for the dumbbell curls
        color = (1, 193, 246)
        if per >= 80:
            if per == 100:
                color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (1, 193, 246)
            if dir == 1:
                count += 0.5
                dir = 0
                
        #draw bar
        cv2.rectangle(img, (1800, 200), (1865, 900), color, 3)
        cv2.rectangle(img, (1800, int(bar)), (1865, 900), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (1800, 175), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
        
        #draw curl count
        cv2.rectangle(img, (0, 1080), (350, 800), (1, 193, 246), cv2.FILLED)
        cv2.putText(img, str(int(count)), (30, 1000), cv2.FONT_HERSHEY_PLAIN, 15, (0, 0, 0), 25)
        
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)