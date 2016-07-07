class User:
   
    def __init__(self):
        self.id=0;
        self.name=""
        self.password=""
        self.longname=""
        self.email=""
        self.rfid_id=""
        self.isblack=False
        self.isbaron=False
        self.isshown=False
        self.autoblack=False
        self.onlyrfid=False


    def __str__(self):
        s = "User:"
        if self.id:
            s = "%s %d" % (s, self.id)
        else:
            s = "%s, None" % s

        if self.name:
            s = "%s, %s" % (s, self.name)
        else:
            s = "%s, None" % s

        if self.password:
            s = "%s, %s" % (s, self.password)
        else:
            s = "%s, None" % s

        if self.longname:
            s = "%s, %s" % (s, self.longname)
        else:
            s = "%s, None" % s

        if self.email:
            s = "%s, %s" % (s, self.email)
        else:
            s = "%s, None" % s

        if self.rfid_id:
            s = "%s, %s" % (s, self.rfid_id)
        else:
            s = "%s, None" % s

        if self.isblack is None:
            s = "%s, None" % s
        else:
            if self.isblack is 0 or self.isblack is False:
                s = "%s, False" % s
            else:
                s = "%s, True" % s

        if self.isbaron is None:
            s = "%s, None" % s
        else:
            if self.isbaron is 0 or self.isbaron is False:
                s = "%s, False" % s
            else:
                s = "%s, True" % s

        if self.isshown is None:
            s = "%s, None" % s
        else:
            if self.isshown is 0 or self. isshown is False:
                s = "%s, False" % s
            else:
                s = "%s, True" % s

        if self.autoblack is None:
            s = "%s, None" % s
        else:
            if self.autoblack is 0 or self. autoblack is False:
                s = "%s, False" % s
            else:
                s = "%s, True" % s

        if self.onlyrfid is None:
            s = "%s, None" % s
        else:
            if self.onlyrfid is 0 or self. onlyrfid is False:
                s = "%s, False" % s
            else:
                s = "%s, True" % s

        return s
