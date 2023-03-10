import datetime


t = datetime.date.today().strftime("%d.%m.%Y")
print(t)
print(datetime.datetime.strptime(t, "%d.%m.%Y"))

