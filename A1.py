import cv2
import time
import numpy as np

Reddest = False
brightest_spot = "opencv" #"loops" for two for loops

cap = cv2.VideoCapture(0) #just change to (1) with ivcam for phone camera
retur = True

while True:
    ti = time.monotonic() # time for frame rate
    retur, frame = cap.read()
    if not retur:
        print("Camera not loaded")
        break # turns of the software
    

    if brightest_spot:
        gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
        maxVal = 0
        maxIndex = (0,0) #pixel location
        if brightest_spot == "opencv":
            minVal,MaxVal,minIndex,maxIndex = cv2.minMaxLoc(gray)
        if brightest_spot == "loops":
            for x in range(gray.shape[0]): #Max value search with x and y cordinates
                for y in range(gray.shape[1]):
                    if gray[x, y] > maxVal:
                        maxIndex = (x,y)
                        maxVal = gray[x,y]
            maxIndex = tuple((int(maxIndex[1]), int(maxIndex[0])))                

        cv2.circle(frame, maxIndex, 15, (208, 224, 64), 4)

    if Reddest:
       hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Look into this approach
       maxValRed = 0
       maxRedIND = (0,0) #pixel location
       for x in range(frame.shape[0]): #Max value search with x and y cordinates
            for y in range(frame.shape[1]):
                if frame[x, y,2] > maxValRed and frame[x, y,1] < 160 and frame[x, y,0] < 160 and abs(frame[x, y,1] - frame[x, y,0]) <15:
                    maxRedIND = (x,y)
                    maxValRed = frame[x,y,2]

       maxRedIND = tuple((int(maxRedIND[1]), int(maxRedIND[0])))                

       cv2.circle(frame, maxRedIND, 15, (255, 0, 64), 4)


    t = time.monotonic()
    cv2.putText(frame, f"{1/(t-ti+0.00001):.1f} FPS", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
    #print(f"{t-ti:.1f} FPS")
    #print(f"{ti:.1f} FPS")
    
    cv2.imshow("Assigment1", frame)

    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break
    if k == ord('l'):
        brightest_spot = "loops"
        print("using two for loop")
    elif k== ord('o'):
        brightest_spot = "opencv"
        print("using opencv")
    elif k== ord('r'):
        Reddest = not Reddest
cap.release()
cv2.destroyAllWindows()