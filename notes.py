from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from os import listdir
from os.path import isfile, join

#TODO
#Add linking ability
#Right click in browser, link to current note
#Or right click and choose another one to link to

#Sort by tags

def load(*args):
    filename.set(filedialog.askdirectory())
    all_notes = [filename.get()+'/'+f for f in listdir(filename.get()) if isfile(join(filename.get(), f))]
    for note in all_notes:
        with open(note) as f:
            note_data = f.read().split(';')
            curr_note_type = note_data[3]
            if curr_note_type=='':
                continue
            if curr_note_type not in all_note_types:
                all_note_types.append(curr_note_type)
                browser.insert('', 'end', curr_note_type, text=curr_note_type)
            browser.insert(curr_note_type, 'end', note_data[0], text=note_data[0])
            for tag in note_data[4].split(','):
                if tag not in all_tags:
                    all_tags.append(tag)
def refresh(*args):
    all_tags = []
    all_note_types = []
    browser.delete(*browser.get_children())
    all_notes = [filename.get()+'/'+f for f in listdir(filename.get()) if isfile(join(filename.get(), f))]
    for note in all_notes:
        with open(note) as f:
            note_data = f.read().split(';')
            curr_note_type = note_data[3]
            if curr_note_type=='':
                continue
            if curr_note_type not in all_note_types:
                all_note_types.append(curr_note_type)
                browser.insert('', 'end', curr_note_type, text=curr_note_type)
            browser.insert(curr_note_type, 'end', note_data[0], text=note_data[0])
            for tag in note_data[4].split(','):
                if tag not in all_tags:
                    all_tags.append(tag)
def load_note(*args):
    text.delete('1.0', 'end')
    current_note.set(value=browser.item(browser.focus())['text'])
    try:
        with open(filename.get() + '/' + current_note.get()) as f:
            note_data = f.read().split(';')
            text.insert('1.0', note_data[1])
            linked.set(value=note_data[2])
            linked_notes = note_data[2].split(",")
            note_type.set(value=note_data[3])
            note_tags.set(value=note_data[4])
    except Exception as e:
        pass
def save(*args):
    if filename.get()=='' or current_note.get()=='':
        current_note.set(value=filedialog.asksaveasfilename().split('/')[-1])
    with open(filename.get()+'/'+current_note.get(), 'w') as f:
        note_data = [current_note.get(), text.get('1.0', 'end'), linked.get(), note_type.get(), note_tags.get()]
        f.write(';'.join(note_data))
    refresh()
def save_as(*args):
    current_note.set(value=filedialog.asksaveasfilename().split('/')[-1])
    with open(filename.get()+'/'+current_note.get(), 'w') as f:
        note_data = [current_note.get(), text.get('1.0', 'end'), linked.get(), note_type.get(), note_tags.get()]
        f.write(';'.join(note_data))
    refresh()
def new_note(*args):
    current_note.set(value='')
    note_tags.set(value='')
    linked.set(value='')
    note_type.set(value='')
    text.delete('1.0', 'end')
def link_note(*args):
    to_link = browser.focus()
    if to_link not in linked_notes:
        linked_notes.append(to_link)
    linked.set(linked_notes)

#gui stuff
root = Tk()
root.title("Notes")

#global variables
filename = StringVar() #folder holding notes
current_note = StringVar() #title of document
note_tags = StringVar() #list of note tags
linked = StringVar() #all notes linked to this one
note_type = StringVar() #top-level type of note
all_tags = [] #set of all unique tags among all notes
all_note_types = [] #global list of all unique note types
linked_notes = []

#Notes Frame
notes = ttk.LabelFrame(root, text="Notes")
notes.grid(column=0, row=0)

#Title
title = ttk.Label(notes, textvariable=current_note)
title.grid(column = 0, row=0, sticky=W)

#Textbox
text = Text(notes, width=40, height=40)
text.grid(column=0,row=1)

#tags
taglabel = ttk.Label(notes, text="Tags:")
taglabel.grid(column=0, row=2, sticky=(W,E))
tags = ttk.Entry(notes, textvariable=note_tags)
tags.grid(column=0,row=3, sticky=(W,E))

#treeview
browser = ttk.Treeview(notes)
browser.grid(column=1,row=0, rowspan=7, sticky=(N,S))
browser.heading('#0', text='Notes')

linkmenu = Menu(browser, tearoff=0)
linkmenu.add_command(label="Link to Current Note", command=link_note)
browser.bind('<<ContextMenu>>', lambda e: linkmenu.post(e.x_root, e.y_root))  

#note type
typelabel = ttk.Label(notes, text="Note Type:")
typelabel.grid(column=0, row=4, sticky = (W,E))
typeselect = ttk.Combobox(notes, textvariable=note_type)
typeselect.grid(column=0,row=5, sticky=(W,E))

typeselect['values'] = ('Settlement', 'Hex', 'Dungeon', 'Creature', 'Object')

#linked pages
linklabel = ttk.Label(notes, text="Linked Pages:")
linklabel.grid(column=0, row = 6, sticky=(W,E))
linkedpages = Listbox(notes, listvariable=linked)
linkedpages.grid(column=0, row=7, sticky=(W,E))

#Menubar
menubar = Menu(root)
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="Create New Note", command=new_note)
file_menu.add_separator()
file_menu.add_command(label="Save Note As", command=save_as)
file_menu.add_command(label="Save Note", command=save)
file_menu.add_separator()
file_menu.add_command(label="Load Directory", command=load)

menubar.add_cascade(label="File", menu=file_menu)
root.config(menu=menubar)

#keybinds
browser.bind('<Double-1>', load_note)
root.bind('<Control-s>', save)
root.bind('<Control-l>', load)
root.bind('<Control-S>', save_as)
root.bind('<Control-r>', refresh)
root.bind('<Control-n>', new_note)

root.mainloop()
