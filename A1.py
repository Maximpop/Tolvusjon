import cv2
import time
import numpy as np

#def tup(x):
#    return tuple((int(x[1]), int(x[0])))

Reddest = False
brightest_spot = "opencv" #"loops" for two for loops

cap = cv2.VideoCapture(0)
retur = True

while True:
    retur, frame = cap.read()
    if not retur:
        print("Camera not loaded")
        break # turns of the software
    ti = time.monotonic() # time for frame rate

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
        lower_red = np.array([0, 0, 200], dtype = "uint8") 

        upper_red= np.array([0, 0, 255], dtype = "uint8")
        mask = cv2.inRange(frame, lower_red, upper_red)

    t = time.monotonic()
    cv2.putText(frame, f"{1/(t-ti+0.00001):.1f} FPS", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 204, 255))

    cv2.imshow("Assigment1", frame)

    k = cv2.waitKey(100) & 0xFF
    if k == ord('c'):
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