import cv2
import numpy as np
import time

# Based on tutorial from https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html

frame = cv2.imread("frameTest.jpg")

frame = cv2.resize(frame[:4000, :], (480, 640))

while True:

    ti = time.time()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow("gray", gray)
    canny = cv2.Canny(gray, 50, 200)

    cv2.imshow("canny", canny)

    cannyColor = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
    cannyColorCopy = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)

    countourArr = 255*np.ones(gray.shape, np.uint8)

    lines = cv2.HoughLines(canny, 1, np.pi/180, 100)

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(cannyColor, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)
            cv2.line(countourArr, pt1, pt2, 0, 3, cv2.LINE_AA)
    
    #linesP = cv2.HoughLinesP(canny, 1, np.pi / 180, 50, None, 50, 10)
    #if linesP is not None:
        #for i in range(0, len(linesP)):
            #l = linesP[i][0]
            #cv2.line(cannyColorCopy, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
    

    contours, q= cv2.findContours(countourArr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maxArea = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > maxArea:
            maxArea = area
            CON = c
    approxi = cv2.approxPolyDP(CON,0.05*cv2.arcLength(CON,True),True)
    cv2.drawContours(countourArr, [approxi], -1, (150), 4)
    cornersOld = np.float32(approxi)
    cornersNew = np.array([
        [0, 0],
        [0, 480],
        [640, 480],
        [640, 0],], np.float32)

    if len(cornersOld) == 4: #if four corners

        getPer = cv2.getPerspectiveTransform(cornersOld, cornersNew)
        Warped = cv2.warpPerspective(frame, getPer, (640, 480))
        cv2.imshow("Cowboy and The horse warped", Warped)
    
    t = time.time()

    cv2.imshow("onesArr", countourArr)
    cv2.imshow("Frame", frame)
    #cv2.imshow("Hough-P", cannyColorCopy)
    
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break
    

