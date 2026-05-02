# AI generated code to visualize PUMLA modelrepo.json in a GUI using Tkinter.
# It loads the JSON, extracts elements, and displays them in a tree view
# with details on selection/double-click.
#
# This file can be copied to any PUMLA model repository root to visualize
# the contents.

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class PUMLAViewerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PUMLA Viewer")
        self.geometry("800x600")
        self._data = {}
        self._elements = []
        self._aliases = {}
        self._load_modelrepo()
        self._build_ui()

    def _get_modelrepo_path(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, "modelrepo.json")

    def _load_modelrepo(self):
        path = self._get_modelrepo_path()
        if not os.path.exists(path):
            messagebox.showerror("Datei nicht gefunden", f"`{path}` existiert nicht.")
            return

        text = open(path, "r", encoding="utf-8").read().strip()
        try:
            obj = json.loads(text)
            objs = [obj]
        except Exception:
            objs = []
            decoder = json.JSONDecoder()
            idx = 0
            length = len(text)
            while idx < length:
                try:
                    obj, consumed = decoder.raw_decode(text, idx)
                    objs.append(obj)
                    idx += consumed
                    while idx < length and text[idx].isspace():
                        idx += 1
                except Exception:
                    break

        model_obj = None
        for o in objs:
            if isinstance(o, dict) and "elements" in o:
                model_obj = o
                break

        if not model_obj:
            messagebox.showerror("Parsing Fehler", "Keine gültige `modelrepo.json` mit `elements` gefunden.")
            return

        self._data = model_obj
        self._elements = model_obj.get("elements", [])
        # map alias or name -> element
        self._aliases = { (e.get("alias") or e.get("name")): e for e in self._elements }

    def _build_ui(self):
        info_frame = ttk.LabelFrame(self, text="Top-Level Informationen")
        info_frame.pack(fill="x", padx=8, pady=6)

        keys_of_interest = ["modelrepopath", "modelrepofile"]
        for k in keys_of_interest:
            val = self._data.get(k, "")
            lbl = ttk.Label(info_frame, text=f"{k}: {val}")
            lbl.pack(anchor="w", padx=6, pady=2)

        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=8, pady=6)

        columns = ("type", "filename")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings")
        self.tree.heading("#0", text="Name (alias)")
        self.tree.heading("type", text="Type")
        self.tree.heading("filename", text="Datei")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        nodes = {}
        def get_parent_alias(elem):
            p = elem.get("parent", "-")
            return None if p in ("-", "", None) else p

        for elem in self._elements:
            alias = elem.get("alias") or elem.get("name")
            text = f"{elem.get('name', '')} ({alias})"
            values = (elem.get("type", ""), elem.get("filename", ""))
            nodes[alias] = {"elem": elem, "text": text, "values": values, "inserted": False}

        # Insert root nodes first, using alias as iid for easy lookup
        for alias, meta in nodes.items():
            elem = meta["elem"]
            parent_alias = get_parent_alias(elem)
            if parent_alias and parent_alias in nodes:
                continue
            try:
                self.tree.insert("", "end", iid=alias, text=meta["text"], values=meta["values"])
            except Exception:
                # fallback: generate unique iid if alias invalid/duplicate
                iid = f"item_{len(self.tree.get_children(''))}_{alias}"
                self.tree.insert("", "end", iid=iid, text=meta["text"], values=meta["values"])
                # keep mapping from iid to element by setting alias variable to iid for lookup later
                nodes[alias]["mapped_iid"] = iid
            else:
                nodes[alias]["mapped_iid"] = alias
            nodes[alias]["inserted"] = True

        # Insert remaining nodes respecting parent relationships
        changed = True
        while changed:
            changed = False
            for alias, meta in nodes.items():
                if meta["inserted"]:
                    continue
                elem = meta["elem"]
                parent_alias = get_parent_alias(elem)
                parent_iid = None
                if parent_alias is None:
                    parent_iid = ""
                elif parent_alias in nodes and nodes[parent_alias].get("mapped_iid"):
                    parent_iid = nodes[parent_alias]["mapped_iid"]
                else:
                    # parent not yet inserted
                    continue

                try:
                    self.tree.insert(parent_iid, "end", iid=alias, text=meta["text"], values=meta["values"])
                except Exception:
                    iid = f"item_{len(self.tree.get_children(parent_iid))}_{alias}"
                    self.tree.insert(parent_iid, "end", iid=iid, text=meta["text"], values=meta["values"])
                    nodes[alias]["mapped_iid"] = iid
                else:
                    nodes[alias]["mapped_iid"] = alias
                nodes[alias]["inserted"] = True
                changed = True

            if not changed:
                # insert any remaining as root to avoid infinite loop
                for alias, meta in nodes.items():
                    if not meta["inserted"]:
                        try:
                            self.tree.insert("", "end", iid=alias, text=meta["text"], values=meta["values"])
                        except Exception:
                            iid = f"item_{len(self.tree.get_children(''))}_{alias}"
                            self.tree.insert("", "end", iid=iid, text=meta["text"], values=meta["values"])
                            nodes[alias]["mapped_iid"] = iid
                        else:
                            nodes[alias]["mapped_iid"] = alias
                        meta["inserted"] = True
                break

        # store mapping iid -> alias for lookup (if mapped_iid differs)
        self._iid_to_alias = {}
        for alias, meta in nodes.items():
            iid = meta.get("mapped_iid") or alias
            self._iid_to_alias[iid] = alias

        # Bind selection and double click
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", self._on_double_click)

        details_frame = ttk.LabelFrame(self, text="Element Details")
        details_frame.pack(fill="both", expand=False, padx=8, pady=6)
        self.details_text = scrolledtext.ScrolledText(details_frame, height=8, wrap="word")
        self.details_text.pack(fill="both", expand=True, padx=4, pady=4)

    def _format_taggedvalues(self, tagged):
        if not tagged:
            return "  (keine tagged values)"
        lines = []
        for tv in tagged:
            tag = tv.get("tag", "")
            vals = tv.get("values", [])
            vals_str = ", ".join(str(v) for v in vals) if vals else ""
            lines.append(f"  - {tag}: {vals_str}")
        return "\n".join(lines)

    def _show_element_details(self, elem):
        name = elem.get("name", "(no name)")
        alias = elem.get("alias") or name
        filename = elem.get("filename", "(no filename)")
        tagged = elem.get("taggedvalues", [])

        details = []
        details.append(f"Name: {name}")
        details.append(f"Alias: {alias}")
        details.append(f"Filename: {filename}")
        details.append("Tagged Values:")
        details.append(self._format_taggedvalues(tagged))

        self.details_text.delete("1.0", "end")
        self.details_text.insert("end", "\n".join(details))

    def _get_element_by_iid_or_text(self, iid, text):
        # Try iid -> alias mapping
        alias = self._iid_to_alias.get(iid) or iid
        if alias in self._aliases:
            return self._aliases[alias]
        # fallback: try extract alias from text
        if "(" in text and text.endswith(")"):
            try:
                extracted = text[text.rfind("(")+1:-1].strip()
                if extracted in self._aliases:
                    return self._aliases[extracted]
            except Exception:
                pass
        # final fallback search by name
        name = text.split(" (")[0].strip()
        for e in self._elements:
            if e.get("name") == name or e.get("alias") == name:
                return e
        return None

    def _on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        text = (self.tree.item(iid, "text") or "").strip()
        elem = self._get_element_by_iid_or_text(iid, text)
        if elem:
            self._show_element_details(elem)
        else:
            self.details_text.delete("1.0", "end")
            self.details_text.insert("end", "Details nicht gefunden.")

    def _on_double_click(self, event):
        # Bestimme das Item unter dem Mausklick
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
        text = (self.tree.item(item_id, "text") or "").strip()
        elem = self._get_element_by_iid_or_text(item_id, text)
        if elem:
            self._show_element_details(elem)

if __name__ == "__main__":
    app = PUMLAViewerApp()
    app.mainloop()