import tkinter as tk
from tkinter import messagebox

import pymongo


# TODO: add a mongodb collection containing teacher's id, name, department, contact number
class TeacherForm:
    def teacherform():
        client = pymongo.MongoClient("mongodb://127.0.0.1:27017")

        db = client["fundadb"]
        collection = db["teachers"]

        dbList = list()

        def callback(event):
            li = list()
            li = event.widget._values
            teacherId.set(dbList[li[1]][0])
            teacherName.set(dbList[li[1]][1])
            teacherDepartment.set(dbList[li[1]][2])
            teacherContact.set(dbList[li[1]][3])
            print(
                dbList[li[1]][0],
                dbList[li[1]][1],
                dbList[li[1]][2],
                dbList[li[1]][3],
            )

        def createGrid(x):
            dbList.clear()
            dbList.append(["ID", "NAME", "DEPARTMENT", "CONTACT NUMBER"])
            coursesCursor = collection.find()
            for entry in coursesCursor:
                entryId = entry["id"]
                entryName = entry["name"]
                entryDepartment = entry["department"]
                entryContact = entry["contactNumber"]
                dbList.append([entryId, entryName, entryDepartment, entryContact])

            for i in range(len(dbList)):
                for j in range(len(dbList[0])):
                    mgrid = tk.Entry(teacherwindow, width=10)
                    mgrid.insert(tk.END, dbList[i][j])
                    mgrid._values = mgrid.get(), i
                    mgrid.grid(row=i + 8, column=j + 6)
                    mgrid.bind("<Button-1>", callback)

            if x == 1:
                for label in teacherwindow.grid_slaves():
                    if int(label.grid_info()["row"] > 7):
                        label.grid_forget()

        def save():
            option = messagebox.askokcancel("Save", "Save entry to record?")
            if option:
                newId = collection.count_documents({})
                if newId > 0:
                    newId = collection.find_one(sort=[("id", -1)])["id"]
                id = newId + 1
                teacherId.set(id)
                insertDict = {
                    "id": int(teacherId.get()),
                    "name": nameField.get(),
                    "department": departmentField.get(),
                    "contactNumber": contactField.get(),
                }
                collection.insert_one(insertDict)
                createGrid(1)
                createGrid(0)

        def delete():
            option = messagebox.askokcancel("Delete", "Delete record entry?")
            if option:
                delQuery = {"id": int(idField.get())}
                collection.delete_one(delQuery)
                createGrid(1)
                createGrid(0)

        def update():
            option = messagebox.askokcancel("Update", "Update an entry?")
            if option:
                idQuery = {"id": int(idField.get())}
                updateValues = {
                    "$set": {
                        "name": nameField.get(),
                        "department": departmentField.get(),
                        "contactNumber": contactField.get(),
                    }
                }
                collection.update_one(idQuery, updateValues)
                createGrid(1)
                createGrid(0)

        # * teacherwindow
        teacherwindow = tk.Tk()
        teacherwindow.title("Teachers Form")
        teacherwindow.geometry("1000x750")
        teacherwindow.configure(bg="purple")

        # * Labels
        titleBar = tk.Label(
            teacherwindow,
            text="Teachers Enlistment Form",
            width=30,
            height=1,
            bg="cyan",
            anchor="center",
            font="Roboto 18 bold",
        )
        titleBar.grid(column=1, row=1, columnspan=2)

        idLabel = tk.Label(
            teacherwindow,
            text="Teacher Id:",
            width=15,
            height=1,
            bg="orange",
            font="Roboto 14 bold",
        )
        idLabel.grid(column=1, row=2)

        nameLabel = tk.Label(
            teacherwindow,
            text="Teacher Name",
            width=15,
            height=1,
            bg="orange",
            font="Roboto 14 bold",
        )
        nameLabel.grid(column=1, row=3)

        departmentLabel = tk.Label(
            teacherwindow,
            text="Teacher Department:",
            width=15,
            height=1,
            bg="orange",
            font="Roboto 14 bold",
        )
        departmentLabel.grid(column=1, row=4)

        contactLabel = tk.Label(
            teacherwindow,
            text="Teacher Contac Number:",
            width=15,
            height=1,
            bg="orange",
            font="Roboto 14 bold",
        )
        contactLabel.grid(column=1, row=5)

        # * Enter Fields
        teacherId = tk.StringVar(teacherwindow)
        idField = tk.Entry(teacherwindow, textvariable=teacherId, state=tk.DISABLED)
        idField.grid(column=2, row=2)

        teacherName = tk.StringVar(teacherwindow)
        nameField = tk.Entry(teacherwindow, textvariable=teacherName, width=40)
        nameField.grid(column=2, row=3)

        teacherDepartment = tk.StringVar(teacherwindow)
        departmentField = tk.Entry(
            teacherwindow, textvariable=teacherDepartment, width=40
        )
        departmentField.grid(column=2, row=4)

        teacherContact = tk.StringVar(teacherwindow)
        contactField = tk.Entry(teacherwindow, textvariable=teacherContact, width=40)
        contactField.grid(column=2, row=5)

        createGrid(0)

        # * Buttons
        saveBtn = tk.Button(master=teacherwindow, text="Save", command=save, width=25)
        saveBtn.grid(column=1, row=6)

        updateBtn = tk.Button(
            master=teacherwindow, text="Update", command=update, width=25
        )
        updateBtn.grid(column=2, row=6)

        deleteBtn = tk.Button(
            master=teacherwindow, text="Delete", command=delete, width=25
        )
        deleteBtn.grid(column=3, row=6)

        teacherwindow.mainloop()
