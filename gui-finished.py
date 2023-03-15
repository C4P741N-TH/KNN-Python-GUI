from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import csv
import pandas as pd
import numpy as np
import math
import operator

root = Tk()
root.title("Python KNN Prompiriya Phornchai Jaturawit")
csvPath = "dataset.csv"
width = 500
height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

data = pd.read_csv(csvPath)
def euclideanDistance(data1, data2, length):
    distance = 0
    for x in range(length):
        distance += np.square(data1[x] - data2[x])
    return np.sqrt(distance)

def knn(trainingSet, testInstance, k):
    distances = {}
    length = testInstance.shape[1]
    # Calculating euclidean distance between each row of training data and test data
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet.iloc[x], length)
        distances[x] = dist[0]
 
    # Sorting them on the basis of distance
    sorted_d = sorted(distances.items(), key=operator.itemgetter(1))
 
    neighbors = []
    
    # Extracting top k neighbors
    for x in range(k):
        neighbors.append(sorted_d[x][0])

    classVotes = {}
    # Calculating the most freq class in the neighbors
    for x in range(len(neighbors)):
        response = trainingSet.iloc[neighbors[x]][-1]
 
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1

    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return(sortedVotes[0][0], neighbors)

TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("Humidity", "pH", "Salinity", "Mineral", "Quality"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('Humidity', text="Humidity(%)", anchor=W)
tree.heading('pH', text="pH", anchor=W)
tree.heading('Salinity', text="Salinity", anchor=W)
tree.heading('Mineral', text="Mineral(%)", anchor=W)
tree.heading('Quality', text="Quality", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=100)
tree.column('#2', stretch=NO, minwidth=0, width=100)
tree.column('#3', stretch=NO, minwidth=0, width=100)
tree.column('#4', stretch=NO, minwidth=0, width=100)
tree.column('#5', stretch=NO, minwidth=0, width=100)
tree.pack()

with open(csvPath) as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        humidity = row['Humidity']
        ph = row['pH']
        salinity = row['Salinity']
        mineral = row['Mineral']
        quality = row['Quality']
        tree.insert("", tk.END, values=(humidity, ph, salinity,mineral,quality))

def getKNN():
    K = k.get()
    Hum = hum.get()
    pH = ph.get()
    Sal = sal.get()
    Mine = mine.get()
    testSet = [[Hum, pH, Sal, Mine]]
    test = pd.DataFrame(testSet)
    result,neigh = knn(data, test, K)
    res.set(result)
    neig.set(neigh)
    

k = IntVar()
k_label = Label(root,text="K Value (Odd)").place(x=7,y=240)
k_input = Entry(root, textvariable=k,).place(x=110, y=240)
k.set('')

hum = IntVar()
hum_label = Label(root,text="Humidity 0-100").place(x=7,y=270)
hum_input = Entry(root, textvariable=hum).place(x=110, y=270)
hum.set('')

ph = DoubleVar()
ph_label = Label(root,text="pH 0.0-14.0").place(x=7,y=300)
ph_input = Entry(root, textvariable=ph).place(x=110, y=300)
ph.set('')

sal = IntVar()
sal_label = Label(root,text="Salinity 0 - 10").place(x=7,y=330)
sal_input = Entry(root, textvariable=sal).place(x=110, y=330)
sal.set('')

mine = IntVar()
mine_label = Label(root,text="Mineral 0-100").place(x=7,y=360)
mine_input = Entry(root, textvariable=mine).place(x=110, y=360)
mine.set('')

res = StringVar()
res_label = Label(root,text="Quality").place(x=7,y=390)
res_disp = Entry(root, textvariable=res,state=DISABLED).place(x=110, y=390)
res.set('')

neig = StringVar()
neig_label = Label(root,text="Neighbour node").place(x=7,y=420)
neigh_disp = Entry(root, textvariable=neig,state=DISABLED).place(x=110, y=420)

calc_btn = Button(root, command=getKNN, text="Calculate")
calc_btn.place(x=250, y=385)


#============================INITIALIZATION==============================
if __name__ == '__main__':
    root.mainloop()