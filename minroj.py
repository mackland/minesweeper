from tkinter import *
from time import *
from highscores import *
import random

#Satter upp hela programmet, hur stor ska planen va samt kontroll av anvandarinmatning
def skapa_plan(svarighetsgrad,meny_fonster,bredd=1,hojd=1,minor_fran_start=1):
    if svarighetsgrad == 'Latt':
        bredd = 9
        hojd = 9
        minor_fran_start = 10
        area = '400x400'
    elif svarighetsgrad == 'Normal':
        bredd = 16
        hojd = 16
        minor_fran_start = 40
        area = '600x600'
    elif svarighetsgrad == 'Expert':
        bredd = 30
        hojd = 16
        minor_fran_start = 99
        area = '800x600'
    else:
        if int(bredd) > 30 or int(bredd) < 9 or int(hojd) > 24 or int(hojd) < 9 or int(minor_fran_start) < 10 or int(minor_fran_start) > 668:
            messagebox.showinfo('Fel!','Det blev fel nar du angav bredd, hojd eller minor')
            return()
        else:
            bredd = int(bredd)
            hojd = int(hojd)
            minor_fran_start = int(minor_fran_start)
            area = str(bredd*24+100)+'x'+str(hojd*26+100) 
    
    plan = [([None]*(hojd)) for i in range(bredd)] #Spelplan med dimension bredd*hojd, skapar en Knapp i varje ruta
    for i in range(bredd):
        for k in range(hojd):
            plan[i][k] = Knapp()
    Minor = []
    while len(Minor) != int(minor_fran_start):
        b = random.randrange(0,bredd)
        h = random.randrange(0,hojd)
        if (b,h) not in Minor:
            plan[b][h].Mina = True
            Minor.append((b,h))

    spelInfo = [bredd,hojd,minor_fran_start,area,svarighetsgrad]
    spelPlaner = [plan, meny_fonster]
    
    start_minroj(spelPlaner,spelInfo)

#Satter upp den den grafiska spelplanen tillsammans med knapparna
def start_minroj(spelPlaner,spelInfo):
    starttid = time()
    bredd = spelInfo[0]
    hojd = spelInfo[1]
    minor_fran_start = spelInfo[2]
    area = spelInfo[3]
    
    spelInfo.append(starttid)

    meny_fonster = spelPlaner.pop()
    meny_fonster.destroy()
    
    spel_fonster = Tk()
    spel_fonster.title("Minroj")

    spel_fonster.geometry(area)
    spel_fonster.resizable(0, 0)

    spelPlaner.append(spel_fonster)
    
    Gameplan = Frame()
    Gameplan.place(in_=spel_fonster, anchor="c", relx=.5, rely=.5)
    
    flaggor = StringVar()
    flaggor.set('Antal minor kvar: '+str(minor_fran_start))
    FlagLabel = Label(spel_fonster,text='Antal minor kvar: ',textvariable=flaggor).pack()
    
    Minplan = [([]) for i in range(bredd)]
    spelPlaner.append(Minplan)

    for i in range(bredd):
        for k in range(hojd):
            a = (i, k)
            Minplan[i].insert(k, Button(Gameplan,text='   ', height = 1, width = 2,command = lambda a=a: knapp_klick(a,spelInfo,spelPlaner)))
            Minplan[i][k].bind('<Button-3>', lambda e,a=a: flagging(a,spelPlaner,spelInfo,flaggor,minor_fran_start))
            Minplan[i][k].grid(column=i,row=k)

#Satter ut flaggor om man hogerklickar, raknar antal flaggor pa plan
def flagging(a,spelPlaner,spelInfo,flaggor,minor_fran_start):
    bredd = spelInfo[0]
    hojd = spelInfo[1]
    plan =  spelPlaner[0]
    Minplan = spelPlaner[2]
    flaggade_rutor = 0
    if not plan[a[0]][a[1]].nedtryckt:
        if plan[a[0]][a[1]].Flag:
            plan[a[0]][a[1]].Flag = False
            Minplan[a[0]][a[1]].configure(text='   ')
        else:
            plan[a[0]][a[1]].Flag = True
            Minplan[a[0]][a[1]].configure(text=' F ')
        for i in range(bredd):
            for k in range(hojd):
                if plan[i][k].Flag == True:
                    flaggade_rutor+=1
        flaggor.set('Antal minor kvar: '+str(minor_fran_start-flaggade_rutor))

#Finns det en mina dar du klickade, om inte ska den roja rutan
def knapp_klick(a,spelInfo,spelPlaner):
    bredd = spelInfo[0]
    hojd = spelInfo[1]
    plan =  spelPlaner[0]
    Minplan = spelPlaner[2]
    
    if plan[a[0]][a[1]].Flag:
        return()
    else:
        if plan[a[0]][a[1]].Mina:
            for i in range(bredd):
                for k in range(hojd):
                    if plan[i][k].Mina:
                        Minplan[i][k].configure(text=' x ')
            SlutForlorade(spelPlaner[1])
        elif plan[a[0]][a[1]].nedtryckt==False:
            roj_ruta(a[0],a[1],spelInfo,spelPlaner)

#En knapp som finns i varje ruta, den haller koll pa om knappen blivit tryckt tidigare eller innehaller en mina
class Knapp():
    def __init__(self, Status = False, Mina = False, Flag = False):
        self.nedtryckt = Status
        self.Mina = False
        self.Flag = False

#Rojer spelplanen, kollar narliggande minor samt rojer ett stort falt ifall det behovs
def roj_ruta(x,y,spelInfo,spelPlaner):
    bredd = spelInfo[0]
    hojd = spelInfo[1]
    minor_fran_start = spelInfo[2]
    antal_rutor_tryckta = 0
    plan =  spelPlaner[0]
    Minplan = spelPlaner[2]

    antal_rutor = bredd*hojd-minor_fran_start
    plan[x][y].nedtryckt=True
    for i in range(bredd):
        for k in range(hojd):
            if plan[i][k].nedtryckt == True:
                antal_rutor_tryckta += 1

    antal_rutor_kvar = int(antal_rutor) - int(antal_rutor_tryckta)
    antal_minor = narliggande_minor(x,y,plan,spelInfo)
    if antal_minor>0:
        Minplan[x][y].configure(text = str(antal_minor))
        farg = rut_farg(antal_minor)
        Minplan[x][y].configure(fg = farg, bg = 'grey')
    else: #om det inte fanns nagra minor i narheten, roj ett storre falt
        Minplan[x][y].configure(state = DISABLED, bg = 'grey')
        if y<hojd-1 and x<bredd-1 and plan[x+1][y+1].nedtryckt == False and plan[x+1][y+1].Flag == False:
            roj_ruta(x+1,y+1,spelInfo,spelPlaner)
        if x<bredd-1 and y>0 and plan[x+1][y-1].nedtryckt == False and plan[x+1][y-1].Flag == False:
            roj_ruta(x+1,y-1,spelInfo,spelPlaner)
        if x<bredd-1 and plan[x+1][y].nedtryckt == False and plan[x+1][y].Flag == False:
            roj_ruta(x+1,y,spelInfo,spelPlaner)
        if x>0 and y<hojd-1 and plan[x-1][y+1].nedtryckt == False and plan[x-1][y+1].Flag == False:
            roj_ruta(x-1,y+1,spelInfo,spelPlaner)
        if y>0 and x>0 and plan[x-1][y-1].nedtryckt == False and plan[x-1][y-1].Flag == False:
            roj_ruta(x-1,y-1,spelInfo,spelPlaner)
        if x>0 and plan[x-1][y].nedtryckt == False and plan[x-1][y].Flag == False:
            roj_ruta(x-1,y,spelInfo,spelPlaner)
        if y>0 and plan[x][y-1].nedtryckt == False and plan[x][y-1].Flag == False:
            roj_ruta(x,y-1,spelInfo,spelPlaner)
        if y<hojd-1 and plan[x][y+1].nedtryckt == False and plan[x][y+1].Flag == False:
            roj_ruta(x,y+1,spelInfo,spelPlaner)
    if antal_rutor_kvar == 0:
        SlutVann(spelInfo,spelPlaner)

#Valjer ut en farg till texten efter antal minor runt rutan
def rut_farg(antal_minor):
    farger = ['blue','#009900','red','purple','maroon','#3399ff','grey','black']
    farg = farger[antal_minor-1]
    return(farg)

#Undersoker alla narliggande rutor efter minor
def narliggande_minor(x,y,plan,spelInfo):
    bredd = spelInfo[0]
    hojd = spelInfo[1]
    antal_minor = 0
    if x>0:
        if plan[x-1][y].Mina: #Kolla rutan ovanfor
            antal_minor += 1
    if x>0 and y>0:
        if plan[x-1][y-1].Mina: #Kolla rutan snett upp till vanster
            antal_minor += 1
    if x>0 and y<hojd-1:
        if plan[x-1][y+1].Mina: #Kolla rutan snett upp till hoger
            antal_minor += 1
    if x<bredd-1:
        if plan[x+1][y].Mina: #Kolla rutan nedanfor
            antal_minor += 1
    if x<bredd-1 and y>0:
        if plan[x+1][y-1].Mina: #Kolla rutan snett ned till vanster
            antal_minor += 1
    if y<hojd-1 and x<bredd-1:
        if plan[x+1][y+1].Mina: #Kolla rutan snett ned till hoger
            antal_minor += 1
    if y<hojd-1:
        if plan[x][y+1].Mina: #Kolla rutan till hoger
            antal_minor += 1
    if y>0:
        if plan[x][y-1].Mina: #Kolla rutan till vanster
            antal_minor += 1
    return(antal_minor)

def SlutForlorade(spel_fonster):
    messagebox.showinfo("Spelet ar slut","Du rakade ga pa en mina.")
    spel_fonster.destroy()
    Menu()

#Funktionen ger anvandaren mojlighet att skriva in sitt namn till highscorelistan
def SlutVann(spelInfo,spelPlaner):
    starttid = spelInfo.pop()
    bredd = spelInfo[0]
    hojd = spelInfo[1]    
    Svarighetsgrad = spelInfo[4]
    Minplan = spelPlaner[2]
    spel_fonster = spelPlaner[1]
    sluttid = time()
    nyTid = int(sluttid-starttid)

    for i in range(int(bredd)):
        for k in range(int(hojd)):
            Minplan[i][k].configure(state=DISABLED)

    frameVann = Tk()
    frameVann.title('Spelet ar slut')
    frameVann.geometry('200x120')
    frameVann.resizable(0, 0)
    GratLabel = Label(frameVann, text='Grattis, du rojde alla rutor pa '+str(nyTid)+' s.',padx=10,pady=10)
    GratLabel.grid(column =0, row =0,columnspan=2)
    if Svarighetsgrad != 'Anpassad':
        frameVann.geometry('200x120')
        NamnLabel = Label(frameVann, text='Namn:',padx=5,pady=5)
        NamnLabel.place(in_=frameVann,relx=.05,rely=.38)
    
        NamnEntry = Entry(frameVann)
        NamnEntry.place(in_=frameVann,relx=.3,rely=.4)

        okButton = Button(frameVann,text='OK',width = 10,command=lambda: highscores(nyTid,NamnEntry.get(),Svarighetsgrad,spel_fonster,frameVann),padx=2,pady=2)
        okButton.place(in_=frameVann,relx=.3,rely=.7)
    else:
        frameVann.geometry('280x120')
        TextLabel = Label(frameVann, text='Tyvarr finns ingen poanglista for anpassad.',padx=5,pady=5)
        TextLabel.place(in_=frameVann,relx=.05,rely=.38)
        
        spelaIgen = Button(frameVann, text='Spela igen', command = lambda: Avsluta(frameVann,spel_fonster,spela_igen = True))
        spelaIgen.place(in_=frameVann, relx=.22, rely=.70)
        
        knappAvsluta = Button(frameVann, text='Avsluta', command = lambda: Avsluta(frameVann,spel_fonster))
        knappAvsluta.place(in_=frameVann, relx=.58, rely=.70)

#visar lista med poang samt ger anvandaren mojlighet att spela igen eller avsluta programmet
def highscores(Tid, spelarnamn,Svarighetsgrad,spel_fonster,frameVann):
    spel_fonster.destroy()
    frameVann.destroy()
    
    framePoang = Tk()
    framePoang.title('Poanglista')
    framePoang.geometry('250x350')
    framePoang.resizable(0,0)
    
    Border = Frame(framePoang, bg = 'white',bd=3,relief=SUNKEN)
    Border.place(in_=framePoang, anchor="c", relx=.5, rely=.45)

    spelaIgen = Button(framePoang, text='Spela igen', command = lambda: Avsluta(framePoang,None,spela_igen = True))
    spelaIgen.place(in_=framePoang, relx=.22, rely=.87)

    knappAvsluta = Button(framePoang, text='Avsluta', command = framePoang.destroy)
    knappAvsluta.place(in_=framePoang, relx=.58, rely=.87)
    
    Poanglista = oppna_lista(str(Svarighetsgrad))
    ny_poang(Tid,spelarnamn,Poanglista) 
    for i in range(0,len(Poanglista),2):
        Label(Border,text=str((int((i+3)/2)))+'. '+str(Poanglista[i])+' - '+str(Poanglista[i+1]),bg='white').pack(pady=3,padx=20,anchor='w')
    spara_poang(Poanglista,str(Svarighetsgrad))

def Avsluta(frame,spel_fonster, spela_igen=False):
    if spel_fonster != None:
        spel_fonster.destroy()
    frame.destroy()
    if spela_igen == True:
        Menu()

#Menyn till hela programmet, tar emot anvandarens inamtning
def Menu():
    meny_fonster = Tk()
    meny_fonster.title('Menu')
    meny_fonster.focus()
    meny_fonster.resizable(0,0)
    
    svarighetsgrad = StringVar()
    svarighetsgrad.set('Latt')

    lattRadio = Radiobutton(meny_fonster, text='Easy\n10 minor\n9 x 9 rutor',justify=LEFT, variable = svarighetsgrad, value='Latt')
    normalRadio = Radiobutton(meny_fonster, text='Normal\n40 minor\n16 x 16 rutor',justify=LEFT, variable = svarighetsgrad, value='Normal')
    expertRadio = Radiobutton(meny_fonster, text='Expert\n99 minor\n16 x 30 rutor',justify=LEFT, variable = svarighetsgrad, value='Expert')
    anpassadRadio = Radiobutton(meny_fonster, text='Anpassad', variable=svarighetsgrad, value='Anpassad')

    lattRadio.grid(column=0,row=2,padx=5,rowspan = 3,sticky=SW)
    normalRadio.grid(column=0,row=5,padx=5,rowspan = 3,sticky=NW)
    expertRadio.grid(column=0,row=8,padx=5,rowspan = 3,sticky=NW)
    anpassadRadio.grid(column=1,row=4,columnspan=8,padx=2,sticky=N)

    minorLabel = Label(meny_fonster, text='Antal Minor (10-668):')
    hojdLabel = Label(meny_fonster,text= 'Hojd (9-24):')
    breddLabel = Label(meny_fonster,text= 'Bredd (9-30):')

    bredd_e = Entry(meny_fonster, width = 5)
    bredd_e.insert(0,9)
    hojd_e = Entry(meny_fonster, width = 5)
    hojd_e.insert(0,9)
    antal_minor_e = Entry(meny_fonster, width = 5)
    antal_minor_e.insert(0,10)

    avsluta = Button(meny_fonster,text='Avsluta', command=meny_fonster.destroy,width=10)
    spela = Button(meny_fonster,text='Spela',command=lambda: skapa_plan(svarighetsgrad.get(),meny_fonster,bredd_e.get(),hojd_e.get(), antal_minor_e.get()), width=10)

    breddLabel.grid(column=2,row=5,padx=1,sticky = NW)
    hojdLabel.grid(column=2,row=6,padx=1,sticky = W)
    minorLabel.grid(column=2,row=7,padx=1,sticky = NW)

    bredd_e.grid(column=3,row=5,padx=5,sticky=S)
    hojd_e.grid(column=3,row=6,padx=5,sticky=E)
    antal_minor_e.grid(column=3,row=7,padx=5,sticky=N)

    avsluta.grid(row=12,column=2,padx=5,pady=5,sticky=W)
    spela.grid(row=12,column=1,padx=5,pady=5,sticky=W)

    meny_fonster.mainloop()

Menu()
