# Импортирование
import tkinter
from tkinter import ttk
import sqlite3

# Создание основного класса.
class Main(tkinter.Frame):

    # Инициализация
    def _init_(self, root):
        super().__init__(root)
        self.init_main()
        self.database = database
        self.view_records()

    # Создание главного окна.
    def init_main(self):

        # Создание toolbar
        toolbar = tkinter.Frame(bg="#17D2E6", bd=5)
        toolbar.pack(side=tkinter.LEFT, fill=tkinter.Y) # Размещение Toolbar

        # Создание Treeview
        self.tree = ttk.Treeview(self, columns=('ID', "SNP", "Telephone",
                                "Email", "Salary"), height=45, show="headings")
        # Создание интерфейса колонок.
        self.tree.column("ID", width=30, anchor=tkinter.CENTER)
        self.tree.column("SNP", width=300, anchor=tkinter.CENTER)
        self.tree.column("Telephone", width=150, anchor=tkinter.CENTER)
        self.tree.column("Email", width=150, anchor=tkinter.CENTER)
        self.tree.column("Salary", width=150, anchor=tkinter.CENTER)

        # Создание вывода их названий на русском языке.
        self.tree.heading("ID", text="ID")
        self.tree.heading("SNP", text="ФИО")
        self.tree.heading("Telephone", text="Номер телефона")
        self.tree.heading("Email", text="Электронная почта")
        self.tree.heading("Salary", text="Заработная плата")

        # Создание возможности пролистывать список вниз.
        scroll = tkinter.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.tree.configure(yscrollcommand=scroll.set)

        # Вывод на экран.
        self.tree.pack(side=tkinter.LEFT)

        # Выбор картинки для переменной ADDIMG.
        self.ADDIMG = tkinter.PhotoImage(file="./img/add.png")
        # Создание кнопки add.
        btn_open_Add = tkinter.Button(toolbar, bg="#FFFFFF", bd=0,
                                            image=self.ADDIMG,
                                            command=self.open_add)
        btn_open_Add.pack(side=tkinter.TOP) # Размещение кнопки add.

        # Выбор картинки для переменной DELETEIMG.
        self.DELETEIMG = tkinter.PhotoImage(file="./img/delete.png")
        # Создание кнопки delete.
        btn_open_Delete = tkinter.Button(toolbar, bg="#FFFFFF", bd=0,
                                            image=self.DELETEIMG,
                                            command=self.delete_records)
        btn_open_Delete.pack(side=tkinter.TOP, pady=5) # Размещение кнопки delete.
        
        # Выбор картинки для переменной REDACTIMG.
        self.REDACTIMG = tkinter.PhotoImage(file="./img/redact.png")
        # Создание кнопки redact.
        btn_open_Redact = tkinter.Button(toolbar, bg="#FFFFFF", bd=0,
                                            image=self.REDACTIMG,
                                            command=self.open_redact)
        btn_open_Redact.pack(side=tkinter.TOP, pady=5) # Размещение кнопки redact.

        # Выбор картинки для переменной SEARCHIMG.
        self.SEARCHIMG = tkinter.PhotoImage(file="./img/search.png")
        # Создание кнопки search.
        btn_open_Redact = tkinter.Button(toolbar, bg="#FFFFFF", bd=0,
                                            image=self.SEARCHIMG,
                                            command=self.open_search)
        btn_open_Redact.pack(side=tkinter.TOP, pady=5) # Размещение кнопки redact.

        # Создание кнопки обновления страницы:
        self.REFRESHIMG = tkinter.PhotoImage(file='./img/refresh.png')
        btn_Refresh = tkinter.Button(toolbar, bg="#FFFFFF", bd=0, 
                                image=self.REFRESHIMG, command=self.view_records)
        btn_Refresh.pack(side=tkinter.TOP, pady=5) # Размещение кнопки refresh.

    # Функция открытия окна add.
    def open_add(self):
        add_window()

    # Функция открытия окна redact.
    def open_redact(self):
        redact_window()

    def open_search(self):
        search_window()

    # Добавление записи в бд.
    def records(self, SNP, Telephone, Email, Salary):
        self.database.insert_data(SNP, Telephone, Email, Salary)
        self.view_records()

    def view_records(self): # Вывод записей бд.
        self.database.cur.execute("""SELECT * FROM database""")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row)
                        for row in self.database.cur.fetchall()]
        
    # Для удаления записей.
    def delete_records(self):
        for selection_time in self.tree.selection():
            self.database.cur.execute("""DELETE FROM database WHERE ID = ?""",
                                (self.tree.set(selection_time, "#1")))
        self.database.con.commit()
        self.view_records()

    # Для редактирования записей.
    def redact_records(self, SNP, Telephone, Email, Salary):
        self.database.cur.execute("""UPDATE database SET SNP=?, Telephone=?,
                                Email=?, Salary=? WHERE ID = ?""",
                                (SNP, Telephone, Email, Salary, self.tree.set
                                 (self.tree.selection()[0], "#1")))
        self.database.con.commit()
        self.view_records()

    # Для поиска записей.
    def search_record(self,SNP):
        SNP = ('%' + SNP +'%',) # Запятая тут важна!
        self.database.cur.execute("""SELECT * FROM database WHERE SNP LIKE ?""", SNP)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', "end", values=row) for row in self.database.cur.fetchall()]


# Добавление функции add.
class add_window(tkinter.Toplevel):

    # Инициализация
    def _init_(self):
        super().__init__(root)
        self.init_add()
        self.view = app

    # Создание окна
    def init_add(self):
        self.title("Добавление сотрудника")
        self.geometry("400x300")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        # Создание интерфейса для строк ввода данных.
        label_SNP = tkinter.Label(self, text="ФИО:",
                                  fg="#139840")
        label_SNP.place(x=50, y=50)
        label_Telephone = tkinter.Label(self, text="Номер телефона:",
                                        fg="#139840")
        label_Telephone.place(x=50, y=80)
        label_Email = tkinter.Label(self, text="Электронная почта:",
                                    fg="#139840")
        label_Email.place(x=50, y=110)
        label_Salary = tkinter.Label(self, text="Заработная плата:",
                                     fg="#139840")
        label_Salary.place(x=50, y=140)

        # Заголовок
        label_info = tkinter.Label(self, text="Добавление сотрудника",
                                   fg="#009900", font="helvetica 14")
        label_info.place(x=60, y=15)
        
        # Создание возможности ввода для строк ввода данных.
        self.entry_SNP = ttk.Entry(self, foreground="#2489A8")
        self.entry_SNP.place(x=200, y=50)
        self.entry_Telephone = ttk.Entry(self, foreground="#2489A8")
        self.entry_Telephone.place(x=200, y=80)
        self.entry_Email = ttk.Entry(self, foreground="#2489A8")
        self.entry_Email.place(x=200, y=110)
        self.entry_Salary = ttk.Entry(self, foreground="#2489A8")
        self.entry_Salary.place(x=200, y=140)

        # Кнопка закрытия окна.
        self.btn_exit = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_exit.place(x=250, y=190)

        # Кнопка подтверждения.
        self.btn_confirm = ttk.Button(self, text="Подтвердить")
        self.btn_confirm.place(x=50, y=190)
        # Нажатие левой кнопкой вызвывает функцию.
        self.btn_confirm.bind("<Button-1>", lambda event: self.view.records
                              (self.entry_SNP.get(), self.entry_Telephone.get(),
                               self.entry_Email.get(), self.entry_Salary.get()))
        
# Добавление функции redact.
class redact_window(tkinter.Toplevel):

    # Инициализация
    def _init_(self):
        super().__init__(root)
        self.init_seacrh()
        self.view = app

    # Создание окна
    def init_seacrh(self):
        self.title("Изменение данных о сотруднике")
        self.geometry("400x300")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        # Создание интерфейса для строк ввода данных.
        label_SNP = tkinter.Label(self, text="ФИО:",
                                  fg="#B2AD20")
        label_SNP.place(x=50, y=50)
        label_Telephone = tkinter.Label(self, text="Номер телефона:",
                                        fg="#B2AD20")
        label_Telephone.place(x=50, y=80)
        label_Email = tkinter.Label(self, text="Электронная почта:",
                                    fg="#B2AD20")
        label_Email.place(x=50, y=110)
        label_Salary = tkinter.Label(self, text="Заработная плата:",
                                     fg="#B2AD20")
        label_Salary.place(x=50, y=140)
        
        # Заголовок
        label_info = tkinter.Label(self, text="Изменение данных о сотруднике",
                                   fg="#DFD921", font="helvetica 14")
        label_info.place(x=45, y=15)
        
        # Создание возможности ввода для строк ввода данных.
        self.entry_SNP = ttk.Entry(self, foreground="#2489A8")
        self.entry_SNP.place(x=200, y=50)
        self.entry_Telephone = ttk.Entry(self, foreground="#2489A8")
        self.entry_Telephone.place(x=200, y=80)
        self.entry_Email = ttk.Entry(self, foreground="#2489A8")
        self.entry_Email.place(x=200, y=110)
        self.entry_Salary = ttk.Entry(self, foreground="#2489A8")
        self.entry_Salary.place(x=200, y=140)

        # Кнопка закрытия окна.
        self.btn_exit = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_exit.place(x=250, y=190)

        # Кнопка подтверждения.
        self.btn_confirm = ttk.Button(self, text="Подтвердить")
        self.btn_confirm.place(x=50, y=190)
        # Нажатие левой кнопкой вызвывает функцию.
        self.btn_confirm.bind("<Button-1>", lambda event: self.view.redact_records
                              (self.entry_SNP.get(), self.entry_Telephone.get(),
                               self.entry_Email.get(), self.entry_Salary.get()))
        
# Добавление функции search.
class search_window(tkinter.Toplevel):
    def _init_(self):
        super().__init__()
        self.init_search()
        self.view = app
        self.grab_set()
        self.focus_set()

    # Интерфейс
    def init_search(self):
        # Создание окна и параметров его.
        self.title("Поиск данных о сотруднике")
        self.geometry('300x100')
        self.resizable(False, False)

        # Заголовок
        label_info = tkinter.Label(self, text="Поиск данных о сотруднике",
                                   fg="#0066CC", font="helvetica 14")
        label_info.place(x=20, y=60)

        # Создание интерфейса и поля ввода
        label_search = tkinter.Label(self, text="Поиск:")
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self, foreground="#2489A8")
        self.entry_search.place(x=105, y=20, width=150)

        # Создание кнопки закрытия.
        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        # Создание кнопки для подтверждения поиска.
        btn_search = ttk.Button(self, text="Поиск")
        btn_search.place(x=105, y=50)
        btn_search.bind("<Button-1>", lambda event:self.view.search_record
                                        (self.entry_search.get()))
        btn_search.bind("<Button-1>", lambda event:self.destroy(), add="+")
        

class DataBase:
    def _init_(self):
        # Подключение к базе данных.
        self.con = sqlite3.connect("database.db")
        self.cur = self.con.cursor()

        # Создание таблицы данных.
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS database(
            id INTEGER PRIMARY KEY NOT NULL,
            SNP TEXT NOT NULL,
            Telephone TEXT,
            Email TEXT,
            Salary INTEGER)""")

        # Сохранение базы данных.
        self.con.commit()

    # Функция для вставления новых данных в базу данных.
    def insert_data(self, SNP, Telephone, Email, Salary):
        self.cur.execute("""INSERT INTO database(SNP, Telephone, Email, Salary)
                         VALUES (?, ?, ?, ?)""",
                         (SNP, Telephone, Email, Salary))

        # Сохранение базы данных
        self.con.commit()

# Для запуска окна, причём только одного.
if __name__ == "_main_":
    root = tkinter.Tk()
    database = DataBase()
    app = Main(root)
    app.pack()

     # Настройки
    root.title("Список сотрудников компании")
    root.geometry("665x450")

     # Запуск окна
    root.mainloop()