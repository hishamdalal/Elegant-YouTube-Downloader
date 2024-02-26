from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import ttkbootstrap as tb

from inc.config import YPD_Config
# from inc.helper import window_center
import inc.helper as helper


class YPD_Settings:
    # config_file = './config.ini'
    themes = {
        'light': ['cosmo', 'flatly', 'journal', 'litera', 'lumen', 'minty', 'pulse', 'sandstone', 'united', 'yeti',
                  'morph', 'simplex', 'cerculean'],
        'dark': ['solar', 'superhero', 'darkly', 'cyborg', 'vapor', ]
    }
    is_dark = False
    current = {}
    
    # ----------------------------------------------------------------------------
    def __init__(self):
        self.config = YPD_Config()
        # self.init_settings()

        self.theme_list = None
        self.download_dir_input = None
        self.dark_theme = None

        w = 700
        h = 250
        
        window = tb.Toplevel(minsize=(w, h))
        window.configure(padx=20, pady=20)
        window.title("Settings")
        window.iconbitmap('images/YouTube.ico')
        
        helper.window_center(window, w, h)
                
        # window.geometry("700x250")

        self.init_current_settings()
        self.layout(window)
        self.controls(window)
        self.set_current_settings()
        self.window = window
    # ----------------------------------------------------------------------------
    def save_settings(self):
        tb.Style(theme=self.theme_list.get())

        try:
            self.config.save(section='MAIN', key='downloads_dir', value=self.download_dir_input.get())
            self.config.save(section='MAIN', key='theme', value=str(self.theme_list.current()))  # self.theme_list.get()
            self.config.save(section='MAIN', key='dark_theme', value="Yes" if self.is_dark.get() else "No")
                        
            helper.toast_notify("Save Setting", 'Settings saved successfully')
            
        except Exception as e:
            helper.show_error(e)

    # ----------------------------------------------------------------------------
    def init_current_settings(self):
        self.current['downloads_dir'] = self.config.get(section='MAIN', key='downloads_dir')
        self.current['theme'] = self.config.get(section='MAIN', key='theme')
        self.current['dark_theme'] = self.config.get(section='MAIN', key='dark_theme')
    # ----------------------------------------------------------------------------
    def set_current_settings(self):
        self.download_dir_input.insert(index=0, string=str(self.current['downloads_dir']))

        if self.current['dark_theme'] == 'Yes':
            self.is_dark.set(1)
        else:
            self.is_dark.set(0)

        self.refresh_themes_list()

        self.theme_list.current(int(self.current['theme']))
    # ----------------------------------------------------------------------------
    def layout(self, window):
        window.grid_columnconfigure(index=0, weight=2, uniform='a')
        window.grid_columnconfigure(index=1, weight=2, uniform='a')
        window.grid_columnconfigure(index=2, weight=2, uniform='a')
        window.grid_columnconfigure(index=3, weight=2, uniform='a')

        window.grid_rowconfigure(index=0, weight=3, uniform='a')
        window.grid_rowconfigure(index=1, weight=2, uniform='a')
        window.grid_rowconfigure(index=2, weight=2, uniform='a')
        window.grid_rowconfigure(index=3, weight=2, uniform='a')
    # ----------------------------------------------------------------------------
    def controls(self, window):
        self.header(window)
        self.directory_contorls(window)
        self.theme_controls(window)
        self.footer_buttons(window)
    # ----------------------------------------------------------------------------
    def header(self, window):
        tb.Label(window, text="Settings", font=('Arial', 20), justify=tb.CENTER).grid(row=0, column=0, columnspan=4)
    # ----------------------------------------------------------------------------
    def directory_contorls(self, window):

        tb.Label(window, text="Download Folder:").grid(row=1, column=0, sticky="ew")
        self.download_dir_input = tb.Entry(window)
        self.download_dir_input.grid(row=1, column=1, columnspan=2, sticky="ew")
        tb.Button(window, text="Browse...", command=lambda:self.browse(window)).grid(row=1, column=3, sticky="ew")
    # ----------------------------------------------------------------------------
    def theme_controls(self, window):
        dark_var = IntVar()
        dark_var.set(0)
        self.is_dark = dark_var

        tb.Label(window, text="Select Theme:").grid(row=2, column=0, sticky="ew")
        self.dark_theme = tb.Checkbutton(window, text="Dark theme?", bootstyle="round-toggle", onvalue=1, offvalue=0, variable=dark_var, command=self.refresh_themes_list)
        self.dark_theme.grid(row=2, column=1)

        self.theme_list = tb.Combobox(window, text="Themes", value=self.themes['light'])
        self.theme_list.grid(row=2, column=2)
        self.theme_list['state'] = "readonly"
        # self.theme_list.current(0)
        # self.theme_list.bind("<<ComboboxSelected>>", self.save_settings())
        tb.Style(theme=self.theme_list.get())
    # ----------------------------------------------------------------------------
    def footer_buttons(self, window):
        tb.Button(window, text="Save", command=self.save_settings).grid(row=3, column=1, sticky="ew")
        tb.Button(window, text="Exit", command=window.destroy, bootstyle="outline").grid(row=3, column=2, sticky="ew")
    # ----------------------------------------------------------------------------
    def refresh_themes_list(self):
        if self.is_dark.get():
            self.theme_list.config(values=self.themes['dark'])
        else:
            self.theme_list.config(values=self.themes['light'])

        self.theme_list.configure(takefocus=True)
        self.theme_list.current(0)

        # self.theme_list.set(value=self.themes['dark'])
    # ----------------------------------------------------------------------------
    def browse(self, window):
        default_dir = self.config.get("MAIN", 'downloads_dir')
        directory = filedialog.askdirectory(initialdir=default_dir, title="Select folder", parent=window)

        if directory:
            self.download_dir_input.delete(0, "end")
            self.download_dir_input.insert(0, directory)
    # ----------------------------------------------------------------------------
