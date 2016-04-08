################################################################
#                           Settings                           #
################################################################
#
# This is the settings file!
# Edit settings to your preference and restart the device
#
# The default for everything is False,
# default numbers are given in comments
#
# Web interface colours and styles
# can be changed in app/static/style.css
#
# Gui Backgrounds can be replaced in gui/ folder (.png files)
#
################################################################


class Settings:

    def __init__(self):
        ##User Interaction
        #Gui
        self.hideGuiList = False    #Show the consumers in the gui
        self.disableRFID = False    #Disable RFID Reading
        self.allowHiding = False    #Allow a user to hide from the gui consumer list
        self.onlyOneDrink = False   #Hide selection for amount in the gui
        self.drinkLimit = 20        #Max amount of consumptions in the gui (default 20)
        #Web Interface
        self.disableWebIF = False   #Disable Web Interface
        self.disableStats = False   #Disable All Statistics

        ##Payment Incentives
        #Money Limit
        self.autoBlack = True       #Automatically block user if money owed > limit
        self.autoUnblack = True     #Automatically unblock user if money owed < limit
        self.blockLimit = 150       #Money limit for automatic blocking (default 150)
        #Mail Spam
        self.autoAnnoy = False      #Automatically send payment eMails
        self.annoyDays = 20         #Automatically send mails every x days (default 20)
        self.annoyLimit = 100       #Money limit for autoAnnoy (default 100)

        ##Developer Settings
        self.debug = False          #Show debug output in console

settings = Settings()