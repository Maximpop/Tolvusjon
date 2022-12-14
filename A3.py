import cv2
import numpy as np
from cocoNames import cocoNames
import time

cap = cv2.VideoCapture(0)
whT = 320
confThress = 0.5
nmsThress = 0.3
modelConfiguration = "yolov3.cfg"
modelWeights = "yolov3.weights"
#modelConfiguration = "yolov3-tiny.cfg"
#modelWeights = "yolov3-tiny.weights"

net = cv2.dnn.readNetFromDarknet(modelConfiguration,modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def findObject(outputs,img):
    hT,wT,cT = img.shape
    bbox = []
    classids = []
    confs = []

    for output in outputs:
        for det in output:
            scores = det[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > confThress:
                w,h = int(det[2]*wT), int(det[3]*hT)
                x,y = int(det[0]*wT - w/2), int(det[1]*hT - h/2)
                bbox.append([x,y,w,h])
                classids.append(classID)
                confs.append(float(confidence))
    indices = cv2.dnn.NMSBoxes(bbox,confs,confThress,nmsThress)
    for i in indices:
        #i = i[0]
        box = bbox[i]
        x,y,w,h = box[0],box[1],box[2],box[3]
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
        cv2.putText(img,f'{cocoNames[classids[i]]} {int(confs[i]*100)}%',(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,255),2)



while True:
    ti = time.monotonic() # time for frame rate
    success, img = cap.read()
    blob = cv2.dnn.blobFromImage(img,1/255,(whT,whT),[0,0,0],1,crop=False)
    net.setInput(blob)

    layerNames = net.getLayerNames()
    #print(layerNames)
    outputNames = [layerNames[i-1] for i in net.getUnconnectedOutLayers()]
    #print(outputlayers)
    #print(outputNames)
    outputs = net.forward(outputNames)
    #print(outputs[0].shape)
    #print(outputs[1].shape)
    #print(outputs[2].shape)
    #print(outputs[0][0])
    #print(findObject(outputs,img))
    findObject(outputs,img)
    t = time.monotonic()
    cv2.putText(img, f"{1/(t-ti+0.00001):.1f} FPS", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
    cv2.imshow("image",img)


    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break