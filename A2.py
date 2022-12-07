import cv2
import time
import numpy as np
import random

def ransac(cor,err, threshold=0.3,iter= 50):
    topScore = 0
    topLineInliners = None
    topLine = None
    thres = len(cor)*threshold

    for i in range(iter): #main for loop
        #random points 
        corA = random.choice(cor) 
        corB = random.choice(cor)

        # line between points calc y = mx + b
        m = (corA[1]-corB[1])/(corA[0]-corB[0])
        b = corA[1] - m*corA[0]

        #counter that counts number of points within error value
        inliner = []
        for i, (x,y) in enumerate(cor):
            e = y - (m*x+b)
            if abs(e) < err: # if abs of e is smaller than our preset error, add to the list
                inliner.append(i)
            if len(inliner) > thres:
                return (m,b), inliner
            else: 
                if topScore < len(inliner):
                    topScore = len(inliner)
                    topLine = (m,b)
                    topLineInliners = inliner
    return topLine,topLineInliners


Reddest = False
brightest_spot = "opencv" #"loops" for two for loops

t_lower = 50  # Lower Threshold
t_upper = 150  # Upper threshold

cap = cv2.VideoCapture(0)
retur = True
ti = time.monotonic() # time for frame rate
retur, frame = cap.read()
#frame = cv2.imread("pic2.png")
if not retur:
    print("Camera not loaded")
frameCan = cv2.Canny(frame,t_lower,t_upper)    
#print(frame[20,200])
#print(frame.shape[1])
#arrray = np.array(frame.shape[0]*frame.shape[1])
#A the man the myth the legend Steinarr has shown me a better way! no need for two for loops....
#data = []
#for x in range(frame.shape[0]): #Max value search with x and y cordinates
#    for y in range(frame.shape[1]):
#        #print(frame[x,y])
#        if frame[x, y] != 0:
#            data.append([y,x])
cor = np.argwhere(frameCan)


#image = cv.circle(image, centerOfCircle, radius, color, thickness)
#cv2.circle(frame,data[0],3,(255, 0, 64),5)
for i in range(len(cor)):
    #code to lighten up edges
    #cv2.circle(frame,tuple((int(cor[i][1]), int(cor[i][0]))),1,(255, 0, 64),1)
    pass
line , inliner = ransac(cor,5)
xcor = 1000*line[0]+line[1]
xcor = int(xcor)

cv2.imshow("Assigment2", frame)
cv2.line(frame,(int(line[1]),0),(xcor,1000),(255,255,255),2)
#cv2.line(frameCan,(a[1],a[0]),(b[1],b[0]),(255,255,255),2)
while True:
    retur, frame = cap.read()
    frameCan = cv2.Canny(frame,t_lower,t_upper)
    cor = np.argwhere(frameCan)
    line , inliner = ransac(cor,5)
    xcor = 1000*line[0]+line[1]
    xcor = int(xcor)
    cv2.line(frameCan,(int(line[1]),0),(xcor,1000),(255,255,255),2)
    cv2.imshow("Assigment2", frameCan)
    
    
    
    #cv2.imshow("Assigment2", frameCan)

    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break
    if k == ord('l'):
        brightest_spot = "loops"
        print("using two for loop")
    elif k== ord('c'):
        retur, frame = cap.read()
        frameCan = cv2.Canny(frame,t_lower,t_upper)
        cor = np.argwhere(frameCan)
        line , inliner = ransac(cor,5)
        xcor = 1000*line[0]+line[1]
        xcor = int(xcor)
        cv2.line(frameCan,(int(line[1]),0),(xcor,1000),(255,255,255),2)
        cv2.imshow("Assigment2", frameCan)
cap.release()
cv2.destroyAllWindows()