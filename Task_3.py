import cv2  
import numpy as np
face_cascade = cv2.CascadeClassifier('C:/Users/saume/Anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml') 
cap = cv2.VideoCapture(0) 
while 1:  
  
    ret, img = cap.read() 
    if ret == True: 
                   img = np.asarray(img, dtype=np.uint8)
                   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
                   faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
  
                   for (x,y,w,h) in faces: 
                                          cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,0),2)  
                                          roi_gray = gray[y:y+h, x:x+w] 
                                          roi_color = img[y:y+h, x:x+w]
                                        
                   cv2.imshow('img',img) 
  
    # Wait for Esc key to stop 
                   k = cv2.waitKey(30) & 0xff
                   if k == 27: 
                              break
cap.release() 
cv2.destroyAllWindows()  