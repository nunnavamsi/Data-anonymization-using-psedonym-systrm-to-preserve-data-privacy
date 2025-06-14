import numpy as np
import cv2
import scipy.spatial.distance as dist
import hmac
import hashlib 
import binascii

def create_sha256_signature(key, message):
    byte_key = key#binascii.unhexlify(key)
    message = message.encode()
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()

ids = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']

img = cv2.imread('images/2.jpg')
img_filter = cv2.GaussianBlur(img,(5,5),0)
img_filter = cv2.medianBlur(img_filter,5)
img_filter = cv2.cvtColor(img_filter, cv2.COLOR_BGR2GRAY)
clahe = cv2.createCLAHE(clipLimit=6.0, tileGridSize=(30,30))
img_filter = clahe.apply(img_filter)
img_filter = cv2.Canny(img_filter,10,120)
cv2.imwrite("test.png",img_filter)
img_filter = cv2.imread("test.png",0)

gray = np.float32(img_filter)
dst = cv2.cornerHarris(gray,2,3,0.20)
dst = cv2.dilate(dst,None)
img_filter = cv2.imread("test.png")
img_filter[dst>0.20*dst.max()]=[0,255,0]

temp1 = cv2.cvtColor(img_filter, cv2.COLOR_BGR2GRAY)
temp2 = dst
print(temp1.shape)
print(temp2.shape)
distance = dist.euclidean(temp1.flatten(), temp2.flatten())

points = temp1[0:1,0:30]
points = (points/255)[0]
print(points)

master_key = 0
for i in range(len(points)):
    if points[i] == 1:
        master_key = master_key + pow(2, i)
print(master_key)
user = 'kaleem'
random_userid = ''
for i in range(len(user)):
    ch = user[i]
    for j in range(len(ids)):
        if ids[j] == ch:
            random_userid+=str(j)
            
print(random_userid)
secret_key = str(master_key).encode()
hmac = create_sha256_signature(secret_key,random_userid+str(points.ravel()[0]))
print(hmac)
cv2.imshow("test",img_filter)
cv2.waitKey(0)
