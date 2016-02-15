#/bin/python
import wx
from app import app
from os import urandom
from app import gui
import thread

if __name__ == '__main__':
    #start gui
    #wx = wx.App()
    #gui.MainWindow(None)

    #thread.start_new_thread(wx.MainLoop,())

    # start flask
    app.secret_key = urandom(24)
    app.run(debug=True)

#app.run()
