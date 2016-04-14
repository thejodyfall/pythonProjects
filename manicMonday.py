
import datetime

class isItMonday():

    def __init__(self):
       print("Is it Monday?\n")
        
    def whatDayisIt(self):
        if datetime.datetime.today().weekday() == 0:
            print "Yes"
        else:
            print "No"

isIt_Monday = isItMonday()
isIt_Monday.whatDayisIt()

      
