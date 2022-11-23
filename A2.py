import cv2
import time
import numpy as np


Reddest = False
brightest_spot = "opencv" #"loops" for two for loops

t_lower = 50  # Lower Threshold
t_upper = 150  # Upper threshold

cap = cv2.VideoCapture(0)
retur = True
ti = time.monotonic() # time for frame rate
retur, frame = cap.read()
if not retur:
    print("Camera not loaded")
frame = cv2.Canny(frame,t_lower,t_upper)    
#print(frame[20,200])
#print(frame.shape[1])
#arrray = np.array(frame.shape[0]*frame.shape[1])
data = []
for x in range(frame.shape[0]): #Max value search with x and y cordinates
    for y in range(frame.shape[1]):
        #print(frame[x,y])
        if frame[x, y] != 0:
            data.append([y,x])
              
print(data[0][0])
#image = cv.circle(image, centerOfCircle, radius, color, thickness)
#cv2.circle(frame,data[0],3,(255, 0, 64),5)
for i in range(len(data)):

    cv2.circle(frame,data[i],1,(255, 0, 64),1)
    pass
while True:
      

    
    cv2.imshow("Assigment2", frame)
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break
    if k == ord('l'):
        brightest_spot = "loops"
        print("using two for loop")
    elif k== ord('c'):
        retur, frame = cap.read()
        frame = cv2.Canny(frame,t_lower,t_upper)
cap.release()
cv2.destroyAllWindows()