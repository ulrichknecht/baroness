#!/usr/bin/python
import wx
from app import app
from os import urandom
from app import gui
import thread
import logging
from app import settings
from app import datalog
from app import plot

def rungui():
    wxx = wx.App()
    gui.MainWindow(None)
    wxx.MainLoop()

if __name__ == '__main__':

    #logging!
    logfile = "baroness.log"
    logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
    #logging.basicConfig(level=logging.DEBUG)
    logging.info("Baroness started!")
    print "Baroness started: logging to ", logfile

    #start data logging
    if settings.settings.fridgeLogging:
        logger = datalog.DataLogger()

    #start plot thread
    plotter = plot.Plotter()

    #start gui
    #wx = wx.App()
    #gui.MainWindow(None)
    #thread.start_new_thread(wx.MainLoop,())
    thread.start_new_thread(rungui,())

    # start flask
    app.secret_key = urandom(24)
    app.run(host="0.0.0.0")

#app.run()
