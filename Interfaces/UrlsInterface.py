from tkinter import *
from tkinter import font as tkfont
from Managers.DbManager import dbService
from Interfaces.HTMLManager import HTMLManager


class UrlsInterface:
    def __init__(self, root):
        self.db = dbService()
        self.root = Toplevel(root)
        self.root.title("URL Manager")
        self.root.config(bg="#F5F5F5")
        self.root.resizable(1, 0)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1) 

        title_font = ("Segoe UI", 24, "bold")
        body_font = ("Segoe UI", 11)
        button_font = ("Segoe UI", 12, "bold")

        title_label = Label(
            self.root, 
            text="URL Manager", 
            font=title_font,
            fg="#8B4513",
            bg="#F5F5F5"
        )
        title_label.grid(row=0, column=0, pady=(20, 10), sticky="n")

        self.canvas = Canvas(self.root, bg="#F5F5F5", highlightthickness=0)
        self.scrollbar = Scrollbar(
            self.root, 
            orient="vertical", 
            command=self.canvas.yview,
            troughcolor="#F5F5F5",
            bg="#C0C0C0",
            activebackground="#A0A0A0",
            width=12
        )
        self.scrollable_frame = Frame(self.canvas, bg="#F5F5F5")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        ))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=1, column=0, sticky="nsew", padx=40, pady=5)
        self.scrollbar.grid(row=1, column=1, sticky="ns", pady=5)

        self.canvas.bind("<Configure>", lambda e: self.scrollable_frame.config(width=e.width))

        self.load_data()

        self.root.mainloop()

    def load_data(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        urls = self.db.getAllUrls()
        body_font = ("Segoe UI", 11)
        button_font = ("Segoe UI", 12, "bold")

        for url in urls:
            url_id, url_text, date_added = url
            frame = Frame(self.scrollable_frame, bg="#F5F5F5", pady=5)
            frame.pack(fill="x", expand=True)

            text_label = Label(
                frame,
                text=f"{url_text}\nAdded on: {date_added}",
                font=body_font,
                bg="#F5F5F5",
                anchor="w",
                justify=LEFT
            )
            text_label.pack(side="left", fill="x", expand=True, padx=(0, 10))

            # Button container frame
            btn_frame = Frame(frame, bg="#F5F5F5")
            btn_frame.pack(side="right")

            # Button style templates
            base_btn_style = {
                "font": button_font,
                "fg": "white",
                "activeforeground": "white",
                "bd": 0,
                "relief": "flat",
                "padx": 12,
                "pady": 6,
                "cursor": "hand2"
            }

            # HTML Button
            html_btn_style = {
                "bg": "#4CAF50",
                "activebackground": "#45A049",
                **base_btn_style
            }
            html_btn = Button(
                btn_frame, 
                text="To HTML", 
                **html_btn_style,
                command=lambda u=url_id, url=url_text: self.export_to_html(u, url)
            )
            html_btn.pack(side="left", padx=(0, 5))

            # Delete Button
            delete_btn_style = {
                "bg": "#FFA500",
                "activebackground": "#FF8C00",
                **base_btn_style
            }
            delete_btn = Button(
                btn_frame, 
                text="Delete", 
                **delete_btn_style,
                command=lambda u=url_id, f=frame: self.delete_url(u, f)
            )
            delete_btn.pack(side="left")

            for btn in [html_btn, delete_btn]:
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=b.cget("activebackground")))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=b.cget("bg")))

    def delete_url(self, url_id, frame):
        self.db.deleteUrl(url_id)
        frame.destroy()

    def export_to_html(self, url_id, url_text):
        print(f"Exporting to HTML - ID: {url_id}, URL: {url_text}")
        htmlGenerator = HTMLManager()
        generated = htmlGenerator.generate_html(url_id, url_text)
        if generated["success"]:
            print(generated["message"])
        else:
            print(generated["message"])