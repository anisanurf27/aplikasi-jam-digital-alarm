from tkinter import*
import time
from tkinter.ttk import Combobox
import pygame

class Jam:
    def __init__(self, parent):
        self.parent=parent
        self.frameAlarm=Frame(parent)
        self.framLayar=Frame(parent)
        self.frameHapus=Frame(parent)
        self.frameNote=Frame(parent)

        self.teksTombol=StringVar(value='set')

        self.fileMusik='Hysteria.mp3'
        self.antrianAlarm=[]
        self.antrianCatatan=[]
        self.alarmHidup=False

        self.komponen()
        self.layarAlarm()
        self.scrollBar()
        self.buatComboBox()
        self.catatan()
        self.buatTombol()
        self.perbaui()

    def komponen(self):
        self.teksJam=StringVar()

        layarJam=Frame(self.parent,bd=10)
        layarJam.pack()

        self.jam=Label(layarJam,textvariable=self.teksJam,font=('Helvetica',40,'bold'),bg="light blue",fg="blue")
        self.jam.pack()

        self.teks=Label(text="Anisa Nur Fadhilah (3.34.21.0.05)", bg='Light Green')
        self.teks.pack()

    def scrollBar(self):
        scroll=Scrollbar(self.framLayar)
        scroll.grid(row=0,column=1, sticky=N+S)
        scroll.config(command=self.layar.yview)
        self.layar.config(yscrollcommand=scroll.set)

    def catatan(self):
        Label(self.frameNote,text='Catatan : ').grid(row=0,column=0)
        self.kolomCatatan=Entry(self.frameNote,width=17)
        self.kolomCatatan.grid(row=0,column=1)

        self.frameNote.pack()

    def perbaui(self):
        datJam=time.strftime("%H:%M:%S",time.localtime())

        self.jam = time.strftime("%H",time.localtime())
        self.menit = time.strftime("%M",time.localtime())
        detik = time.strftime("%S",time.localtime())

        cocok = self.jam + ' : ' + self.menit

        if len(self.antrianAlarm) :
            if  cocok==self.antrianAlarm[0]and detik==('00'):
                alarm=self.antrianCatatan.pop(0)
                self.teksTombol.set('stop')
                self.pemberitahuan = "waktunya " + alarm
                if self.pemberitahuan != "waktunya Tanpa Catatan." :
                    self.teks.config(text= self.pemberitahuan)
                self.antrianAlarm.pop(0)
                self.updateLayar()
                self.alarmHidup = True
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(self.fileMusik)
                pygame.mixer.music.play()

        if self.alarmHidup and pygame.mixer.music.get_busy()==False :
            self.perintahSetAlarm()

        self.teksJam.set(datJam)
        self.timer = self.parent.after(1000,self.perbaui)

    def buatComboBox(self):
        Label(self.frameAlarm, text='Jam : ').grid(row=0,column=0)
        self.alarmJam = StringVar()
        self.comboJam = Combobox(self.frameAlarm, textvariable=self.alarmJam,
                                state='readonly', width=2)
        self.comboJam['values'] = ('00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15',
                                     '16','17','18','19','20','21','22','23')
        self.comboJam.current(0)
        self.comboJam.grid(row=0,column=1)

        Label(self.frameAlarm, text='  Menit : ').grid(row=0,column=2)
        self.alarmMenit = StringVar()
        self.comboMenit = Combobox(self.frameAlarm, textvariable=self.alarmMenit,
                                state='readonly', width=2)
        self.comboMenit['values'] = ('00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15',
                                     '16','17','18','19','20','21','22','23','24','25','26','27','28','29','30',
                                     '31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46',
                                      '47','48','49','50','51','52','53','54','55','56','57','58','59')
        self.comboMenit.current(0)
        self.comboMenit.grid(row=0,column=3)

        self.frameAlarm.pack(pady=3)

    def buatTombol(self):
        self.tombolSet = Button(self.frameNote,textvariable=self.teksTombol,command=self.perintahSetAlarm).grid(row=0,column=2)
        self.kolomHapus = Entry(self.frameHapus, width=5)
        self.kolomHapus.grid(row=0,column=0)
        self.tombolSet = Button(self.frameHapus, text='Hapus', command=self.perintahHapus).grid(row=0, column=1)

        self.frameHapus.pack()

    def perintahSetAlarm(self):
        if self.teksTombol.get() == 'set':
            masukan = self.comboJam.get()+' : '+self.comboMenit.get()
            tidakAda = True
            for i in self.antrianAlarm:
                if i == masukan:
                    tidakAda=False
            if tidakAda :
                self.tentukanUrutan(angka=masukan)
            self.updateLayar()
        else:
            self.teksTombol.set('set')
            self.teks.config(text="Anisa Nur Fadhilah (3.34.21.0.05)", bg='Light Green')
            self.alarmHidup=False
            try:
                pygame.mixer.music.stop()
            except:
                pass

    def layarAlarm(self):
        self.layar = Text(self.framLayar, height=5, width=35, state=DISABLED)
        self.layar.grid(row=0,column=0)
        self.framLayar.pack()

    def updateLayar(self):
        masukan=''
        for i in range(len(self.antrianAlarm)) :
            masukan += str(i+1)+". "+ self.antrianAlarm[i]+' -> '+self.antrianCatatan[i]+'\n'
        self.layar.config(state=NORMAL)
        self.layar.delete('1.0',END)
        self.layar.insert(END, masukan)
        self.layar.config(state=DISABLED)

    def perintahHapus(self):
        try:
            for i in range(len(self.antrianAlarm)) :
                if int(self.kolomHapus.get())-1 == i :
                    self.antrianAlarm.pop(i)
                    self.updateLayar()
                    break
        except :
            pass

    def tentukanUrutan(self, angka=0):
        if angka != 0 :
            self.antrianCatatan.append(self.kolomCatatan.get())
            self.antrianAlarm.append(angka)
        jarakJamPositif = []
        jarakJamNegatif = []
        convertInt = []
        antrianBaruPositif = []
        antrianBaruNegatif = []
        penampungCatatan = []

        for i in self.antrianAlarm :
            angka = ''
            for j in i :
                if j != ':' and j != ' ' :
                    angka += j
            convertInt.append(angka)
            jarak = int(self.jam + self.menit) - int(angka)
            jarak *= -1

            if jarak <= 0:
                jarakJamPositif.append(jarak)
            elif jarak > 0 :
                jarakJamNegatif.append(jarak)

        jarakJamPositif.sort()
        jarakJamNegatif.sort()

        for i in jarakJamPositif :
            for j in range(len(convertInt)) :
                jarak = int(self.jam + self.menit) - int(convertInt[j])
                jarak *= -1
                if i == jarak :
                    antrianBaruPositif.append(self.antrianAlarm[j])
                    catatan =self.antrianCatatan[j]
                    if catatan == '' or catatan==' ' or catatan=='  ' :
                        catatan = 'Tanpa Catatan'
                    penampungCatatan.append(catatan)

        for i in jarakJamNegatif :
            for j in range(len(convertInt)) :
                jarak = int(self.jam + self.menit) - int(convertInt[j])
                jarak *= -1
                if i == jarak :
                    antrianBaruNegatif.append(self.antrianAlarm[j])
                    catatan = self.antrianCatatan[j]
                    if catatan == '' or catatan==' ' or catatan=='  ' :
                        catatan = 'Tanpa Catatan'
                    penampungCatatan.append(catatan)

        self.antrianAlarm = antrianBaruNegatif+antrianBaruPositif
        self.antrianCatatan = penampungCatatan

if __name__ == '__main__':
    root = Tk()
    root.title("jam digital")
    app = Jam(root)
    root.mainloop()
