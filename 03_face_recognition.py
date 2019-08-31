import cv2
import sqlite3
import requests

url_update = 'http://YOUR_IP_ADDRESS/FacialRecognition/updateProfile.php'
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("recognizer/trainningData.yml")
font = cv2.FONT_HERSHEY_COMPLEX
# font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX,0.4,1,0,1)

def sendRequest(url, data):
    response = requests.post(url, data=data)
    return response

def get_profile(user_id):
    conn = sqlite3.connect("FaceBase.db")
    cmd_update_presence = "UPDATE person SET presence=" + str(1) + " WHERE id=" + str(user_id)
    conn.execute(cmd_update_presence)
    conn.commit()
    cmd = "SELECT * FROM person WHERE id = " + str(user_id)
    cursor = conn.execute(cmd)
    profile = None

    for row in cursor:
        profile = row
    conn.close()
    return profile

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray,1.3,5)

    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        var_user_id, conf = rec.predict(gray[y:y+h,x:x+w])
        print("Conf" + str(conf))
        confidence = round(100 - conf)
        print(confidence)

        if confidence >= 60:
            profile = get_profile(var_user_id)
            print(profile)
            cv2.putText(img, "Nom : "+str(profile[1]), (x,y+h+20),  font, 1, (0,255,0), 2)
            cv2.putText(img, "Statut : " + str('Present'), (x, y + h + 70), font, 1, (0, 255, 0), 2)
            data = { 'id' : var_user_id }
            responseRequest = sendRequest(url_update, data)
            print(responseRequest.text)
        data = { 'id' : '1' }
        responseRequest = sendRequest(url_update, data)
    cv2.imshow("Visage",img)
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
