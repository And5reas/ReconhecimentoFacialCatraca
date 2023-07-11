import cv2 as cv
import numpy as np
import face_recognition
import os
from datetime import datetime


class ReconhecimentoFacial:

    def __init__(self):
        self.path = "ImgsDataBase"
        self.images = []
        self.classNames = []
        self.myList = os.listdir(self.path) # Pegar o nome de todas as imagens do DataBase

    def findEncodings(self, images):
        encodeList = []
        i = 0
        for img in images:
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            try:
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            except:
                print(f'"{self.classNames[i]}.jpg" | Não foi possivel codificar esta imagem')
            i += 1
        return encodeList

    def markAttendance(self, name):
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

    def Run(self):
        for i in self.myList:
            curImg = cv.imread(f'{self.path}/{i}')
            self.images.append(curImg)
            self.classNames.append(os.path.splitext(i)[0])

        encodeListKnown = self.findEncodings(self.images)
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
                    name = self.classNames[matchIndex].upper()

                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
                    cv.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 255), cv.FILLED)
                    cv.putText(frame, name, (x1+6, y2-6), cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2)

                    self.markAttendance(name)

            cv.imshow("Camera", frame)

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break



