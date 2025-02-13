from tkinter import *
from tkinter import font as tkfont

from Managers.ScrappingManager import ScrappingManager


class TheScrapperInterface:
    def __init__(self, root):
        self.scrapper = ScrappingManager()
        self.root = Toplevel(root)
        self.root.title("The Scrapper")
        self.root.columnconfigure([0, 1, 2], weight=1)
        self.root.rowconfigure([0, 1, 2, 3, 4], weight=0)
        self.root.resizable(1, 0)
        self.root.config(bg="#F5F5F5") 

        title_font = ("Segoe UI", 24, "bold")
        body_font = ("Segoe UI", 11)
        button_font = ("Segoe UI", 12, "bold")

        title_label = Label(
            self.root, 
            text="Wikipedia Scraper", 
            font=title_font,
            fg="#8B4513",
            bg="#F5F5F5"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(20, 30), sticky="n")

        self.input_field = Entry(
            self.root, 
            font=body_font,
            relief="flat",
            highlightthickness=1,
            highlightcolor="#E0E0E0",
            highlightbackground="#E0E0E0",
            bd=0
        )
        self.input_field.grid(row=1, column=0, columnspan=3, pady=5, padx=40, sticky="ew", ipady=8)

        button_style = {
            "font": button_font,
            "bg": "#FFA500",
            "fg": "white",
            "activebackground": "#FF8C00",
            "activeforeground": "white",
            "bd": 0,
            "relief": "flat",
            "width": 0,
            "padx": 20,
            "pady": 12,
            "highlightthickness": 0,
            "cursor": "hand2"
        }
        btn_scrap = Button(self.root, text="SCRAAAP NOW!", **button_style, command=self.scrap)
        btn_scrap.grid(row=2, column=0, columnspan=3, pady=20, padx=40, sticky="ew")

        self.response_field = Text(
            self.root, 
            height=8, 
            font=body_font,
            relief="flat",
            wrap="word",
            highlightthickness=1,
            highlightcolor="#E0E0E0",
            highlightbackground="#E0E0E0",
            padx=10,
            pady=10
        )
        self.response_field.grid(row=3, column=0, columnspan=3, pady=5, padx=40, sticky="nsew")

        scrollbar = Scrollbar(
            self.root, 
            command=self.response_field.yview,
            troughcolor="#F5F5F5",
            bg="#C0C0C0",
            activebackground="#A0A0A0",
            width=12
        )
        scrollbar.grid(row=3, column=2, pady=5, sticky="ns")
        self.response_field.config(yscrollcommand=scrollbar.set, state="disabled")

        def on_enter(e):
            btn_scrap.config(bg="#FFB732")
        
        def on_leave(e):
            btn_scrap.config(bg="#FFA500")

        btn_scrap.bind("<Enter>", on_enter)
        btn_scrap.bind("<Leave>", on_leave)

        self.root.mainloop()

    def scrap(self):
        self.response_field.config(state= "normal")
        self.response_field.delete("1.0", "end")
        scrapped_result = self.scrapper.scrape_url(self.input_field.get())
        self.response_field.insert("1.0", scrapped_result["message"])
        self.response_field.config(state="disabled")
        self.response_field.update_idletasks() 
        num_lines = self.get_num_displayed_lines()
        max_height = 10 
        new_height = max(1, min(num_lines, max_height))
        self.response_field.config(height=new_height)

    def get_num_displayed_lines(self):
        lines = 0
        while True:
            line_info = self.response_field.dlineinfo(f"{lines + 1}.0")
            if line_info is None:
                break
            lines += 1
        return lines