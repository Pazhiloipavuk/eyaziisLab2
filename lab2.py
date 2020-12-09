import nltk
from pathlib import Path
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
from nltk import *
from nltk.corpus import stopwords
from string import punctuation
from wordfreq import top_n_list

docs = []
langs = []

stopwords_german = set(stopwords.words('german'))
stopwords_spanish = set(stopwords.words('spanish'))

root=Tk()
space0 = Label(root,text='\n')
aboutButton = Button(root,text='About',width=8,height=2,bg='light grey')
space1 = Label(root,text='\n')
chooseDocsButton=Button(root,text='Choose htmls',width=55,height=2,bg='light grey')
space2 = Label(root,text='\n')
resultTree=ttk.Treeview(root, columns=("File", "Language (freq words)", "Language (alphabet)", "Language (stopwords)"), selectmode='browse', height=11)
resultTree.heading('File', text="File", anchor=W)
resultTree.heading('Language (freq words)', text="Language (freq words)", anchor=W)
resultTree.heading('Language (alphabet)', text="Language (alphabet)", anchor=W)
resultTree.heading('Language (stopwords)', text="Language (stopwords)", anchor=W)
resultTree.column('#0', stretch=NO, minwidth=0, width=0)
resultTree.column('#1', stretch=NO, minwidth=347, width=347)
resultTree.column('#2', stretch=NO, minwidth=347, width=347)
resultTree.column('#3', stretch=NO, minwidth=347, width=347)
resultTree.column('#4', stretch=NO, minwidth=347, width=347)
space3 = Label(root,text='\n')
detectButton=Button(root,text='Detect language',width=55,height=2,bg='light grey')
space4 = Label(root,text='\n')
saveButton=Button(root,text='Save',width=55,height=2,bg='light grey')
space5 = Label(root,text='\n')

def nameOf(path):
    return Path(path).stem

def chooseDocsClicked():
    global docs, langs
    docs = []
    langs = []
    resultTree.delete(*resultTree.get_children())
    files = filedialog.askopenfilename(multiple=True)
    splitlist = root.tk.splitlist(files)
    for doc in splitlist:
        docs.append((nameOf(doc), Path(doc, encoding="UTF-8", errors='ignore').read_text(encoding="UTF-8", errors='ignore')))
        resultTree.insert('', 'end', values=(nameOf(doc), '', '', ''))

def detect_freqwords_method(text):
    words = set()
    for sentence in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sentence):
            if word not in punctuation:
                words.add(word)
    if len(words.intersection(top_n_list('de', 30))) > len(words.intersection(top_n_list('es', 30))):
        return "German"
    else:
        return "Spanish"

def detect_alphabet_method(text):
    german_alphabet = set("ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß".lower())
    spanish_alphabet = set("ABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúñü".lower())
    chars = set() 
    for sentence in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sentence):
            if word not in punctuation:
                chars.update(set(word.lower()))
    if len(german_alphabet.intersection(chars)) > len(spanish_alphabet.intersection(chars)):
        return "German"
    else:
        return "Spanish"

def detect_stopwords_method(text):
    words = set([word.lower() for word in wordpunct_tokenize(text)])
    stopwords_german_count = len(words.intersection(stopwords_german))
    stopwords_spanish_count = len(words.intersection(stopwords_spanish))
    if stopwords_german_count > stopwords_spanish_count:
        return "German"
    else:
        return "Spanish"

def detectButtonClicked():
    resultTree.delete(*resultTree.get_children())
    for doc in docs:
        freqwords_method = detect_freqwords_method(doc[1])
        alphabet_method = detect_alphabet_method(doc[1])
        stopwords_method = detect_stopwords_method(doc[1])
        langs.append(stopwords_method)
        resultTree.insert('', 'end', values=(doc[0], freqwords_method, alphabet_method, stopwords_method))

def save():
    file = open('results.txt', 'w')
    for i, doc in enumerate(docs):
        file.write(doc[0])
        file.write(" - ")
        file.write(langs[i])
        file.write("\n")
    file.close()

def aboutButtonClicked():
    messagebox.showinfo("Lab 2", "Usage: Choose html files. Then click detect language.\nYou can also save result.\n\nDeveloped by: Artyom Gurbovich and Pavel Kalenik.")

aboutButton.config(command=aboutButtonClicked)
chooseDocsButton.config(command=chooseDocsClicked)
detectButton.config(command=detectButtonClicked)
saveButton.config(command=save)

space0.pack()
aboutButton.pack()
space1.pack()
chooseDocsButton.pack()
space2.pack()
resultTree.pack()
space3.pack()
detectButton.pack()
space4.pack()
saveButton.pack()
space5.pack()
root.mainloop()