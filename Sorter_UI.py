from tkinter import *
from tkinter import filedialog

from sorter import Picture
from sorter import Directory

# from PIL import ImageTk, Image
                # font            context      function        label       title
color_set = ['dark slate gray','light goldenrod','tomato','dark salmon','saddle brown']
page_buf=[]

dir_inst = Directory(None)
dir_path = ""
button_width = 8
page_idx = 0
page_col  = 2
mapping = ["title","tag1","tag2"]
#Command
def FrameClear(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def content_display():
    global dir_inst, page_idx, page_buf
    dir_inst = Directory(dir_path)
    content = dir_inst.ls()
    FrameClear(RFrm_Up)
    page_buf = []
    for page in range(int(len(content)/25)+1):
        display = '\n'.join(content[page*25:(page+1)*25])
        page_buf.append(display)
    if len(page_buf) > page_col:
        for idx in range(page_col):
            lbl_dir_content = Label(RFrm_Up, text=page_buf[page_idx+idx],
                fg=color_set[0],bg=color_set[1], font='Verdana 10 bold')
            lbl_dir_content.pack(side=LEFT,ipadx=10,fill=Y)
    else:
        for idx in range(len(page_buf)):
            lbl_dir_content = Label(RFrm_Up, text=page_buf[idx],
                fg=color_set[0],bg=color_set[1], font='Verdana 10 bold')
            lbl_dir_content.pack(side=LEFT,ipadx=10,fill=Y)

def NextPage():
    global page_idx, page_buf
    if page_idx + page_col < len(page_buf):
        page_idx = page_idx + page_col
        FrameClear(RFrm_Up)
        for idx in range(page_col):
            if page_idx+idx < len(page_buf):
                lbl_dir_content = Label(RFrm_Up, text=page_buf[page_idx+idx],
                    fg=color_set[0],bg=color_set[1], font='Verdana 10 bold')
                lbl_dir_content.pack(side=LEFT,ipadx=10,fill=Y)

def PrePage():
    global page_idx, page_buf
    if page_idx - page_col >= 0:
        page_idx = page_idx - page_col
        FrameClear(RFrm_Up)
        for idx in range(page_col):
            lbl_dir_content = Label(RFrm_Up, text=page_buf[page_idx+idx],
                fg=color_set[0],bg=color_set[1], font='Verdana 10 bold')
            lbl_dir_content.pack(side=LEFT,ipadx=10,fill=Y)

def BrowseDir():
    global dir_inst, dir_path, page_idx
    page_idx = 0
    dir_path = filedialog.askdirectory(title = "Select a Directory",)
    label_dir_path.configure(text="Directory Opened: "+dir_path, font='Verdana 12 bold italic')
    content_display()

def StartSort():
    global dir_inst, page_idx
    page_idx = 0
    val = v1.get()
    dir_inst.sort(mapping[val])
    content_display()

def StartFetch():
    global dir_inst, page_idx
    page_idx = 0
    dir_inst.fetch()
    content_display()

def StartAdd():
    global dir_inst
    val = v2.get()
    tag_str = Txt_add.get(1.0, END+"-1c")
    dir_inst.addAttr(tag_str,mapping[val])
    content_display()

def StartRemove():
    global dir_inst
    val = v3.get()
    dir_inst.rmAttr(mapping[val])
    content_display()

def StartCalLen():
    global dir_inst
    dir_inst.calculate_len()
    content_display()

def BuildRadio(var, item_list):
    sub_LFrm = Frame(LFrm)
    sub_LFrm.pack()
    for item, val in item_list:
        Radiobutton(sub_LFrm, text=item, variable=var, value=val, fg=color_set[0],bg=color_set[2]).pack(side=LEFT)

root = Tk()
root.geometry('800x600')
root.title('File Sorter')

UpFrm = Frame(root)
LFrm = Frame(root)
RFrm = Frame(root)

#title side
UpFrm.config(bg=color_set[3])
UpFrm.pack(anchor=NW,fill=BOTH, padx=5,pady=5)
label_dir_path = Label(UpFrm, text='Welcome to File Sorter',
        bg=color_set[3],fg=color_set[4], font='Verdana 16 bold italic')
label_dir_path.pack(anchor=N,pady=20)


#function side
LFrm.config(bg=color_set[2])
LFrm.pack(anchor=NW, side=LEFT,fill=BOTH, padx=5,pady=5)
Label(LFrm, text='function',fg=color_set[0],bg=color_set[2],font='Verdana 10 bold').pack(anchor=NW)
# open
Btn_open = Button(LFrm, text='Open',fg=color_set[0],font='Verdana 10 bold',width=button_width,command=BrowseDir)
Btn_open.pack(padx=50,pady=20)
# sort
v1 = IntVar()
v1.set(0)
BuildRadio(v1,[("title",0),("tag1",1),("tag2",2)])
Btn_sort = Button(LFrm, text='Sort',fg=color_set[0],font='Verdana 10 bold',width=button_width,command= StartSort)
Btn_sort.pack(padx=50,pady=10)
# fetch
Btn_fetch = Button(LFrm, text='Fetch',fg=color_set[0],font='Verdana 10 bold',width=button_width,command=StartFetch)
Btn_fetch.pack(padx=50,pady=20)
# add
v2 = IntVar()
v2.set(1)
BuildRadio(v2,[("tag1",1),("tag2",2)])
Txt_add = Text(LFrm, height = 1,font='Verdana 10 bold', width=10)
Txt_add.pack()
Btn_add = Button(LFrm, text='Add',fg=color_set[0],font='Verdana 10 bold',width=button_width,command= StartAdd)
Btn_add.pack(padx=50,pady=10)
# remove
v3 = IntVar()
v3.set(1)
BuildRadio(v3,[("tag1",1),("tag2",2)])
Btn_remove = Button(LFrm, text='remove',fg=color_set[0],font='Verdana 10 bold',width=button_width,command= StartRemove)
Btn_remove.pack(padx=50,pady=10)
# size
Btn_len = Button(LFrm, text='size',fg=color_set[0],font='Verdana 10 bold',width=button_width,command=StartCalLen)
Btn_len.pack(padx=50,pady=20)


#content side
RFrm.config(bg=color_set[1])
RFrm.pack(anchor=NW,fill=BOTH,expand=True,padx=5,pady=5)

RFrm_Up = Frame(RFrm,bg=color_set[1])
RFrm_Up.pack(anchor=N,padx=20,pady=20)
lbl_dir_content = Label(RFrm_Up, fg=color_set[0], font='Verdana 10 bold',justify=LEFT,
text='This is file sorter.\nname rule : (title)_(tag1)#(tag2)-num.any\n\nusage:\n\
sort:\tSort files into directories by specific tag.(title,tag1,tag2)\n\
fetch:\tFetch files from all directories.\n\
add:\tAdd string to all of files in directories. (tag1,tag2)\n\
remove:\tRemove string to all of files in directories.(tag1,tag2)\n\
size:\tCalculate the number of files and name number to folder')
lbl_dir_content.pack()


RFrm_Down = Frame(RFrm,bg=color_set[1])
RFrm_Down.pack(anchor=E,side = BOTTOM)
Button(RFrm_Down, text='Previous', fg=color_set[0], height=1, width=10,command=PrePage).pack(side=LEFT,padx=20,pady=20)
Button(RFrm_Down, text='Next', fg=color_set[0], height=1, width=10,command=NextPage).pack(padx=20,pady=20) 

root.mainloop()