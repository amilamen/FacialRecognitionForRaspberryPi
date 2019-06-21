import os
import cv2
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'dataSet'

def get_images_with_id(file_path):
    image_paths = [os.path.join(file_path,f) for f in os.listdir(file_path)]
    faces = []
    ids = []

    for image_path in image_paths:
        face_img = Image.open(image_path).convert('L');
        face_np = np.array(face_img,'uint8')
        id_image = int(os.path.split(image_path)[-1].split('.')[1])
        faces.append(face_np)
        ids.append(id_image)
        cv2.imshow("training",face_np)
        cv2.waitKey(10)
    return np.array(ids),faces

var_ids, var_faces = get_images_with_id(path)
recognizer.train(var_faces, var_ids)
recognizer.write('recognizer/trainningData.yml')
cv2.destroyAllWindows()
