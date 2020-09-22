import tkinter as tk
from database import get_all_stats, db_connection


class MyLabel(tk.Frame):
    def __init__(self, master, name, percentage, domain):
        super().__init__(master, bd=2, relief='raised')
        tk.Label(self, text=f'{percentage}', font=('Arial', 24), fg='#88F', width=5, anchor='e').grid(row=0, column=0, rowspan=2)
        tk.Label(self, text=name, font=('Aria', 16, 'bold'), fg='black', width=21, anchor='w').grid(row=0, column=1)
        tk.Label(self, text=', '.join(domain), font=('Aria', 10), fg='black').grid(row=1, column=1, sticky='w')
        self.columnconfigure(1, weight=1)


class ListViewer(tk.Listbox):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.scrollbar = tk.Scrollbar(master, orient=tk.VERTICAL)
        self.list = tk.Listbox(master, selectmode=tk.EXTENDED, yscrollcommand=self.scrollbar.set)
        self.list.config(height=20)
        self.scrollbar.config(command=self.list.yview)

        self.popup_menu = tk.Menu(self.list, tearoff=0)
        self.popup_menu.add_command(label='Open file location')
        self.popup_menu.add_command(label='Open file in Notepad')
        self.list.bind("<Button-3>", self.popup)

        self.print_btn = tk.Button(master, text="Print selection", command=self.print_selection)
        self.delete_btn = tk.Button(master, text="Delete selection", command=self.delete_selected_items)

        self.scrollbar.grid(column=3, row=5, sticky='nsew')
        self.list.grid(column=0, row=5, columnspan=2, padx=(10, 1), sticky='nsew')
        self.print_btn.grid(column=0, row=6, padx=(10, 1), sticky='nsew')
        self.delete_btn.grid(column=1, row=6, sticky='nsew')

    def list_size(self):
        return self.list.size()

    def all_list_items(self):
        return self.list.get(0, tk.END)

    def clear_list(self):
        self.list.delete(0, tk.END)

    def populate_list(self, record):
        self.list.insert(0, record)

    def get_current_selection(self):
        """
        If in Listbox selected more than 1 item:
                return list with items
            else:
                return item string
        """
        current_selection = self.list.curselection()
        selected_items = [self.list.get(i) for i in current_selection]
        if len(selected_items) == 1:
            return self.list.get(current_selection)
        return selected_items

    def popup(self, event):
        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def print_selection(self):
        selected_items = self.get_current_selection()
        top = tk.Toplevel()
        selection_list = ListViewer(top)
        selection_list.grid(column=0, row=5, sticky='nsew')

        if isinstance(selected_items, list):
            max_len_str = max(selected_items, key=len)
            selection_list.config(width=len(max_len_str))
            for record in selected_items:
                selection_list.populate_list(record)
        else:
            selection_list.populate_list(selected_items)
            selection_list.config(width=len(selected_items))

    def delete_selected_items(self):
        selection = self.list.curselection()
        for i in reversed(selection):
            self.list.delete(i)


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="This is total stats")
        label.grid(row=0, column=0)
        for i, n in enumerate(name):
            MyLabel(self, n, percentage[i], domain[i]).grid(row=1+i, column=0, columnspan=2, padx=(4, 4))


class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="This is all exercises")
        label.grid(row=0, column=0)
        all_done_acts_query = "SELECT * FROM done_acts"
        all_done = db_connection(all_done_acts_query, receive=True)
        page_list = ListViewer(self)
        for record in all_done:
            page_list.populate_list(record)


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Do Act", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Show Acts", command=p2.lift)
        l1 = tk.Label(buttonframe, text='TEST DATA', font=('Arial', 16, 'bold'), bg='green')

        b1.pack(side="left")
        b2.pack(side="left")
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
    root.title('Exercise counter')
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x350+340+350")
    root.mainloop()
