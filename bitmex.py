import bitmex
from tkinter import *
from datetime import timedelta
import time as t
import uuid

r = Tk()
r.title('Bitmex Slope Script')

sprice = 0.0
intchange = 0.0
quantity = 0.0
symbol = ''
direction = ''
apikey = ''
apisec = ''
test = True

def smain():
    global sprice
    global intchange
    global quantity
    global symbol
    global direction
    global apikey
    global apisec
    global test
    client = bitmex.bitmex(test=test, api_key=apikey, api_secret=apisec)
    currentprice = sprice
    idem = uuid.uuid4().hex
    client.Order.Order_new(symbol=symbol, side=direction, clOrdID=idem, orderQty=quantity, price=currentprice).result()
    print ('Placed order at price of ' + str(currentprice) + '\nPrice change of ' + str(intchange) + ' will take effect every 5 minutes')
    while True:
        t.sleep(300)
        currentprice = currentprice + intchange
        print ('Amending order price to ' + str(int(currentprice)))
        client.Order.Order_amend(origClOrdID=idem, price=int(currentprice)).result()

authframe = Frame(r)
authframe.pack(anchor='w')
keyframe = Frame(authframe)
keyframe.pack(anchor='w')
Label(keyframe, text='API Key').pack(side=LEFT)
key1 = Entry(keyframe, width=26)
key1.pack(side=LEFT, padx=20)
secretframe = Frame(authframe)
secretframe.pack(anchor='w')
Label(secretframe, text='API Secret').pack(side=LEFT)
sec1 = Entry(secretframe, width=53)
sec1.pack(side=LEFT, padx=7)

optframe = Frame(r)
optframe.pack(anchor='w', pady=15)
symframe = Frame(optframe)
symframe.pack(anchor='w')
Label(symframe, text='Symbol').pack(side=LEFT)
sym1 = Entry(symframe, width=10)
sym1.insert(0, 'XBTUSD')
sym1.pack(side=LEFT, padx=20)
qframe = Frame(optframe)
qframe.pack(anchor='w')
Label(qframe, text='Quantity').pack(side=LEFT)
q1 = Entry(qframe, width=10)
q1.pack(side=LEFT, padx=14)
dframe = Frame(optframe)
dframe.pack(anchor='w')
Label(dframe, text='Direction').pack(side=LEFT)
dirvar = StringVar()
Radiobutton(dframe, text='Buy', variable=dirvar, value='Buy').pack(side=LEFT)
Radiobutton(dframe, text='Sell', variable=dirvar, value='Sell').pack(side=LEFT)
dirvar.set('Sell')
tframe = Frame(optframe)
tframe.pack(anchor='w')
Label(tframe, text='Server').pack(side=LEFT)
testvar = BooleanVar()
Radiobutton(tframe, text='Testnet', variable=testvar, value=True).pack(side=LEFT)
Radiobutton(tframe, text='Bitmex', variable=testvar, value=False).pack(side=LEFT)
testvar.set(True)


slopeframe = Frame(r)
slopeframe.pack(anchor='w')
timeframe = Frame(slopeframe)
timeframe.pack(side=LEFT, anchor='w')
sframe = Frame(timeframe)
sframe.pack(anchor='w')
Label(sframe, text='Start Time').pack(anchor='w')
Label(sframe, text='H').pack(side=LEFT)
s1 = Entry(sframe, width=5)
s1.pack(side=LEFT)
Label(sframe, text='M').pack(side=LEFT)
s2 = Entry(sframe, width=5)
s2.pack(side=LEFT)
Label(sframe, text='S').pack(side=LEFT)
s3 = Entry(sframe, width=5)
s3.pack(side=LEFT)
eframe = Frame(timeframe)
eframe.pack(anchor='w')
Label(eframe, text='End Time').pack(anchor='w')
Label(eframe, text='H').pack(side=LEFT)
e1 = Entry(eframe, width=5)
e1.pack(side=LEFT)
Label(eframe, text='M').pack(side=LEFT)
e2 = Entry(eframe, width=5)
e2.pack(side=LEFT)
Label(eframe, text='S').pack(side=LEFT)
e3 = Entry(eframe, width=5)
e3.pack(side=LEFT)
priceframe = Frame(slopeframe)
priceframe.pack(side=LEFT, anchor='w', padx=15)
iframe = Frame(priceframe)
iframe.pack(anchor='w')
Label(iframe, text='Start Price').pack(side=LEFT)
ifr1 = Entry(iframe, width=10)
ifr1.pack(side=LEFT, padx=16)
fframe = Frame(priceframe)
fframe.pack(anchor='w')
Label(fframe, text='End Price').pack(side=LEFT)
ffr1 = Entry(fframe, width=10)
ffr1.pack(side=LEFT, padx=19)

def initscript():
    global sprice
    global intchange
    global quantity
    global symbol
    global direction
    global apikey
    global apisec
    global test
    starttime = timedelta(hours=int(s1.get()), minutes=int(s2.get()), seconds=int(s3.get()))
    endtime = timedelta(hours=int(e1.get()), minutes=int(e2.get()), seconds=int(e3.get()))
    runtime = endtime - starttime
    runmin = runtime.total_seconds() / 60
    sprice = float(ifr1.get())
    priceinc = float(ffr1.get()) - float(ifr1.get())
    slope = priceinc/runmin
    intchange = slope*5
    quantity = float(q1.get())
    symbol = sym1.get()
    direction = dirvar.get()
    test = testvar.get()
    apikey = key1.get()
    apisec = sec1.get()
    smain()

Button(r, text='Start Script', width=25, command=initscript).pack(pady=10)
mainloop()
