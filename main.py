from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.dialogs import Messagebox
from pytube.exceptions import RegexMatchError
from pytube import YouTube
import pytube.request
# from pytube.innertube import InnerTube

import webbrowser

# from icecream import ic
# from icecream import install
# install()


# import io
import os
import threading
import datetime
import re
# import urllib.request
# from PIL import ImageTk, Image
# import os.path
import sys
import requests


import inc.helper as helper
import inc.config as config
import inc.settings as settings
import inc.translation as translation

# from inc import helper
# from inc import YPD_Config
# from inc import YPD_Settings
# from inc import YPT_Translations
# import inc.translation

pytube.request.default_range_size = 100000


class YPD:
    use_oauth = False
    allow_oauth_cache = False

    current = {}
    rownum = 0
    url = ''
    _type = "Video"
    ext = ".mp4"
    streams = {}
    title = "Test"
    downloads_dir = "."
    filename = ''
    filename_with_ext = ''
    resource = None
    resolutions = None
    file_info = {}
    file_extra_info = {}
    url_var = None
    thumb = None
    root = None
    menubar = None
    yt = None
    skip_existing = True
    override = False
    
    # ----------------------------------------------------------------------------                
    def __init__(self):

        self.config = config.YPD_Config()        
        w = 700
        h = 450
        
        root = tb.Window(themename="superhero", minsize=(w, h))
        root.configure(padx=20, pady=20) 

        root.title("Elegeant YouTube Downloader")
        
        if os.path.isfile("images/YouTube.ico"):
            root.iconbitmap('images/YouTube.ico')
        
        # https://stackoverflow.com/a/49954793/2269902
        helper.window_center(root, w, h)  
        
        # self.root = root
        # self.root.wait_visibility(self.root) 
             
        
        # root.bind_all("<Key>", self._onKeyRelease, "+")
        root.bind("<Key>", self._onKeyRelease)
        # root.bind('<Key>', self.paste)
        root.bind('<Escape>', self._onKeyRelease)
        root.bind('<Return>', self._onKeyRelease)
        #
        # root.grid_columnconfigure(index=0, weight=1, uniform='a')
        # root.grid_rowconfigure(index=0, weight=1, uniform='a')
        # frame = tb.Frame(root, width=700, height=450, borderwidth=0)
        # frame.grid(row=0, column=0, sticky="news")

        self.init_current_settings()
        self.init_vars()
        
        self.layout(root)
        self.controls(root)
        self.root = root
        # self.frame = frame
        self.init_theme()
        self.root.after(400, self.set_current_settings)

        # self.open_translations_modal()
        root.mainloop()
    # ----------------------------------------------------------------------------
    def init_vars(self):
        _type = tb.StringVar()
        self._type = _type

        skip_existing = BooleanVar()
        self.skip_existing = skip_existing
    # ----------------------------------------------------------------------------
    def init_current_settings(self):
        
        self.current['type'] = self.config.get(section='MAIN', key='type')
        self.current['override'] = helper.bool(self.config.get(section='MAIN', key='override'))

        self.downloads_dir = self.config.get(section='MAIN', key='downloads_dir')
        self.theme = self.config.get(section='MAIN', key='theme')
        self.dark_theme = self.config.get(section='MAIN', key='dark_theme')
        self.resolution = self.config.get(section='MAIN', key='resolution')
    # ----------------------------------------------------------------------------
    def set_current_settings(self):
        if len(self.current):
            self._type.set(self.current['type'])
            self.override = self.current['override']
            self.skip_existing.set(not self.override)
    # ----------------------------------------------------------------------------
    def init_theme(self):
        themename = "superhero"
        try:
            theme = self.config.get('MAIN', 'theme')
            dark_theme = self.config.get('MAIN', 'dark_theme')

            if theme != "" and theme != None:
                if dark_theme == 'Yes':
                    themename = settings.YPD_Settings.themes['dark'][int(theme)]
                else:
                    themename = settings.YPD_Settings.themes['light'][int(theme)]
        
        except Exception as e:
            helper.show_error(e)
            
        finally:
            tb.Style(theme=themename)
    # ----------------------------------------------------------------------------
    def layout(self, window):
        window.grid_columnconfigure(index=0, weight=1, uniform='a')
        window.grid_columnconfigure(index=1, weight=1, uniform='a')
        window.grid_columnconfigure(index=2, weight=1, uniform='a')
        window.grid_columnconfigure(index=3, weight=1, uniform='a')

        window.grid_rowconfigure(index=0, weight=2, uniform='a')
        window.grid_rowconfigure(index=1, weight=2, uniform='a')
        window.grid_rowconfigure(index=2, weight=2, uniform='a')
        window.grid_rowconfigure(index=3, weight=2, uniform='a')
        window.grid_rowconfigure(index=4, weight=8, uniform='a')
        window.grid_rowconfigure(index=5, weight=1, uniform='a')
        window.grid_rowconfigure(index=6, weight=2, uniform='a')
    # ----------------------------------------------------------------------------
    def controls(self, window):
        self.rownum = 0
        self.menu(window)
        self.header(window)
        self.type_controls(window)
        self.url_controls(window)
        self.quality_controls(window)
        self.info_controls(window)
        self.progress_controls(window)
        self.footer_buttons(window)
    # ----------------------------------------------------------------------------
    def menu(self, window):
        menubar = tb.Menu(window)
        # Adding File Menu and commands
        self.menu_items = tb.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Menu', menu=self.menu_items)
        self.menu_items.add_command(label='Settings', command=self.open_settings_modal)
     
        self.menu_items.add_command(label='Open folder', command=self.open_folder)
        self.menu_items.add_separator()
        self.menu_items.add_command(label='Exit', command=window.destroy)
        
        
        self.menu_items2 = tb.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Download', menu=self.menu_items2)
        
        self.menu_items2.add_command(label='Thumbnail', command=self.download_thumbnail)
        self.menu_items2.entryconfig("Thumbnail", state="disabled")
        
        self.menu_items2.add_command(label='Info', command=self.download_info)
        self.menu_items2.entryconfig("Info", state="disabled")
        
        self.menu_items2.add_command(label='Open Translations', command=self.open_translations_modal)
        self.menu_items2.entryconfig("Open Translations", state="disabled")
        
        # self.menu_items3 = tb.Menu(menubar, tearoff=0)
        # menubar.add_cascade(label='About', menu=self.menu_items3)
        # self.menu_items3.add_command(label='About', command=window.destroy)
     

        # self.menu_items2.add_command(label='Translations', command=self.download_translate)
        # self.menu_items2.entryconfig("Translations", state="disabled")
        
        menubar.add_command(label='About', command=self.about_me)
        
        
        # display Menu
        window.config(menu=menubar)
    # ----------------------------------------------------------------------------
    def header(self, window):
        # self.rownum +=1
        title = "Elegant YouTube Downloader"
        
        lbl = tb.Label(window, text=title, font=('Ubuntu Medium', 20), justify=tb.CENTER)
        lbl.grid(row=self.rownum, column=0, columnspan=4)
    # ----------------------------------------------------------------------------
    def url_controls(self, window):
        self.rownum += 1
        tb.Label(window, text="Video URL:").grid(row=self.rownum, column=0, sticky="ew")
        url_var = StringVar()
        self.url_var = url_var

        self.url = tb.Entry(window, textvariable=url_var)
        self.url.grid(row=self.rownum, column=1, columnspan=2, sticky="ew")

        self.fetch_btn = tb.Button(window, text="Get Info", command=self.fetch_data)
        self.fetch_btn.grid(row=self.rownum, column=3, sticky="ew")
    # ----------------------------------------------------------------------------
    def type_controls(self, window):
        self.rownum += 1

        tb.Label(window, text="Type:").grid(row=self.rownum, column=0, sticky="ew")

        self.radio1 = tb.Radiobutton(window, text="Video", value="Video", name="video", variable=self._type,
                                     command=lambda: self.set_val('Video'))
        self.radio1.grid(row=self.rownum, column=1)

        self.radio2 = tb.Radiobutton(window, text="Audio", value="Audio", name="audio", variable=self._type,
                                     command=lambda: self.set_val('Audio'))
        self.radio2.grid(row=self.rownum, column=2)

        # set default value
        # r1.set(self._type)
    # ----------------------------------------------------------------------------
    def quality_controls(self, window):
        self.rownum += 1
        tb.Label(window, text="Quality:").grid(row=self.rownum, column=0, sticky="ew")

        self.qualities = tb.Combobox(window, name="quality")
        self.qualities.grid(row=self.rownum, column=1, columnspan=2, sticky="ew")

        # var1.set('720')
        # self.qualities.current(0)

        self.qualities['state'] = 'readonly'
        
        # override = bool(self.config.get('MAIN', 'override')) or False
        
        # skip_existing = IntVar()
        # self.skip_existing = skip_existing
        # override_var.set(value=True)
        
        self.override = tb.Checkbutton(window, text="Override", variable=self.skip_existing, command=self.set_override)
        self.override.grid(row=self.rownum, column=3)
        # self.override.state(["selected"])
                
    # ----------------------------------------------------------------------------
    def info_controls(self, window):
        self.rownum += 1

        # tb.Label(window, text="Info:").grid(row=self.rownum, column=0, sticky="ew")

        self.info = tb.Text(window, font=('Courier New', 11), padx=4, pady=4)
        scroll = tb.Scrollbar(window)
        self.info.configure(yscrollcommand=scroll.set, wrap="word", state="normal")
        self.info.grid(row=self.rownum, column=0, columnspan=4, sticky="ewn")

        scroll.config(command=self.info.yview)
        scroll.grid(row=self.rownum, column=3, sticky="nse")

        # read only
        self.info.bind("<Key>", lambda e: "break")

        # self.thumb = tb.Label(window)
        # self.thumb.grid(row=self.rownum, column=4, sticky="ew")
    # ----------------------------------------------------------------------------
    def progress_controls(self, window):
        self.rownum += 1
        # tb.Label(window, text="Progress:").grid(row=self.rownum, column=0, sticky="new")

        self.bar = tb.Progressbar(window, orient=tb.HORIZONTAL, length=100, value=0,
                                  mode='determinate', bootstyle="success-striped")
        self.bar.grid(row=self.rownum, column=0, columnspan=3, sticky="ewsn")

        self.percent = tb.Label(window, text="progress: 0%",)
        self.percent.grid(row=self.rownum, column=3)
    # ----------------------------------------------------------------------------
    def footer_buttons(self, window):
        self.rownum += 1
        self.download_btn = tb.Button(window, text="Download", command=self.action_download)
        self.download_btn.grid(row=self.rownum, column=0, sticky="ew")
        self.download_btn.config(state=DISABLED)
        
        self.translation_btn = tb.Button(window, text="Translation", command=self.open_translations_modal, bootstyle="outline") 
        self.translation_btn.grid(row=self.rownum, column=1, sticky="ew")
        self.translation_btn.config(state=DISABLED)
        
        tb.Button(window, text="Settings", command=self.open_settings_modal, bootstyle="outline").grid(row=self.rownum,
                                                                                                       column=2, sticky="ew")
        
        tb.Button(window, text="Open Folder", command=self.open_folder, bootstyle="outline").grid(row=self.rownum,
                                                                                                  column=3, sticky="ew")
        
        # tb.Button(window, text="About", command=self.about_me, bootstyle="outline success").grid(row=self.rownum,
        #                                                                                           column=3, sticky="ew")
    # ----------------------------------------------------------------------------
    def download_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress = (bytes_downloaded / total_size) * 100
        str_progress = f"progress: {progress:.2f}%"

        self.bar.config(value=progress)
        self.percent.config(text=str_progress)
    # ----------------------------------------------------------------------------
    def complete_progress(self, stream, file_path):
        helper.toast_notify("Done!", 'Downloaded Successfully')
    # ----------------------------------------------------------------------------
    def check_url(self, url: str):
        if url == "":
            return False
        
        youtube_regex = (r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        match = re.match(string=url, pattern=youtube_regex)   
        return match is not None
    # ----------------------------------------------------------------------------
    def _paste(self):
        try:
            if self.root.clipboard_get() != "":
                url = self.root.clipboard_get()
                self.url_var.set(url)
                # youtube_regex = (
                #     r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')      
                # match = re.match(string=url, pattern=youtube_regex)     
                if self.check_url(url):
                    self.fetch_data()
                
                else:
                    self.log_line("Error", "Unvalid url!")
            else:
                self.log_line("Error", "Nothing in clipboard!")
        
        except Exception as e:
            helper.show_error(e)
            self.log_line("Error", e)
            self.log_line("Tip", "Try to copy URL and paste it again.")
            self.info.delete(index1="1.0", index2=END)

    # ----------------------------------------------------------------------------
    def _onKeyRelease(self, event):
        # https://stackoverflow.com/a/47496024/2269902
        
        ctrl  = (event.state & 0x4) != 0
        # if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
        #     # event.widget.event_generate("<<Cut>>")
        #     pass
        
        # V
        if event.keycode==86 and ctrl: #and event.keysym.lower() != "v": 
            # event.widget.event_generate("<<Paste>>")
            self._paste()
        # C
        if event.keycode==67 and ctrl: # and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")
            pass
        # X
        if event.keycode==88 and ctrl: # and event.keysym.lower() != "x":
            event.widget.event_generate("<<Cut>>")
            pass
        
        # Z
        if event.keycode==90: #and event.keysym.lower() == "z":
            event.widget.event_generate("<<Undo>>")
            # self.url_var.set("")
        
        # Escape
        if event.keycode==27: #and event.keysym.lower() == "z":
            # event.widget.event_generate("<<Escape>>")
            self.root.destroy()
            exit()
            
        # if event.keycode==13: # and event.keysym.lower() != "return":
        #     event.widget.event_generate("<<Return>>")
                   
        # print(event.keycode, event.keysym.lower())

    # ----------------------------------------------------------------------------
    # ToDo: add ctrl+c
    # def _copy(self, event):
    #     print ('Ctrl-C')
    #     self.root.clipboard_append('text')
    # ----------------------------------------------------------------------------
    # radio button change callback
    def set_val(self, value):
        self._type.set(value)
        url = self.url_var.get()
        if self.check_url(url):
            self.disable_mode(True)
            self.fetch_data()
    # ----------------------------------------------------------------------------
    def set_override(self):
        self.override = not self.skip_existing.get()

    # ----------------------------------------------------------------------------
    def get_description(self, yt) -> str:
        i: int = yt.watch_html.find('"shortDescription":"')
        desc: str = '"'
        i += 20  # excluding the `"shortDescription":"`
        while True:
            letter = yt.watch_html[i]
            desc += letter  # letter can be added in any case
            i += 1
            if letter == '\\':
                desc += yt.watch_html[i]
                i += 1
            elif letter == '"':
                break
        
        # desc = re.sub(r'\\.',lambda x:{'\\n':'\n','\\t':'\t'}.get(x[0],x[0]),desc)
        desc = desc.replace('\\n', "\n").replace('\\t', "\t")

        return desc

    # ----------------------------------------------------------------------------
    # FETCH DATA #--------------------------------------------------------------------------------#
    def fetch_data(self):
        
        # Save user 'type' choice (audio or video)
        self.config.save('MAIN', 'type', self._type.get())
        self.config.save('MAIN', 'override', (not self.skip_existing))
        
        # Refresh download_dir value
        self.downloads_dir = self.config.get(section='MAIN', key='downloads_dir')
            
        # If no link in textbox or clipboard then stop
        if self.url_var.get() =="" and self.root.clipboard_get() == "":
            self.log_line("Error", "URL is required!")
            return 0
        
        # If no link in clipboard but there is one in the textbox use it as input
        if self.root.clipboard_get() =="" :
            self.url_var.set(self.url_var.get())
            self.log_line("Error", "clipboard is empty use textbox")
        
        if not self.check_url( str(self.url_var.get()) ):
            self.log_line("Error", "Unvalid url!")
            return 0
        
        self.clear_file_data()
        
        
        self.disable_mode(True)
        self.qualities.config(values=[], state=DISABLED)
        
        self.bar.config(value=0)
        self.percent.config(text="process: 0%")

        # https://stackoverflow.com/a/49480563/2269902
        threading.Thread(target=self.do_fetch_data).start()
    # ----------------------------------------------------------------------------
    def do_fetch_data(self):
        self.resolutions = []

        if helper.is_valid_path(self.downloads_dir, is_dir=True) != True:
            self.log_line("Error", "Path is not valid!")
            return False
        
        elif self.url.get() == "":
            self.log_line("Error", "URL is not valid!")
            return False
            
        elif helper.is_valid_path(self.downloads_dir, is_dir=True) and self.url.get():

            self.info.delete(index1="1.0", index2=END)
            self.log_line("Process", "Fetching...")

            try:
                self.yt = YouTube(self.url.get(),
                             on_complete_callback=self.complete_progress,
                             use_oauth=self.use_oauth,
                             allow_oauth_cache=self.allow_oauth_cache)

                threading.Thread(target=self.yt.register_on_progress_callback(self.download_progress)).start()
                self.yt.register_on_complete_callback(self.complete_progress)

                # x = InnerTube(client='ANDROID', use_oauth=True, allow_cache=False)
                # # print('InnerTube', x)
                # print('access_token', x.access_token)
                # print('api_key', x.api_key)
                # print('base_params', x.base_params)
                # # print('verify_age', x.verify_age())
                # print('base_data', x.base_data)
                # # helper.dump(x)

                self.store_file_data(self.yt)
                # self.log_info()
                
                
                self.filename = self.file_info['file_name']
                
                # <publish_date>
                # <streaming_data>
                # [streams]
                # {vid_info}
                #

                # try:
                #     self.yt.bypass_age_gate()
                #
                # except Exception:
                #     raise AgeRestrictionError("Age Restriction Error")

                try:
                    self.yt.check_availability()
                except Exception as e:
                    raise helper.UnavailableError(e)

                # if self.yt.age_restricted():
                #     raise AgeRestrictionError("This video has age restrictions.")
                
                _only_audio = False
                progressive = True
                self.ext = '.mp4'
                
                # Get stream
                if self._type.get() == "Audio":
                    _only_audio = True
                    progressive=False
                    self.ext = '.mp3'
                    
                self.log_line("Type", self._type.get())
                self.log_line("Process", "Get streams...")
                self.menu_items2.entryconfig('Open Translations', state="normal")
                self.translation_btn.config(state="normal")
                
                #> GET STREAMS --------------------
                self.streams = self.yt.streams.filter(only_audio=_only_audio, progressive=progressive).desc()

                if len(self.streams) > 0:
                    
                    self.file_extra_info['discription'] = self.get_description(self.yt)
                    
                    # get file qualities
                    i = 1
                    for stream in self.streams:
                        file_size = str(stream.filesize_mb) + " mb"
                        self.file_info['file size ('+str(i)+')'] = file_size
                        self.file_extra_info['download url '+str(i)] = stream.url
                                                
                        if self._type.get() == "Video":
                            self.resolutions.append(str(stream.resolution) + " (" + str(file_size) + ")")
                            self.file_info['resolution ('+str(i)+')'] = str(stream.resolution)

                        elif self._type.get() == "Audio":
                            self.resolutions.append(str(stream.itag) + " (" + str(file_size) + ")")
                            self.file_info['itag ('+str(stream.itag)+')'] = str(stream.resolution)

                        self.qualities.config(values=self.resolutions, state=READONLY, takefocus=True)
                        self.qualities.current(0)
                        
                        i+=1
                        
                    self.disable_mode(False)

                    self.log_info()
                    
                    return True

            except RegexMatchError as e:
                helper.show_error(e)
                self.log_line("RegexMatchError", "URL is not correct, {e}\n")

            except helper.AgeRestrictionError as e:
                helper.show_error(e)
                self.log_line("AgeRestrictionError", e)

            except helper.UnavailableError as e:
                helper.show_error(e)
                self.log_line("UnavailableError", e)

            except helper.PytubeError as e:
                helper.show_error(e)
                self.log_line("PyTubeError", e)

            except Exception as e:
                # self.log_line("Unknown Error", e)
                print("Unknown error:", e)
                helper.show_error(e)
                self.root.destroy()
        else:
            self.log_line("Error", "Not valid path or url, click ctrl+v to paste url")
            return False
    # ----------------------------------------------------------------------------
    # DOWNLOAD #--------------------------------------------------------------------------------#    
    def action_download(self):
        
        self.config.save('MAIN', 'type', self._type.get())
        self.config.save('MAIN', 'override', (not self.skip_existing))
        
        # Refresh download_dir value
        self.downloads_dir = self.config.get(section='MAIN', key='downloads_dir')

        threading.Thread(target=self.do_download).start()
    # ----------------------------------------------------------------------------
    def do_download(self):
        self.quality = self.qualities.get()

        res = self.qualities.get().split()[0]
        
        self.log_separator()
        self.log_line('Quality:',  str(res))
        self.disable_mode(True)

        # DOWNLOAD
        try:
            if len(self.streams) > 0:
                if self._type.get() == 'Video':
                    self.resource = self.streams.get_by_resolution(resolution=res)
                elif self._type.get() == 'Audio':
                    self.resource = self.streams.get_by_itag(itag=int(res))
                else:
                    print("Radio error")

                # add resolution to filename
                self.filename = str(helper.slugify(self.filename))
                self.filename_with_ext = self.filename + "@" + res + self.ext
                
                self.log_line('Proccess',  "Downloading...")
                self.log_line('File name',  self.filename_with_ext)
                # print(self.downloads_dir, self.filename)
                # self.info.insert(END, "Title:\t" + self.filename +"\n")
                # self.get_thumbnail()
                
                #> START DOWNLOADING ---------------------------
                self.resource.download(output_path=self.downloads_dir, filename=self.filename_with_ext, skip_existing=self.override)
            
            else:
                self.log_line('Error', 'No stream found!')

        except Exception as e:
            self.log_line("Unknown Error", e)
            helper.show_error(e)
            self.root.destroy()
            
        finally:
            self.disable_mode(False)
    # ----------------------------------------------------------------------------
    def store_file_data(self, yt):
        self.file_info['title'] = yt.title
        # self.file_info['length1'] = yt.length
        self.file_info['video_id'] = yt.video_id
        self.file_info['author'] = yt.author
        self.file_info['publish_date'] = yt.publish_date
        self.file_info['length'] = str(datetime.timedelta(seconds=yt.length))
        self.file_info['rating'] = yt.rating
        self.file_info['views'] = yt.views
        self.file_info['keywords'] = yt.keywords
        # self.file_info['description'] = yt.description
        self.file_info['watch_url'] = yt.watch_url
        self.file_info['file_name'] = str(helper.slugify(yt.title))
        self.file_extra_info['thumbnail_url'] = yt.thumbnail_url
    # ----------------------------------------------------------------------------
    def clear_file_data(self):
        self.file_info = {}
        self.file_extra_info = {}
    # ----------------------------------------------------------------------------    
    def log_info(self):
        for k in self.file_info:
            self.log_line(k, self.file_info[k])
    # ----------------------------------------------------------------------------
    def log_line(self, title, text):
        self.info.insert(END, chars=f"{title}:\t{text}\n")
        # https://stackoverflow.com/a/17749213/2269902
        self.info.see(tb.END)
        # text.bind('<<Modified>>', scroll_to_end_callback)
    # ----------------------------------------------------------------------------            
    def log_separator(self, char="=", size=50):
        chr = char * size
        self.info.insert(END, chars= chr + "\n")
        self.info.see(tb.END)

    # ----------------------------------------------------------------------------            
    def clear_log_box(self):
        self.info.delete(index1="1.0", index2=END)
    # ----------------------------------------------------------------------------            
    def open_settings_modal(self):
        settings.YPD_Settings()
    # ----------------------------------------------------------------------------
    def open_folder(self):
        dir_path = self.config.get('MAIN', 'downloads_dir')
        
        if os.path.isdir(dir_path):
            
            file_path = dir_path+"/"+self.filename_with_ext
            
            if os.path.isfile(file_path):
                helper.explore_file(file_path)
            
            else:
                helper.explore_folder(dir_path)
        else:
            self.log_line("Error", 'path "' + dir_path + '" is not exist')
    # ----------------------------------------------------------------------------
    def download_thumbnail(self):
        
        try:
            thumb_url = self.file_extra_info['thumbnail_url']
            download_dir = self.config.get("MAIN", 'downloads_dir')
            thumb_name = self.filename + ".jpg"
            download_path = download_dir +"/"+thumb_name
        
            r = requests.get(thumb_url, stream=True)
            
            if r.status_code == 200:
                r.raw.decode_content = True          
                
                with open(download_path, 'wb') as f:
                    f.write(r.content)
                    
                    if os.path.isfile(download_path):
                        cmd = f'explorer.exe /select,"%s"'

                        path = os.path.realpath(download_path)
                        subprocess.Popen(cmd % path)
                
                        helper.toast_notify('Done!', 'Downloaded Successfully into: '+ self.config.get("MAIN", 'downloads_dir'))
                        helper.explore_file(download_path, True)
                        self.log_line("Success", 'Downloaded Successfully into: '+ self.config.get("MAIN", 'downloads_dir')
                                      )
                    else:
                        helper.toast_notify('Error', "path to file 'download_path' is not valid!", tb.DANGER)
                        self.log_line('Error', "path to file 'download_path' is not valid!")
                
            else:
                helper.toast_notify('Error', 'Downloaded thumbnail is fail', tb.DANGER)
                self.log_line('Error', 'Downloaded thumbnail is fail')
                                
        except Exception as e:
            self.log_line('Error', "Coudn't download thumb file")
            helper.show_error(e)        
    # ----------------------------------------------------------------------------
    def download_info(self):
        
        try:
            download_dir = self.config.get("MAIN", 'downloads_dir')
            filename = helper.slugify(self.filename)
            download_path = download_dir +"/"+filename+".txt"
            
            with open(download_path, 'w', encoding="utf-8") as f:
                for line in self.file_info:
                    f.write(line +":\t" + str(self.file_info[line]) + "\n")
                
                for line in self.file_extra_info:
                    f.write(line +":\t" + str(self.file_extra_info[line]) + "\n")
                
                helper.explore_file(download_path)
                helper.toast_notify('Done', 'File info saved successfully', tb.SUCCESS)
                    
        except Exception as e:
            helper.toast_notify('Error', "Couldn't save file info", tb.DANGER) 
            self.log_line('Error', "Couldn't save file info")
            helper.show_error(e)        
    # ----------------------------------------------------------------------------
    @DeprecationWarning
    def __download_translate(self):
        
        video_id = self.file_info['video_id']
        
        if video_id:
            download_dir = self.config.get("MAIN", 'downloads_dir')
            download_path = download_dir +"/"+self.filename+".lang.srt"            

            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                        
            # transcript = transcript_list.find_generated_transcript(['ar'])
            
            # for x, tr in enumerate(transcript_list):
            #     print('lang_code: ', tr.language_code)

            
            transcript = transcript_list.find_transcript(['en', 'ar'])
            # translated_transcript = transcript.translate('ar')
            # print(translated_transcript.fetch())
            # helper.dump(transcript)
            
            if transcript.is_translatable:
                # data["url"] = transcript._url
                # data["is_generated"] = transcript.is_generated
                # data["is_translatable"] = transcript.is_translatable
                # data["language"] = transcript.language
                # data["language_code"] = transcript.language_code
                # data["video_id"] = transcript.video_id
                # data["translate_ar"] = transcript.translate('ar')
                # data["lang_list"] = transcript.translation_languages
                # data["fetch"] = transcript.fetch()
                # data["ar_fetch"] = transcript.translate('ar').fetch()
                
               
                ar = transcript.translate('ar').fetch(preserve_formatting=True)
                
                # UD.bidirectional(u'\u0688')
                
                # for line in ar:
                #     print(line.text, line.start, line.duration)
                
                # https://youtu.be/tvtb6Bg8CFU
                
                formater = SRTFormatter()
                
                # To support RTL in srt files.. I did some updates in the next library:
                # venv\Lib\site-packages\youtube_transcript_api\formatters.py
                # updated code in the file ./transcript-update.txt
                # more info: https://www.w3.org/International/questions/qa-bidi-unicode-controls
                
                srt_formatted = formater.format_transcript(ar)

                with open(download_path, 'w', encoding='utf-8') as srt_file:
                    srt_file.write(srt_formatted)

                # ---------------------------------------------------------
                # download_path = download_dir +"/"+self.filename+".lang.txt"  
                
                # formater = TextFormatter()
                # srt_formatted = formater.format_transcript(ar)
                
                # with open(download_path, 'w', encoding='utf-8') as srt_file:
                #     srt_file.write(srt_formatted)
                # # ---------------------------------------------------------
                # download_path = download_dir +"/"+self.filename+".lang.vtt"  
                
                # formater = WebVTTFormatter()
                # srt_formatted = formater.format_transcript(ar)
                
                # with open(download_path, 'w', encoding='utf-8') as srt_file:
                #     srt_file.write(srt_formatted)
                # # ---------------------------------------------------------
                # download_path = download_dir +"/"+self.filename+".lang.ppf"  
                
                # formater = PrettyPrintFormatter()
                # srt_formatted = formater.format_transcript(ar)
                
                # with open(download_path, 'w', encoding='utf-8') as srt_file:
                #     srt_file.write(srt_formatted)

                    
                
                # with open(download_path, 'w') as f:
                #      f.write()
                
            # - obj._translation_languages_dict : {}
            # - obj._url : Str
            # - obj.fetch()
            # - obj.is_generated : Boolean
            # - obj.is_translatable : Boolean
            # - obj.language = 'English'
            # - obj.language_code = 'en'
            # - obj.translate()
            # - obj.translation_languages : [{}]
            # - obj.video_id : Str

    # ----------------------------------------------------------------------------
    def disable_mode(self, state):
        
        if state == True:
            state = "disabled"
            cursor = "clock"
        else:
            state = "normal"
            cursor = "arrow"
            
        self.root.config(cursor=cursor)
        self.download_btn.config(state=state)
        self.fetch_btn.config(state=state)
        self.translation_btn.config(state=state)
        self.menu_items2.entryconfig("Thumbnail", state=state)
        self.menu_items2.entryconfig("Info", state=state)
        self.menu_items2.entryconfig('Open Translations', state=state) 
    # ----------------------------------------------------------------------------
    def about_me(self):
        answer = Messagebox.yesno("My name is: Hisham Dalal\nDo you want to visit my githup profile?", title="About me", alert=True, parent=self.root, width=200, padding=(25,25))

        if answer == 'Yes':
            url = 'github.com/hishamdalal'
            # new = 2
            # chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

            # Windows
            # chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

            # Linux
            # chrome_path = '/usr/bin/google-chrome %s'

            # webbrowser.get(chrome_path).open(url)
            
            chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            
            if os.path.isfile(chrome_path):
                webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
                webbrowser.get('chrome').open_new_tab(url)
            else:
                webbrowser.open_new_tab(url)
    # ----------------------------------------------------------------------------    
    def open_translations_modal(self):
        
        # url =  self.url_var.get() or self.root.clipboard_get()
        # url = self.url.get()
        translation.YPT_Translations(self.file_info)
    # ----------------------------------------------------------------------------    


YPD()
