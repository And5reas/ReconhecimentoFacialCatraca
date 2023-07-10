from StartCatracaReconhecimentoFacial import ReconhecimentoFacial
from CadastrarRostos import CadastrarRostoDB
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from threading import Thread


class Cadastrar(Screen):
    def on_kv_post(self, base_widget):
        global camera
        camera = self.ids.CVcamera

    def LimparTudo(self):
        self.ids["lbl_retorno"].text = ""
        self.ids["txt_nomeCadastrar"].text = ""
        self.ids["txt_nomeCadastrar"].background_color = (1, 1, 1, 1)

    def Cadastrar(self):
        nome = self.ids["txt_nomeCadastrar"].text
        if nome != "":
            if CadasFace.Cadastrar(nome):
                self.ids["lbl_retorno"].text = "Rosto cadastrado com exito >:D"
            else:
                self.ids["txt_nomeCadastrar"].background_color = (.8, .2, .2, 1)
                self.ids["lbl_retorno"].text = "Nome já cadastrado. Tente novamente com outro nome."
        else:
            self.ids["txt_nomeCadastrar"].background_color = (.8, .2, .2, 1)
            self.ids["lbl_retorno"].text = 'Nome em branco. Preencha o campo "Nome".'


class Janela(Screen):
    def on_enter(self, *args):
        self.StopCamera()
        CadasFace.CloseCamera()

    def StopCamera(self):
        Clock.unschedule(self.loadVideo)

    def StartCamera(self):
        CadasFace.SetCamera()
        Clock.schedule_interval(self.loadVideo, 1/30)

    def loadVideo(self, *args):
        buffer, shape1, shape2 = CadasFace.StartCamera()
        texture = Texture.create(size=(shape1, shape2), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        camera.texture = texture

    def startReconhecimento(self):
        RF = ReconhecimentoFacial()
        threadCadastrar = Thread(target=RF.Run())
        threadCadastrar.start()


class WindowManager(ScreenManager):
    pass


class And5reasVisage(App):
    def build(self):
        from kivy.config import Config
        Config.read("and5reasvisage.ini")
        return kv


CadasFace = CadastrarRostoDB()
camera = None
kv = Builder.load_file("principal.kv")

if __name__ == '__main__':
    And5reasVisage().run()
