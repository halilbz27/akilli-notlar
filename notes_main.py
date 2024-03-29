from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import*

import json

app = QApplication([])

#2.hafta
"""notes ={ SİL
    "Hoş Geldiniz": {
        "metin" : "Bu dünyanın en iyi not uygulaması",
        "etiketler" : ["iyilik","talimat"]
    }
}
with open("notes_data.json","w") as file:
    json.dump(notes,file)"""

#--

'''Uygulama arayüzü'''
#uygulama penceresi parametreleri
notes_win = QWidget()
notes_win.setWindowTitle('Akıllı notlar')
notes_win.resize(900, 600)

#uygulama penceresi widget'ları
list_notes = QListWidget()
list_notes_label = QLabel('Notların listesi')

button_note_create = QPushButton('Not oluştur') #"notun adını girin" alanlı bir pencere belirir
button_note_del = QPushButton('Notu sil')
button_note_save = QPushButton('Notu kaydet')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Etiketi giriniz...')
field_text = QTextEdit()#Büyük soldaki yazi
 
button_tag_add = QPushButton('Nota ekle')
button_tag_del = QPushButton('Nottan çıkar')
button_tag_search = QPushButton('Notları etikete göre ara')

list_tags = QListWidget()
list_tags_label = QLabel('Etiket listesi')

#anahat düzenine göre widget'ların konumu
layout_notes = QHBoxLayout()#genel yatay hizalama
col_1 = QVBoxLayout()#1.dikey hizalamam(1.sutun)
col_1.addWidget(field_text)#ilk dikeye büyük text alanını ekliyoruz.

col_2 = QVBoxLayout()#ikinci dikey çizgim herşeyi buna ekliyoruz
col_2.addWidget(list_notes_label)#sağ üstteki listeleri ekliyoruz
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()#butonları hizalamak için yatay sutun ekledim. 1.yatay
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)

row_2 = QHBoxLayout()#2.yatay
row_2.addWidget(button_note_save)

col_2.addLayout(row_1)#2.dikey sutuna ekliyoruz yatayları
col_2.addLayout(row_2)#2.dikey sutuna ekliyoruz yatayları

col_2.addWidget(list_tags_label)#sağ alttaki 3 text alanını ekliyoruz 2.dikeye
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()#butonlar için yatay çizgi ekliyoruz.
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)

row_4 = QHBoxLayout()#butonlar için yatay çizgi ekliyoruz.
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)#2.dikey sutuna ekliyoruz yatayları
col_2.addLayout(row_4)

#ekranı 3'e bölüyoruz
layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)

#2.hafta - Fonksiyonlar
def add_note():#yeni not eklemek için
    note_name, ok =QInputDialog.getText(notes_win,"Not ekle","Notun adı: ")
    if ok and note_name !="": #ok basıldı ve boş değilse
        notes[note_name] ={"metin": "", "etiketler": []} #sözlük yapısını oluştur.
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["etiketler"])
        print(notes)

def save_note(): #seçilen notu güncelleyip kaydeder.
    if list_notes.selectedItems(): #bir not seçili ise
        key = list_notes.selectedItems()[0].text()
        notes[key]["metin"] =field_text.toPlainText()#soldaki düzenleme metnini al.
        with open("notes_data.json","w") as file:
            json.dump(notes,file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Kaydedilecek not seçili değil")

def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["metin"])#soldaki büyük alana notu getir.
    list_tags.clear()
    list_tags.addItems(notes[key]["etiketler"])

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json","w") as file:
            json.dump(notes,file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Silinecek not seçili değil")

"""NOT ETİKETİYLE ÇALIŞMA"""
def add_tag():
    if list_notes.selectedItems():#list nottan not seçili ise
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()#tag alanındaki etili okur
        if not tag in notes[key]["etiketler"]:
            notes[key]["etiketler"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json","w") as file:
            json.dump(notes,file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Etiket eklemek için not seçili değil")

def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["etiketler"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["etiketler"])
        with open("notes_data.json","w") as file:
            json.dump(notes,file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Silinecek etiket seçili değil")

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() =="Notları etikete göre ara" and tag:
        notes_filtered={}
        for note in notes:
            if tag in notes[note]["etiketler"]:
                notes_filtered[note]=notes[note]
        
        button_tag_search.setText("Aramayı temizle")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)

    elif button_tag_search.text() =="Aramayı temizle":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Notları etikete göre ara")
    else:
        pass



#uygulamayı başlatma 
button_tag_search.clicked.connect(search_tag)
button_tag_del.clicked.connect(del_tag)#3.hafta
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
list_notes.itemClicked.connect(show_note)#seçtiğim an o fonk çağır
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)#3.hafta

notes_win.show()
#2.hafta
with open("notes_data.json","r") as file:
    notes=json.load(file)
list_notes.addItems(notes)


#--
app.exec_()
