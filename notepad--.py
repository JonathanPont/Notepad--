import tkinter as tk, tkinter.font as tk_font
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os
import subprocess
import sys

def exitProgram():
    quit()

def newFile(event=None):
    global filepath
    txt_edit.delete("1.0", tk.END)
    window.title("New File")
    filepath = ""

def setFont(font):
    txt_edit.configure(font=(font, 10))

def saveAs():
    global filepath
    old_filepath = filepath
    filepath = asksaveasfilename(defaultextension="txt", filetypes=[("Text File", "*.txt"),("Other File", "*.*")])
    if not filepath:
        filepath = old_filepath
        return
    txt_edit.edit_modified(False)
    with open(filepath, "w") as output_file:
        text = txt_edit.get("1.0", tk.END)
        output_file.write(text)
    window.title(filepath.split("/")[-1] + " - " + filepath)
    
    

def save(event=None):
    global filepath
    if filepath:
        txt_edit.edit_modified(False)
        with open(filepath, "w") as output_file:
            text = txt_edit.get("1.0", tk.END)
            output_file.write(text)
        window.title(filepath.split("/")[-1] + " - " + filepath)
        
    else:
        saveAs()

def openFile(event=None):
    global filepath
    filepath = askopenfilename(filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")])
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()[:-1]
        txt_edit.insert(tk.END, text)
    txt_edit.edit_modified(False)
    window.title(filepath.split("/")[-1] + " - " + filepath)

def changeTheme():
    global dark_theme
    dark_theme = not dark_theme
    if dark_theme:
        window.configure(bg="#353535")
        txt_edit.configure(bg="#393939", fg="#FAFAFA", insertbackground="#E0E0E0", highlightthickness=1, highlightcolor="#000000", highlightbackground="#400040")
    else:
        window.configure(bg="SystemButtonFace")
        txt_edit.configure(bg="SystemWindow", fg="SystemWindowText", insertbackground="SystemWindowText", highlightthickness=0.1, highlightcolor="SystemButtonFace", highlightbackground="SystemButtonFace")

def textChange(event=None):
    global filepath
    txt_edit.edit_modified(False)
    if filepath:
        window.title("*" + filepath.split("/")[-1] + " - " + filepath + "*")
    else:
        window.title("New File*")

def openWith(app=""):
    global filepath
    filename = filepath.split("/")[-1]
    if app == "exec":
        exec(txt_edit.get("1.0", tk.END), {}, {})
    elif app:
        subprocess.Popen(app + " " + filename)
    else:
        if " " in filename:
            os.system('start "' + filename + '"')
        else:
            os.system('start ' + filename)
    

window = tk.Tk()

dark_theme = False

#top menu
menu = tk.Menu(window)
window.config(menu=menu)

fileMenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
optionsMenu = tk.Menu(menu)
menu.add_cascade(label="Options", menu=optionsMenu)
fontsMenu = tk.Menu(optionsMenu)
optionsMenu.add_cascade(label="Font", menu=fontsMenu)
runMenu = tk.Menu(menu)
menu.add_cascade(label="Run", menu=runMenu)

fileMenu.add_command(label="New", command=newFile)
fileMenu.add_command(label="Open", command=openFile)
fileMenu.add_command(label="Save", command=save)
fileMenu.add_command(label="Save As", command=saveAs)
fileMenu.add_command(label="Exit", command=exitProgram)
optionsMenu.add_command(label="Theme", command=changeTheme)

for font in [font for font in tk_font.families() if font[0] != "@"]:
    fontsMenu.add_command(label=font, command=lambda font=font :setFont(font))

runMenu.add_command(label="Run With Default", command=openWith)
runMenu.add_command(label="Run With exec()", command=lambda : openWith("exec"))
runMenu.add_command(label="Open With Notepad", command=lambda : openWith("notepad.exe"))

#main text box
txt_edit = tk.Text(window, font=("Microsoft YaHei", 10), highlightthickness=0.1)

txt_edit.place(relwidth=1.0, relheight=1.0)

txt_edit.bind("<<Modified>>", textChange) # Two ctrl+s needed

#
newFile()

#shortcuts
window.bind_all("<Control-Key-s>", save)
window.bind_all("<Control-Key-o>", openFile)
window.bind_all("<Control-Key-n>", newFile)

window.mainloop()
