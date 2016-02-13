import wx
from database import *

class MainWindow(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.init_ui()

    def init_ui(self):
        self.SetSize((480, 320))
        self.SetTitle('Baroness Control')
        panel = wx.Panel(self, -1)

        products = get_products()
        buttonids = []
        i = 0
        for product in products:
            but = wx.Button(panel, label=product.name, pos=(50+i*150, 50), size=(100, 100))
            print "Button %s created" % product.name
            self.Bind(wx.EVT_BUTTON, self.on_button_press, id=but.Id)
            i = i+1

        self.Bind(wx.EVT_CLOSE, self.on_quit)
        self.Show(True)

    def on_button_press(self,e, id=-1):
        print e

    def on_quit(self, e):
        print "close"
        self.Destroy()