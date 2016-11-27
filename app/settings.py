# -*- coding: utf-8 -*-
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

from fridge import Fridge, Sensor

class Settings:

    def __init__(self):
        ##User Interaction
        #Gui
        self.hideGuiList = False    #Show the consumers in the gui
        self.enableRFID = False     #Enable RFID Reading
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

        ##Email
        #Login data and server
        self.SMTPserver = "smtp.gmail.com:587"        #Mailserver URL
        self.mailUsername = "bier1baroness"           #Username for the mailserver
        self.mailPassword = "test11test11"            #Password for the User on the mailserver
        self.mailFromName = "bier1baroness@gmail.com" #From filed in mail header
        #Standard Texts
        self.singleMessageStandardSubject = u"Baroness - Bierrechnung"
        self.singleMessageStandardText = u"Hallo %%longname%%\ndu hast %%dept%%€ Schulden.\nBitte überweise diesen Betrag an das Konto:\n\n%%if_is_black%%Weil du zu hohe Schulden hast, bist du geschwärzt%%end_if_is_black%%\nLiebe Grüße,\nDein Bierbaron"
        self.masMessageStandardSubject = u"Baroness - Bierrechnung"
        self.masMessageStandardText = u"Hallo %%longname%%\ndu hast %%dept%%€ Schulden.\nBitte überweise diesen Betrag an das Konto:\n\n%%if_is_black%%Weil du zu hohe Schulden hast, bist du geschwärzt%%end_if_is_black%%\nLiebe Grüße,\nDein Bierbaron"

        ##Data Logging
        #Fridge Temperature
        self.fridgeLogging = False  #Log the fridge temperature (connect temp. sensors before enabling)
        self.fridgeTime = 300       #Write fridge temp to file every x seconds
        self.fridgeLength = 30      #Length of data log span in days

        ##Developer Settings
        self.debug = False          #Show debug output in console

        ##Data Logging - Fridges
        self.fridges = list()       #Do not edit

        #Create an antialcoholic fridge (Antikühlschrank) with 3 sensors (top, middle and bottom temp.)
        new_f = Fridge("Antikühlschrank")                      #make new fridge
        new_f.add_sensor(Sensor("Temperatur Oben", "1"))       #add sensor 1 as top
        new_f.add_sensor(Sensor("Temperatur Mitte", "2"))      #add sensor 2 as middle
        new_f.add_sensor(Sensor("Temperatur Unten", "3"))      #add sensor 3 as bottom
        self.fridges.append(new_f)                             #append to the list of fridges

        #Create an alcoholic fridge with 3 sensors             #add more fridges as you like
        new_f = Fridge("Bierkühlschrank")
        new_f.add_sensor(Sensor("Temperatur Oben", "4"))
        new_f.add_sensor(Sensor("Temperatur Mitte", "5"))
        new_f.add_sensor(Sensor("Temperatur Unten", "6"))
        self.fridges.append(new_f)

settings = Settings()
