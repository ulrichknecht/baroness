#!/usr/bin/python
import wx
from app import app
from os import urandom
from app import gui
import thread
import logging

if __name__ == '__main__':

    #logging!
    logfile = "baroness.log"
    #logging.basicConfig(filename=logfile, level=logging.WARNING)
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Baroness started!")
    print "Baroness started: logging to ", logfile


    #start gui
    wx = wx.App()
    gui.MainWindow(None)
    thread.start_new_thread(wx.MainLoop,())

    # start flask
    app.secret_key = urandom(24)
    app.run(host="0.0.0.0")

#app.run()
