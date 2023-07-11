import cv2 as cv
import os


class CadastrarRostoDB:

    def __init__(self):
        self.path_cadastro = ""
        self.B, self.G, self.R = 255, 0, 0
        self.margemCF = 50
        self.faceCascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.cap = None
        self.i = -1

        self.pathDataBase = "ImgsDataBase"
        if not os.path.isdir(self.pathDataBase):
            os.mkdir(self.pathDataBase)

    def SetCamera(self):
        self.cap = cv.VideoCapture(0)
        if not self.cap.isOpened():
            input("Cannot open camera or not found")
            exit()

    def CloseCamera(self):
        self.cap = None

    def StartCamera(self):
        ret, frame = self.cap.read()
        imgGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(imgGray, scaleFactor=1.1, minNeighbors=15, minSize=(50, 50))
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x - self.margemCF, y - self.margemCF), (x + w + self.margemCF, y + h + self.margemCF), (self.B, self.G, self.R), 2)

            if self.i > 0:
                imgCropped = frame[y - self.margemCF:y + h + self.margemCF, x - self.margemCF:x + w + self.margemCF]
                cv.imwrite(self.path_cadastro, imgCropped)
                self.i -= 1
            elif self.i == 0:
                self.B, self.G, self.R = 255, 0, 0
                self.i -= 1

        return cv.flip(frame, 0).tostring(), frame.shape[1], frame.shape[0]

    def Cadastrar(self, nome):
        self.i = 1
        self.B, self.G, self.R = 0, 255, 255
        self.path_cadastro = self.pathDataBase + "\\" + nome + ".jpg"
        while os.path.isfile(self.path_cadastro):
            self.B, self.G, self.R = 255, 0, 0
            self.i = -1
            return False
        return True
