from tkinter import *

from Interfaces.TheScrapperInterface import TheScrapperInterface



class UiManager:
    def __init__(self):

        self.root = Tk()
        self.root.title("Wikipedia Scraper")
        self.root.geometry("680x500")
        self.root.resizable(True, True)
        self.root.configure(bg="#FFE5B4")  
        self.root.columnconfigure((0, 1, 2), weight=1)
        self.root.rowconfigure((0, 1, 2, 3, 4), weight=1)
        
        title_font = ("Segoe UI", 28, "bold")
        button_font = ("Segoe UI", 13, "bold")
        
        title_label = Label(
            self.root, 
            text="Wikipedia Scraper", 
            font=title_font,
            bg="#FFE5B4", 
            fg="#8B4513",
            pady=10
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(40, 20), sticky="n")
        
        button_style = {
            "font": button_font,
            "bg": "#FFA500",  
            "fg": "white",
            "activebackground": "#FF8C00",
            "activeforeground": "white",
            "bd": 0,
            "relief": "flat",
            "width": 0,
            "padx": 30,
            "pady": 14,
            "cursor": "hand2",
            "highlightthickness": 0
        }
        
        button_frame = Frame(self.root, bg="#FFE5B4")
        button_frame.grid(row=1, column=1, rowspan=3, sticky="nsew")
        
        btn_scrap = Button(
            button_frame, 
            text="Scrap Wikipedia URLs", 
            **button_style, 
            command=self.theScrapper
        )
        btn_search = Button(
            button_frame, 
            text="Search in Scrapped URLs", 
            **button_style
        )
        btn_create = Button(
            button_frame, 
            text="Create Your Custom Page", 
            **button_style
        )
        
        btn_scrap.pack(pady=12, fill="x", expand=True)
        btn_search.pack(pady=12, fill="x", expand=True)
        btn_create.pack(pady=12, fill="x", expand=True)
        
        def on_enter(e):
            e.widget.config(bg="#FFB732", relief="flat", highlightbackground="#E69500")
            
        def on_leave(e):
            e.widget.config(bg="#FFA500", highlightbackground="#FFE5B4")
        
        for btn in [btn_scrap, btn_search, btn_create]:
            btn.config(highlightbackground="#FFE5B4", highlightthickness=2)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        for btn in [btn_scrap, btn_search, btn_create]:
            btn.config(highlightbackground="#E69500")
        
        self.root.mainloop()
        
    def theScrapper(self):
        TheScrapperInterface(self.root)

    def theSearcher(self):
        pass

    def thePageCreator(self):
        pass
