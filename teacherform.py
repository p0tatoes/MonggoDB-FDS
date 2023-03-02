import tkinter as tk
from tkinter import messagebox

import pymongo


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
                    mgrid.grid(column=j + 6, row=i + 8)
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

        def teachersFilter():
            for label in teacherwindow.grid_slaves():
                if int(label.grid_info()["row"] > 7):
                    label.grid_forget()

            filterId = int(idFilterField.get())

            idOption = str()

            dbList.clear()
            dbList.append(["ID", "NAME", "DEPARTMENT", "CONTACT #"])
            if idFilterOption.get() == ">":
                idOption = "$gt"
            elif idFilterOption.get() == ">=":
                idOption = "$gte"
            elif idFilterOption.get() == "<":
                idOption = "$lt"
            elif idFilterOption.get() == "<=":
                idOption = "$lte"
            elif idFilterOption.get() == "!=":
                idOption = "$ne"
            elif idFilterOption.get() == "=":
                idOption = "$eq"
            nameStart = f"^{nameStartFilter.get()}"
            nameEnd = f"{nameEndFilter.get()}$"
            department = f"^{departmentFilterField.get()}"
            contact = f"^{contactFilterField.get()}"
            teachersCursor = collection.find(
                {
                    "id": {idOption: filterId},
                    "$and": [
                        {"name": {"$regex": nameStart}},
                        {"name": {"$regex": nameEnd}},
                    ],
                    "department": {"$regex": department},
                    "contactNumber": {"$regex": contact},
                }
            )
            for entry in teachersCursor:
                entryId = entry["id"]
                entryName = entry["name"]
                entryDep = entry["department"]
                entryContact = entry["contactNumber"]
                dbList.append([entryId, entryName, entryDep, entryContact])

            for i in range(len(dbList)):
                for j in range(len(dbList[0])):
                    mgrid = tk.Entry(teacherwindow, width=10)
                    mgrid.insert(tk.END, dbList[i][j])
                    mgrid._values = mgrid.get(), i
                    mgrid.grid(column=j + 6, row=i + 8)
                    mgrid.bind("<Button-1>", callback)

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

        # ! Filters
        filterLabel = tk.Label(
            teacherwindow, text="Filters", bg="cyan", font="Robot 12 bold", width=30
        )
        filterLabel.grid(column=6, row=2, columnspan=4)
        # * ID Filter Option Menu
        idFilterLabel = tk.Label(teacherwindow, text="ID", bg="orange")
        idFilterLabel.grid(column=6, row=4)
        idFilterOptions = [">", ">=", "<", "<=", "!=", "="]
        idFilterOption = tk.StringVar(teacherwindow)
        idFilterOption.set(idFilterOptions[0])
        idFilterDrpDwn = tk.OptionMenu(teacherwindow, idFilterOption, *idFilterOptions)
        idFilterDrpDwn.grid(column=6, row=5)

        # * ID Filter Text Field
        idFilter = tk.IntVar(teacherwindow)
        idFilterField = tk.Entry(teacherwindow, textvariable=idFilter, width=10)
        idFilterField.grid(column=6, row=6)

        # * Name Start Text Field
        nameStartLabel = tk.Label(teacherwindow, text="Name Start", bg="orange")
        nameStartLabel.grid(column=7, row=3)
        nameStartFilter = tk.StringVar(teacherwindow)
        nameStartFilterField = tk.Entry(
            teacherwindow, textvariable=nameStartFilter, width=10
        )
        nameStartFilterField.grid(column=7, row=4)

        # * Name End Text Field
        nameEndLabel = tk.Label(teacherwindow, text="Name End", bg="orange")
        nameEndLabel.grid(column=7, row=5)
        nameEndFilter = tk.StringVar(teacherwindow)
        nameEndFilterField = tk.Entry(
            teacherwindow, textvariable=nameEndFilter, width=10
        )
        nameEndFilterField.grid(column=7, row=6)

        # * Department Start Text Field
        departmentFilterLabel = tk.Label(teacherwindow, text="Department", bg="orange")
        departmentFilterLabel.grid(column=8, row=5)
        departmentFilter = tk.StringVar(teacherwindow)
        departmentFilterField = tk.Entry(
            teacherwindow, textvariable=departmentFilter, width=10
        )
        departmentFilterField.grid(column=8, row=6)

        # * Contact Number Start Text Field
        contactFilterLabel = tk.Label(teacherwindow, text="Contact #", bg="orange")
        contactFilterLabel.grid(column=9, row=5)
        contactFilter = tk.StringVar(teacherwindow)
        contactFilterField = tk.Entry(
            teacherwindow, textvariable=contactFilter, width=10
        )
        contactFilterField.grid(column=9, row=6)

        # * Filter Button
        filterBtn = tk.Button(
            teacherwindow,
            text="Filter",
            command=teachersFilter,
            width=10,
            bg="deep pink",
        )
        filterBtn.grid(column=10, row=6)

        # ! End of Filters

        teacherwindow.mainloop()
