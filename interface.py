import tkinter as tk
from database import get_all_stats, db_connection


class MyLabel(tk.Frame):
    def __init__(self, master, name, percentage, domain):
        tk.Frame.__init__(self, master, bd=2, relief='raised')
        tk.Label(self, text=f'{percentage}', font=('Arial', 24), fg='#88F', width=5, anchor='e').grid(row=0, column=0, rowspan=2)
        tk.Label(self, text=name, font=('Aria', 16, 'bold'), fg='black', width=21, anchor='w').grid(row=0, column=1)
        tk.Label(self, text=', '.join(domain), font=('Aria', 10), fg='black').grid(row=1, column=1, sticky='w')
        self.columnconfigure(1, weight=1)


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Do and save your Action : ")
        label.grid(row=0, column=0)

        label = tk.Label(self, text="This is total stats")
        label.grid(row=2, column=0)

        for i, n in enumerate(name):
            MyLabel(self, n, percentage[i], domain[i]).grid(row=0+i, column=0, columnspan=2, padx=(4, 4))


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Do Act", command=p1.lift)
        l1 = tk.Label(buttonframe, text='TEST DATA', font=('Arial', 18, 'bold'), bg='green')

        b1.pack(side="left")
        l1.pack(side="left")
        p1.show()


if __name__ == "__main__":

    name = ['acts', 'made', 'days', 'reps', 'avg']
    percentage = []
    for item in get_all_stats():
        for ins in item:
            percentage.append(ins)

    all_acts_querry = "SELECT * FROM acts"
    all_acts = db_connection(all_acts_querry, receive=True)
    all_acts_list = []
    for item in all_acts:
        all_acts_list.append(item[1])
    domain = [[act[1] for act in all_acts], ['total acts made'], ['total days with action'], ['total reps'],
              ['avg reps pro act']]
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x350+340+350")
    root.mainloop()