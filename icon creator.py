from tkinter import*
from tkinter import filedialog
from PIL import Image, ImageTk


root = Tk()
root.title("icon creator")
root.geometry("600x500")
bgcolor = "#ff6234"
root.config(bg=bgcolor)

global import_img, export_img
import_img = ""
export_img = ""

def import_image():
    global import_img
    import_img = filedialog.askopenfilename(title="open image", filetypes=(("Jpg files", "*.jpg"), ("PNG files", "*.png")))
    entry_import.delete(0,END)
    entry_import.insert(0, import_img)

def export_image():
    global export_img
    export_img = filedialog.asksaveasfilename(title="open image", filetypes=(("Icon files", "*.ico"),))
    entry_export.delete(0,END)
    entry_export.insert(0, export_img)

def covert_to_icon():
    global import_img, export_img
    img = Image.open(import_img)
    img.save(export_img, "ICO")

Label(root, text="import Image", bg=bgcolor, font=("Helvetica", 10)).grid(row=0, column=0, pady=25)

entry_import  = Entry(root, bd=0, width="50", font=('Helvetica',10))
entry_import.grid(row=0, column=1, padx=10, sticky=EW)

Button(root, text="import Image", bg="red", fg="white", font=('Helvetica',10), bd=0, command=import_image).grid(row=0, column=2, padx=5)


Label(root, text="export Image", bg=bgcolor, font=("Helvetica", 10)).grid(row=1, column=0, pady=25)

entry_export  = Entry(root, bd=0, width="50", font=('Helvetica',10))
entry_export.grid(row=1, column=1, padx=10, sticky=EW)

Button(root, text="export image", bg="red", fg="white", font=('Helvetica',10), bd=0, command=export_image).grid(row=1, column=2, padx=5)
Button(root, text="convert", bg="green2", fg="white", font=('Helvetica',13), bd=0, command=covert_to_icon).grid(row=2, column=0, columnspan=3, sticky=EW)




root.mainloop()