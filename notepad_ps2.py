#step 1: import semua module
#pyqt5 -> modules buat bikin app
#qtcore -> install semua core pyqt5
#qtwidgets -> bikin app, halaman app, btn, label, dll
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout

#json -> file txt notepad
import json


#step 2: bikin app dan halaman utama
#list notes
notes = []
#app
app = QApplication([])

#halaman utama
notes_win = QWidget()
#set title
notes_win.setWindowTitle('Notepad')
#ukuran
notes_win.resize(900, 600)


#step 3: bikin btn, label, list notes, tempat text
#bikin dulu list notes
list_notes = QListWidget()
list_notes_label = QLabel('list catatan')

#btn notes
button_note_create = QPushButton('Create note') #a window with field "Enter note name" appears
button_note_del = QPushButton('Delete note')
button_note_save = QPushButton('Save note')

#bikin tag
list_tags = QListWidget()
list_tags_label = QLabel('List tags')
field_tag = QLineEdit('')
field_tag.setPlaceholderText('Masukin tag...')
button_tag_add = QPushButton('Add to note')
button_tag_del = QPushButton('Unpin from note')
button_tag_search = QPushButton('Search notes by tag')


field_text = QTextEdit()

#step 4: layout -> penempatan text, label, btn
#arrangement of widgets by layouts
layout_notes = QHBoxLayout() #layout utama
col_1 = QVBoxLayout() #kolom 1
col_1.addWidget(field_text)


col_2 = QVBoxLayout() #kolom 2
#list notes
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
#bkin 2 row untuk btn, row 1 berisikan btn create dan del
#row 2 berisikan btn save
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)

#row 1 dan row 2 harus ditaruh ke dalam col 2
col_2.addLayout(row_1)
col_2.addLayout(row_2)

#list tag
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

#btn tag, bikin 2 row
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

#btn tag row di taruh ke dalam c2
col_2.addLayout(row_3)
col_2.addLayout(row_4)

#nambahin layout c1 dan c2 ke dalam layout notes utama
layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
#set layout utama ke dalam screen
notes_win.setLayout(layout_notes)


#App functionality
#Working with note text
# 1. fungsi u/ menambahkan note
def add_note():
    #ok -> tombol ok, kita mau tau apakah kita udah pencet tombol ok / belom
    note_name, ok = QInputDialog.getText(notes_win, "Add note", "Note name: ")
    #deteksi jika kita sudah pencet tombol ok dan note name != kosong
    if ok and note_name != "":
        #kita buat list kosong
        note = list()
        #list yang berisikan -> judul, isi, tag
        note = [note_name, '', []]
        #masukin list note judul, isi, tag ke dalam list notes general
        notes.append(note)
        #untuk menammpilkan catatan note terbaru -> list notes
        #list notes -> QListWidget
        list_notes.addItem(note[0])
        #untuk menampilkan tag pada catatan terbaru -> list tags
        #list tags-> Qlistwidget
        list_tags.addItems(note[2])
        #tampilin hasil notes yg ada di terminal
        print(notes)
        #taruh ke dalam file txt
        with open(str(len(notes)-1)+".txt", "w") as file:
            file.write(note[0]+'\n')

# 2. fungsi u/ tampilin isi dari note2 yg kita pilih
def show_note():
    #kita mendeteksi note mana yg kita pilih
    #lalu kita ambil judul note nya -> key
    key = list_notes.selectedItems()[0].text()
    print(key)
    #mesin akan mengecek untuk setiap note yang ada di dalam list notes
    for note in notes:
        #jika ada note dengan judul note yang kita pilih
        if note[0] == key:
            #tampilin isi dari text nya
            #kenapa [1]? karena mengikuti note = [note_name, '', []]
            #note = [judul note, 'isi note', [list tag]]
            #karena mau menampilkan isi note, maka kita pilih [1]
            field_text.setText(note[1])
            list_tags.clear()
            #begitupula sama tags
            tag = note[2]
            list_tags.addItems(tag)

# 3. fungsi u/ menyimpan note
def save_note():
    #deteksi apakah ada note yang kita pilih
    if list_notes.selectedItems():
        #cari judul note dari note yg kita pilih
        key = list_notes.selectedItems()[0].text()
        #nomor file txt
        index = 0
        #untuk setiap note yg ada di dalam list notes
        for note in notes:
            #jika ada note yang punya judul yg sama dgn note yg kita pilih
            if note[0] == key:
                #simpan apapun kalimat yg ada di dalam field text
                #ke dalam note[1]
                #toPlainText -> mendeteksi kalimat yg 
                #ada di dalam field text
                note[1] = field_text.toPlainText()
                #simpan ke dalam file txt
                with open(str(index)+".txt", "w") as file:
                    file.write(note[0]+'\n')
                    file.write(note[1]+'\n')
                    for tag in note[2]:
                        file.write(tag+' ')
                    file.write('\n')
            index += 1
        print(notes)
    else:
        print("Note to save is not selected!")


# 4. fungsi untuk del note
def del_note():
    #cek apakah ada note yang dipilih oleh cursor
    if list_notes.selectedItems():
        #ambil judul note nya
        key = list_notes.selectedItems()[0].text() #note yang dipilih
        #cek, untuk setiap note yang ada di dalam notes
        for note in notes:
            #jika ada catatan dalam notes punya judul yg sama
            if note[0] == key:
                #clear semua
                list_tags.clear()
                field_tag.clear()
                #masukan list yg sudah diperbarui
                #dengan cara take item row yang kita klik pada saat itu
                list_notes.takeItem(list_notes.currentRow())
                #remove dalam notes
                notes.remove(note)
        #notes=> note=["A", "aloheuvue", ["asal"]]
        with open(str(len(notes)-1)+".txt", "w") as file:
            file.write(note[0]+'\n')
        print(notes)
    else:
        print("Please select a note!")


#Working with note tags
# 5. fungsi untuk tambah tag
def add_tag():
    #cek apakah ada note yang dipilih oleh cursor
    if list_notes.selectedItems():
        #cari tau judul note nya
        key = list_notes.selectedItems()[0].text()
        #simpen kalimat yg ada di dalam field tag
        tag = field_tag.text()
        #untuk setiap note yang ada di dalam notes
        for note in notes:
            #jika ada note yang punya judul yg sama
            #dengan tag nya belum ada kalimat tersebut
            if note[0] == key and note[2] != tag:
                note[2] = tag
                #tampilin tag tersebut ke dalam tampilan screen
                list_tags.addItem(note[2])
                field_tag.clear()
        with open(str(len(notes)-1)+".txt", "w") as file:
            file.write(note[0]+'\n')
        print(notes)
    else:
        print("Please select a note!")

# 6. fungsi untuk del tag
def del_tag():
    #cek dulu, apakah kita pilih note A / note B /dll
    if list_notes.selectedItems():
        #cari tau judul note yg kita pilih
        key = list_notes.selectedItems()[0].text()
        #cari tau tag dari note yg kita pilih
        tag = list_tags.selectedItems()[0].text()
        #setelah tau, baru remove
        for note in notes:
            if note[0] == key and note[2] == tag:
                field_tag.clear()
                list_tags.takeItem(list_tags.currentRow())
                notes.remove(note)
        #kita simpen ke dalam json file
        #json file berisikan semua data
        with open(str(len(notes)-1)+".txt", "w") as file:
            file.write(note[0]+'\n')
        print(notes)
    else:
        print("note yang tag nya mau di delete, belum dipilih")

# 7. fungsi untuk search tag
def search_tag():
    print(button_tag_search.text())
    tag = field_tag.text()
    if button_tag_search.text() == "Search notes by tag" and tag == True: #tag nya gak kosong
        print(tag)
        notes_filtered = {} #notes with the highlighted tag will be here
        for note in notes:
            if tag in notes[note]["tags"]: 
                notes_filtered[note]=notes[note]
        button_tag_search.setText("Reset search")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(button_tag_search.text())
    elif button_tag_search.text() == "Reset search":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Search notes by tag")
        print(button_tag_search.text())
    else:
        pass
    
#App startup
#attaching event handling
button_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)


#app startup 
notes_win.show()
app.exec_()