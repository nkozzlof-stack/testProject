import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import db


class OrdersApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Учёт заказов (PostgreSQL / test_orders)")
        self.geometry("950x620")

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True)

        self.tab_clients = ClientsTab(nb)
        self.tab_orders  = OrdersTab(nb)
        self.tab_reports = ReportsTab(nb)

        nb.add(self.tab_clients, text="Клиенты")
        nb.add(self.tab_orders,  text="Заказы")
        nb.add(self.tab_reports, text="Отчёты")

        nb.bind("<<NotebookTabChanged>>", lambda e: (
            self.tab_clients.refresh(),
            self.tab_orders.refresh(),
        ))


class ClientsTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.tree = ttk.Treeview(self, columns=("id", "fio"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("fio", text="ФИО")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("fio", width=400)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        btns = ttk.Frame(self)
        btns.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(btns, text="Добавить",      command=self.add).pack(side="left", padx=4)
        ttk.Button(btns, text="Редактировать", command=self.edit).pack(side="left", padx=4)
        ttk.Button(btns, text="Удалить",       command=self.delete).pack(side="left", padx=4)

        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            for c_id, fio in db.get_clients():
                self.tree.insert("", "end", values=(c_id, fio))
        except Exception as e:
            messagebox.showerror("Ошибка БД", str(e))

    def selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Внимание", "Выберите запись")
            return None
        return self.tree.item(sel[0])["values"][0]

    def add(self):
        fio = simpledialog.askstring("Новый клиент", "Введите ФИО:")
        if fio and fio.strip():
            db.add_client(fio.strip())
            self.refresh()

    def edit(self):
        c_id = self.selected_id()
        if c_id is None:
            return
        cur_fio = self.tree.item(self.tree.selection()[0])["values"][1]
        fio = simpledialog.askstring("Редактирование", "ФИО:", initialvalue=cur_fio)
        if fio and fio.strip():
            db.update_client(c_id, fio.strip())
            self.refresh()

    def delete(self):
        c_id = self.selected_id()
        if c_id is None:
            return
        if messagebox.askyesno("Удаление", "Удалить клиента?"):
            try:
                db.delete_client(c_id)
            except Exception as e:
                messagebox.showerror(
                    "Ошибка",
                    f"Не удалось удалить клиента.\n"
                    f"Возможно, у него есть заказы.\n\n{e}"
                )
            self.refresh()


class OrdersTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.tree = ttk.Treeview(self,
                                 columns=("id", "dt", "client", "article"),
                                 show="headings")
        for col, txt, w in (("id", "ID", 60),
                            ("dt", "Дата/время", 160),
                            ("client", "Клиент", 260),
                            ("article", "Артикул", 260)):
            self.tree.heading(col, text=txt)
            self.tree.column(col, width=w)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        btns = ttk.Frame(self)
        btns.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(btns, text="Добавить",      command=self.add).pack(side="left", padx=4)
        ttk.Button(btns, text="Редактировать", command=self.edit).pack(side="left", padx=4)
        ttk.Button(btns, text="Удалить",       command=self.delete).pack(side="left", padx=4)

        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            for o in db.get_orders():
                self.tree.insert("", "end", values=o)
        except Exception as e:
            messagebox.showerror("Ошибка БД", str(e))

    def selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Внимание", "Выберите заказ")
            return None
        return self.tree.item(sel[0])["values"][0]

    def open_dialog(self, title, init_dt=None):
        clients  = db.get_clients()
        articles = db.get_articles()
        if not clients or not articles:
            messagebox.showerror("Ошибка", "Сначала добавьте клиентов и артикулы")
            return None

        dlg = tk.Toplevel(self)
        dlg.title(title)
        dlg.grab_set()
        dlg.resizable(False, False)

        ttk.Label(dlg, text="Дата/время (ГГГГ-ММ-ДД ЧЧ:ММ):")\
            .grid(row=0, column=0, padx=8, pady=6, sticky="w")
        dt_var = tk.StringVar(
            value=init_dt or datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        ttk.Entry(dlg, textvariable=dt_var, width=25)\
            .grid(row=0, column=1, padx=8, pady=6)

        ttk.Label(dlg, text="Клиент:")\
            .grid(row=1, column=0, padx=8, pady=6, sticky="w")
        client_var = tk.StringVar()
        client_cb = ttk.Combobox(
            dlg, textvariable=client_var, state="readonly",
            values=[f"{c[0]} | {c[1]}" for c in clients]
        )
        client_cb.grid(row=1, column=1, padx=8, pady=6)
        client_cb.current(0)

        ttk.Label(dlg, text="Артикул:")\
            .grid(row=2, column=0, padx=8, pady=6, sticky="w")
        article_var = tk.StringVar()
        article_cb = ttk.Combobox(
            dlg, textvariable=article_var, state="readonly",
            values=[f"{a[0]} | {a[1]}" for a in articles]
        )
        article_cb.grid(row=2, column=1, padx=8, pady=6)
        article_cb.current(0)

        result = {}

        def ok():
            try:
                dt_val = datetime.strptime(dt_var.get(), "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror(
                    "Ошибка",
                    "Неверный формат даты. Используйте ГГГГ-ММ-ДД ЧЧ:ММ"
                )
                return
            result["dt"]        = dt_val
            result["client_id"] = int(client_var.get().split("|")[0].strip())
            result["group_id"]  = int(article_var.get().split("|")[0].strip())
            dlg.destroy()

        ttk.Button(dlg, text="OK",     command=ok)\
            .grid(row=3, column=0, padx=8, pady=10)
        ttk.Button(dlg, text="Отмена", command=dlg.destroy)\
            .grid(row=3, column=1, padx=8, pady=10)

        self.wait_window(dlg)
        return result or None

    def add(self):
        data = self.open_dialog("Новый заказ")
        if data:
            db.add_order(data["dt"], data["client_id"], data["group_id"])
            self.refresh()

    def edit(self):
        o_id = self.selected_id()
        if o_id is None:
            return
        cur = self.tree.item(self.tree.selection()[0])["values"]
        data = self.open_dialog("Редактирование заказа", init_dt=str(cur[1]))
        if data:
            db.update_order(o_id, data["dt"], data["client_id"], data["group_id"])
            self.refresh()

    def delete(self):
        o_id = self.selected_id()
        if o_id is None:
            return
        if messagebox.askyesno("Удаление", "Удалить заказ?"):
            db.delete_order(o_id)
            self.refresh()


class ReportsTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)
        ttk.Button(top, text="1. Заказы по клиентам",
                   command=lambda: self.run("client")).pack(side="left", padx=4)
        ttk.Button(top, text="2. Заказы за последний месяц",
                   command=lambda: self.run("month")).pack(side="left", padx=4)
        ttk.Button(top, text="3. Заказы по артикулам",
                   command=lambda: self.run("article")).pack(side="left", padx=4)

        self.tree = ttk.Treeview(self, show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def run(self, kind):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            if kind == "client":
                cols = ("ID", "ФИО", "Кол-во заказов")
                data = db.report_orders_by_client()
            elif kind == "month":
                cols = ("ID", "Дата/время", "ФИО", "Артикул")
                data = db.report_orders_last_month()
            else:
                cols = ("ID", "Артикул", "Кол-во заказов")
                data = db.report_orders_by_article()
        except Exception as e:
            messagebox.showerror("Ошибка БД", str(e))
            return

        self.tree["columns"] = cols
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=200, anchor="w")

        for row in data:
            self.tree.insert("", "end", values=row)


if __name__ == "__main__":
    app = OrdersApp()
    app.mainloop()