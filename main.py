from time import sleep
import cv2 as cv
import numpy as np
import os
import face_recognition

if __name__ == '__main__':

    # Iniciar captura de câmera e retornar algo se não encontrar a câmera
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
            input("Cannot open camera or not found")
            exit()

    while True:
        ret, frame = cap.read()

        frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        faceLoc = face_recognition.face_locations(frameRGB)[0]
        encodeNow = face_recognition.face_encodings(frameRGB)[0]
        cv.rectangle(frame, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 255, 0), 2)

        cv.imshow('Camera', frame)

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

