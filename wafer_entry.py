from tkinter import StringVar, ttk


class WaferEntry:
    def __init__(self,root, name, column, row, callback, default):
        variable = StringVar(value=default)
        def variable_changed(var, index, mode):
            try:
                return callback(variable.get())
            except:
                pass


        variable.trace_add("write", variable_changed)

        ttk.Label(root, text=name).grid(column=column, row=row)
        ttk.Entry(root, textvariable=variable).grid(column=column, row=row+1)
