import cv2
import sqlite3
import requests

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)
url_insert_update = 'http://192.168.1.102/FacialRecognition/insertOrUpdate.php'


def insert_or_update(user_id, name, age, gen):
    conn = sqlite3.connect("FaceBase.db")
    conn.execute("CREATE TABLE IF NOT EXISTS person(id INTEGER, nom VARCHAR(255), age VARCHAR(255), sexe VARCHAR(255),"
                 "presence VARCHAR(1), datePresence CURRENT_DATE )")
    cmd = "SELECT * FROM person WHERE id=" + str(user_id)
    cursor = conn.execute(cmd)
    
    is_record_exist = 0

    for row in cursor:
        is_record_exist = 1
    if is_record_exist == 1:
        cmd = "UPDATE person SET nom= '" + str(name) + "' WHERE id=" + str(user_id)
        cmd2 = "UPDATE person SET age= '" + str(age) + "' WHERE id=" + str(user_id)
        cmd3 = "UPDATE person SET sexe= '" + str(gen) + "' WHERE id=" + str(user_id)
        cmd4 = "UPDATE person SET presence=" +str(0) + " WHERE id=" + str(user_id)
        cmd5 = "UPDATE person SET datePresence = CURRENT_DATE " + "WHERE id=" + str(user_id)
    else:
        cmd = "INSERT INTO person(id,nom,age,sexe, presence, datePresence) VALUES(" + str(user_id) + ",'" + str(name) + "','" + str(
            age) + "','" + str(gen) + "','" + str(0) + "',CURRENT_DATE " + ")"
        print(cmd)
        cmd2 = ""
        cmd3 = ""
        cmd4 = ""
        cmd5 = ""

    conn.execute(cmd)
    conn.execute(cmd2)
    conn.execute(cmd3)
    conn.execute(cmd4)
    conn.execute(cmd5)
    conn.commit()
    conn.close()

def sendRequest(url, data):
    response = requests.post(url, data=data)
    return response



var_user_id = input("Entrez un id : ")
var_name = input("Entrez le nom d'utilisateur : ")
var_age = input("Entrez  l'âge : ")
var_gen = input('Entez le sexe  : ')
insert_or_update(var_user_id, var_name, var_age, var_gen)
data = { 'nom' : var_name, 'age' : var_age, 'sexe' : var_gen, 'presence' : str(0), 'datePresence' : '' }
responseRequest = sendRequest(url_insert_update, data)
print(responseRequest.text)
sampleNum = 0

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        sampleNum = sampleNum + 1;
        cv2.imwrite("dataSet/User." + str(var_user_id) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.waitKey(100)

    cv2.imshow("Face", img)
    cv2.waitKey(1)

    if sampleNum > 20:
        break;
cam.release()
cv2.destroyAllWindows()
