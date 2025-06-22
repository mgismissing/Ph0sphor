import tkinter as tk
from tkinter import ttk, font

root = tk.Tk()
root.title("Phosph0r RRO Editor")
root.geometry("640x480")

# W98 theme
class theme:
    font_tuple = ("MS W98 UI", 8)
    font_tuple_bold = ("MS W98 UI", 8, "bold")
    default_font = font.nametofont("TkDefaultFont")
    text_font = font.nametofont("TkTextFont")
    fixed_font = font.nametofont("TkFixedFont")

style = ttk.Style(root)
style.theme_use("alt")

# W98 Font
theme.default_font.configure(family="MS W98 UI", size=8)
theme.text_font.configure(family="MS W98 UI", size=8)
theme.fixed_font.configure(family="MS W98 UI", size=8)
style.configure("Treeview", font=theme.font_tuple)
style.configure("Treeview.Heading", font=theme.font_tuple_bold)

# Grid config
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Sidebar (Overlay Files List)
sidebar = ttk.Frame(root, width=200)
sidebar.grid(row=0, column=0, sticky="ns")
sidebar.grid_propagate(False)

sidebar_label = ttk.Label(sidebar, text="FILE EXPLORER", font=theme.font_tuple_bold)
sidebar_label.pack(anchor="nw", padx=4, pady=4)

for file in ["colors.xml", "dimens.xml", "strings.xml"]:
    file_label = ttk.Label(sidebar, text=file, anchor="w")
    file_label.pack(fill="x", pady=0, padx=4)

# Main Editor Area (Resource List)
editor_frame = ttk.Frame(root)
editor_frame.grid(row=0, column=1, sticky="nsew")

# Treeview (Resource Key/Value Table)
tree = ttk.Treeview(editor_frame, columns=("type", "key", "value"), show="headings")
tree.heading("type", text="Type")
tree.heading("key", text="Key")
tree.heading("value", text="Value")

#tree.insert("", "end", values=res)

# Scrollbar
scrollbar = ttk.Scrollbar(editor_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Property Editor (Right Panel)
property_frame = ttk.Frame(root, width=250)
property_frame.grid(row=0, column=2, sticky="ns")
property_frame.grid_propagate(False)

prop_label = ttk.Label(property_frame, text="PROPERTY EDITOR", font=theme.font_tuple_bold)
prop_label.pack(anchor="nw", padx=4, pady=4)

type_label = ttk.Label(property_frame, text="Type:")
type_label.pack(anchor="nw", padx=4)
type_entry = ttk.OptionMenu(property_frame, tk.StringVar(value="string"), "string", *["string", "drawable"])
type_entry.pack(anchor="nw", padx=4, pady=4, fill="x")

key_label = ttk.Label(property_frame, text="Key:")
key_label.pack(anchor="nw", padx=4)
key_entry = ttk.Entry(property_frame)
key_entry.pack(anchor="nw", padx=4, pady=4, fill="x")

value_label = ttk.Label(property_frame, text="Value:")
value_label.pack(anchor="nw", padx=4)
value_entry = ttk.Entry(property_frame)
value_entry.pack(anchor="nw", padx=4, pady=4, fill="x")

apply_button = ttk.Button(property_frame, text="Add")
apply_button.pack(anchor="center", pady=4)

# Top Menu (Import/Export)
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Import Overlay")
filemenu.add_command(label="Export Overlay")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

root.mainloop()
