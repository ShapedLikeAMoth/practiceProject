#DT is Date and Time file

from datetime import datetime

def timeDate():
    now = datetime.now()

    rok = now.year
    mies = now.month
    dzien =now.day

    godz = now.hour
    minu = now.minute
    seku = now.second
    return(rok, mies, dzien, godz, minu, seku)


teraz = []
teraz = timeDate()
print (teraz)
