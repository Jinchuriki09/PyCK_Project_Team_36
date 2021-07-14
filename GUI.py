from tkinter import *
from tkinter.scrolledtext import ScrolledText

import pandas as pd
import functions
import updates

root=Tk()
root.title('Flipkart product tracker')

def btn1():
    url = enterLink.get()
    functions.addEntry(url)
    enterLink.delete(0,len(url))
    
def btn2():
    url = enterSectionLink.get()
    functions.populateDB(url)
    enterSectionLink.delete(0,len(url))
    
def btn3():
    url = 'https://flipkart.com/search?q='
    string = enterProductName.get()
    tagList = string.split()
    for tag in tagList:
        url += tag
        url += '+'
    url = url[:-1]
    url += r.get()
    functions.populateDB(url)
    enterProductName.delete(0,len(url))


def btn4():
    new_window = Tk()
    new_window.title('Database')
    
    varDict = {}
    df = pd.read_csv('database.csv', index_col=0, converters={'price_in_rupees' : str,
                                                              'availability' : str})
    
    checklist = ScrolledText(new_window, width=40, height=30)
    checklist.pack()
    for i, row in df.iterrows():
        varDict[i] = IntVar(new_window)
        c = Checkbutton(checklist, text=row['product_name'][:50]+'...', variable=varDict[i], onvalue=1, offvalue=0, anchor='w')
        checklist.window_create('end', window=c)
        
    
    def deleteAll():
        df = pd.read_csv('database.csv', index_col=0, converters={'price_in_rupees' : str,
                                                                  'availability' : str})
        
        df_new = df[0:0]
        df_new.to_csv('database.csv', mode="w")
        new_window.destroy()
            
    
    def deletebtn():
        df1 = pd.read_csv('database.csv', index_col=0, converters={'price_in_rupees' : str,
                                                                   'availability' : str})
        for i in varDict:
            if(varDict[i].get()):
                df1.drop(index=i, inplace=True)
        df1 = df1.reset_index(drop=True)
        df1.to_csv("database.csv", mode="w")
        new_window.destroy()
    
    deleteButton = Button(new_window, text="delete selected", command=deletebtn)
    deleteButton.pack(side = LEFT, padx=20, pady=10) 
    
    deleteAllButton = Button(new_window, text="clear database", command=deleteAll)
    deleteAllButton.pack(side = RIGHT, padx=20, pady=10)
            
def btn5():
    updates.doCheck()
    
#product page link fucntionality
        
singleLink = Label(root, text="Enter product page link")
enterLink = Entry(root)
button1 = Button(root, text="Add entry", command=btn1)

singleLink.grid(row=0,column=0, padx=15, pady=5, sticky='w')
enterLink.grid(row=1,column=0, padx=15, pady=5, sticky='w')
button1.grid(row=2,column=0, padx=15, pady=5, sticky='w')

#scrape section functionality
label1 = Label(root, text="").grid(row=3, column=0, pady=5)

sectionLink = Label(root, text="Enter section page link")
enterSectionLink = Entry(root)
button2 = Button(root, text="Select products", command=btn2)

sectionLink.grid(row=0,column=1, padx=15, pady=5, sticky='w')
enterSectionLink.grid(row=1,column=1, padx=15, pady=5, sticky='w')
button2.grid(row=2,column=1, padx=15, pady=5, sticky='w')


#search & get functionality

search = Label(root, text="Search products")
enterProductName = Entry(root)
button3 = Button(root, text="Add products", command=btn3)

search.grid(row=4,column=0, padx=15, pady=5, sticky='w')
enterProductName.grid(row=5,column=0, padx=15, pady=5, sticky='w')
button3.grid(row=6,column=0, padx=15, pady=5, sticky='w')

r = StringVar(value='&sort=popularity')
radiobtn1 = Radiobutton(root, text="Sort by popularity", variable=r, value='&sort=popularity')
radiobtn2 = Radiobutton(root, text="Sort by price-Low to High", variable=r, value='&sort=price_asc')
radiobtn3 = Radiobutton(root, text="Sort by price-High to Low", variable=r, value='&sort=price_desc')
radiobtn4 = Radiobutton(root, text="Sort by Newest first", variable=r, value='&sort=recency_desc')

radiobtn1.grid(row=4, column=1, sticky='w') 
radiobtn2.grid(row=5, column=1, sticky='w')
radiobtn3.grid(row=6, column=1, sticky='w')
radiobtn4.grid(row=7, column=1, sticky='w')

label2 = Label(root, text="").grid(row=8, column=0, pady=5)

#database managment functionality

button4 = Button(root, text="Show Database", command=btn4)
button4.grid(row=9,column=0, padx=15, pady=5, sticky='w')

#check for changes and mail functionality

button5 = Button(root, text="Check for updates", command=btn5)
button5.grid(row=9, column=1, padx=15, pady=5, sticky='w')

root.mainloop()