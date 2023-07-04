import cv2 as cv
import numpy as np
import face_recognition
import os
from datetime import datetime

path = "ImgsDataBase"
images = []
classNames = []
myList = os.listdir(path) # Pegar o nome de todas as imagens do DataBase

for i in myList:
    curImg = cv.imread(f'{path}/{i}')
    images.append(curImg)
    classNames.append(os.path.splitext(i)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open("Attendance.csv", "r+") as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(",")
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime("%H:%M:%S")
            f.writelines(f"\n{name},{dtString}")

encodeListKnown = findEncodings(images)
print('Encoding Completed')

cap = cv.VideoCapture(0)

while True:
    sucess, frame = cap.read()
    imgS = cv.resize(frame, (0, 0), None, 0.25, 0.25)
    imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)

    faceLocFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, faceLocFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, faceLocFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 255), cv.FILLED)
            cv.putText(frame, name, (x1+6, y2-6), cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2)

            markAttendance(name)

    cv.imshow("Camera", frame)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break



