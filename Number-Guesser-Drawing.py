from PIL import ImageGrab
# from PIL import Image
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
# import pickle

def getter(widget):
    # x=root.winfo_rootx()+widget.winfo_x()
    # y=root.winfo_rooty()+widget.winfo_y()
    x = widget.winfo_rootx()*1.5 + 2
    y = widget.winfo_rooty()*1.5 + 1
    # print(widget.winfo_rootx(),widget.winfo_rooty())
    x1=x+1.5*widget.winfo_width() - 4
    y1=y+1.5*widget.winfo_height() - 5
    img = ImageGrab.grab((x,y,x1,y1))
    return img

# def save_canvas_to_Image(canvas):
#     canvas.update()
#     canvas.postscript(file='temp.eps', colormode='color')
#     img = Image.open('temp.eps')
#     return img

def drawing(event):
    x,y = event.x,event.y
    # print(x,y)
    canvas.create_oval(x-10,y-10,x+10,y+10,fill='#ffffff',outline='#ffffff')

def guesser():
    global guess_text
    # img1 = save_canvas_to_Image(canvas)
    img1 = getter(canvas)
    # guess = np.random.randint(0,10)
    guess = predict_number(img1)
    guess_text = str(guess)
    display_box.configure(state='normal')
    display_box.delete(1.0,2.0)
    display_box.insert(tk.END, guess_text)
    display_box.configure(state='disabled')

def predict_number(img1):
    img1 = np.array(img1.resize((28,28)).convert('L'))
    # with open('objs.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    #     pickle.dump(img1, f)
    img1 = tf.expand_dims(img1.reshape(784), axis=0)/255
    prediction = np.argmax(model1.predict(img1))
    return prediction



model1 = load_model('mnist-digits-9818.h5')

root = tk.Tk()
root.title('Number Guesser')
# root.geometry('400x350')

canvas = tk.Canvas(root, width=300, height=300, background='#000000')
canvas.bind('<B1-Motion>', drawing)
canvas.grid(column=0, columnspan=5, row=0, rowspan=5, padx=5, pady=5)

guess_text = tk.StringVar()
display_box = tk.Text(root,width=1, height=1, bg=root['background'], fg='#ff0000',font=('Helvetica', '48'), relief=tk.FLAT)
display_box.insert(tk.END, '?')
display_box.configure(state='disabled')
display_box.grid(column=5, columnspan=2, row=0, rowspan=2, padx=5, pady=5)

check_button = ttk.Button(root, text='Guess', command=guesser)
check_button.grid(column=5, columnspan=2, row=2, rowspan=1, padx=5, pady=5)

clear_button = ttk.Button(root, text='Clear',command=lambda:canvas.delete('all'))
clear_button.grid(column=5, columnspan=2, row=3, rowspan=1, padx=5, pady=5)

root.mainloop()