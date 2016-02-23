# -*- coding: utf-8 -*-
import wx
from plot import *
from database import *
import flask as fla

class MainWindow(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.SetSize((480, 320))
        self.SetTitle('Baroness Control')

        self.panelStart = PanelStart(self)
        self.panelUser = Panel1(self)
        self.panelList = Panel2(self)
        self.panelThanks = PanelThanks(self)

        self.active = 0
        self.user = User()

        self.switchPanels()

        self.Show()

    def onStart(self, e):
        self.active = 2
        self.switchPanels()

    def delayExit(self, e=None):
        wx.CallLater(5000, self.onExit)

    def getUser(self):
        return self.user.id
    #    return self.user

    def onExit(self, e=None):
        self.active = 0
        self.switchPanels()

    def onUser(self, e):
        longn = e.GetEventObject().GetLabelText()
        for user in get_users():
            if user.longname == longn:
                self.user = user
        if not self.user.isblack:
            self.panelUser.l_user.SetLabel(self.user.longname)
            self.active = 1 #getränkeauswahl
        else:
            self.active = 0 #start TODO: Sorry Bro Panel
        self.switchPanels()

    def onProduct(self, e):
        self.active = 3
        print self.user.longname + ' consumes'
        buttonl = e.GetEventObject().GetLabelText()
        drink = buttonl.split('\n')[0]
        with app.app_context():
            for i in range(0, int(self.panelUser.GetAmount())):
                add_consume(self.user.name, get_product_by_name(drink).id)
        plot_all_thread(self.user)
        self.switchPanels()

    def switchPanels(self):
        if self.active == 0:
            self.panelStart.Show()
            self.panelUser.Hide()
            self.panelList.Hide()
            self.panelThanks.Hide()
        elif self.active == 1:
            self.panelStart.Hide()
            self.panelUser.Show()
            self.panelList.Hide()
            self.panelThanks.Hide()
        elif self.active == 2:
            self.panelStart.Hide()
            self.panelUser.Hide()
            self.panelList.Show()
            self.panelThanks.Hide()
        elif self.active == 3:
            self.panelStart.Hide()
            self.panelUser.Hide()
            self.panelList.Hide()
            self.panelThanks.Show()
            self.panelThanks.label_1.SetLabel(self.user.longname)
            self.delayExit()

class PanelStart (wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos = wx.DefaultPosition, size=(480, 320))
        #panel = wx.Panel(self, -1)
        self.bitmap_1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap("./app/static/start.png", wx.BITMAP_TYPE_ANY))
        self.Bind(wx.EVT_LEFT_DOWN, parent.onStart)
        self.bitmap_1.Bind(wx.EVT_LEFT_DOWN, parent.onStart)

    def on_quit(self, e):
        print "close"
        self.Destroy()

class PanelThanks (wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos = wx.DefaultPosition, size=(480, 320))
        #panel = wx.Panel(self, -1)
        self.bitmap_1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap("./app/static/thanks.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_1.Bind(wx.EVT_LEFT_DOWN, parent.onStart)
        self.label_1 = wx.StaticText(self, wx.ID_ANY, 'bla blub', pos=(100,100))
        self.label_1.SetFont(wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Humor Sans"))

    def on_quit(self, e):
        print "close"
        self.Destroy()

class Panel1 (wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos = wx.DefaultPosition, size=(480, 320))

        self.bitmap_1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap("./app/static/products.png", wx.BITMAP_TYPE_ANY))

        products = get_products()
        buttonids = []
        i = 0
        for product in products:
            if product.isshown:
                #480x320
                self.but = wx.Button(self, id=wx.ID_ANY, label=product.name + u"\n" + "%0.2f" % product.price, pos=(0+i*120, 0), size=(120, 120))
                self.but.SetFont(wx.Font(23, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Humor Sans"))
                print "Button %s created" % product.name
                self.but.Bind(wx.EVT_LEFT_DOWN, parent.onProduct, id=self.but.Id)
                i = i+1

        self.b_less = wx.Button(self, id = wx.ID_ANY, label=u"-", pos=(0,240), size=(120, 80))
        self.b_less.SetFont(wx.Font(60, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Humor Sans"))
        self.b_less.Bind(wx.EVT_LEFT_DOWN, self.onLess, id=self.b_less.Id)

        self.l_amount = wx.StaticText(self, wx.ID_ANY, "1", pos=(145,245), style=wx.ALIGN_CENTER)
        self.l_amount.SetFont(wx.Font(50, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Sans"))

        self.b_more = wx.Button(self, id = wx.ID_ANY, label=u"+", pos=(240,240), size=(120, 80))
        self.b_more.SetFont(wx.Font(60, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Humor Sans"))
        self.b_more.Bind(wx.EVT_LEFT_DOWN, self.onMore, id=self.b_more.Id)

        self.b_exit = wx.Button(self, id = wx.ID_ANY, label=u"x", pos=(360,240), size=(120, 80))
        self.b_exit.SetFont(wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Humor Sans"))
        self.b_exit.Bind(wx.EVT_LEFT_DOWN, parent.onExit, id=self.b_exit.Id)

        self.l_user = wx.StaticText(self, wx.ID_ANY, "todo", pos=(20,170), style=wx.ALIGN_CENTER)
        self.l_user.SetFont(wx.Font(25, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Humor Sans"))

        self.Bind(wx.EVT_CLOSE, self.on_quit)
        #self.Show(True)

    def onMore(self,e, id=-1):
        self.amount = int(self.l_amount.GetLabelText()) + 1
        self.l_amount.SetLabel(str(self.amount))
        self.Layout()

    def onLess(self,e, id=-1):
        self.amount = int(self.l_amount.GetLabelText()) - 1
        if self.amount > 0:
            self.l_amount.SetLabel(str(self.amount))
            self.Layout()

    def GetAmount(self):
        return int(self.l_amount.GetLabelText())

    def on_quit(self, e):
        print "close"
        self.Destroy()


class Panel2 (wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, size=(480, 320))

        self.bitmap_1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap("./app/static/users.png", wx.BITMAP_TYPE_ANY))

        users = get_users()
        names = list()
        for user in users:
            if user.isshown:
                names.append(user.longname)


        self.but_names = list()
        i = 0
        for name in names:
            #480x320
            self.but = wx.Button(self, id=wx.ID_ANY, label=name, pos=(0,0+i*40), size=(400, 40))
            self.but.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Humor Sans"))
            self.but.Bind(wx.EVT_LEFT_DOWN, parent.onUser, id=self.but.Id)
            self.but_names.append(self.but)
            i += 1

        self.b_up = wx.Button(self, id=wx.ID_ANY, label=u"\u25B2", pos=(400,0), size=(80, 80))
        self.b_up.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Humor Sans"))
        self.b_up.Bind(wx.EVT_LEFT_DOWN, self.on_up, id=self.b_up.Id)

        self.b_down = wx.Button(self, id=wx.ID_ANY, label=u"\u25BC", pos=(400,240), size=(80, 80))
        self.b_down.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Humor Sans"))
        self.b_down.Bind(wx.EVT_LEFT_DOWN, self.on_down, id=self.b_down.Id)

        self.b_exit = wx.Button(self, id=wx.ID_ANY, label="X", pos=(400,120), size=(80, 80))
        self.b_exit.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Humor Sans"))
        self.b_exit.Bind(wx.EVT_LEFT_DOWN, parent.onExit, id=self.b_exit.Id)
        self.Bind(wx.EVT_CLOSE, self.on_quit)
        #self.Show(True)

    #This is bad programming :)
    def on_down(self,e , id=-1):
        for button in self.but_names:
            button.SetPosition((button.GetPosition()[0],button.GetPosition()[1]-320))
        self.Layout()

    def on_up(self,e , id=-1):
        for button in self.but_names:
            button.SetPosition((button.GetPosition()[0],button.GetPosition()[1]+320))
        self.Layout()

    def on_button_press(self,e, id=-1):
        print e.Id
        print id
        #if id == self.b_down.Id:

    def on_quit(self, e):
        print "close"
        self.Destroy()