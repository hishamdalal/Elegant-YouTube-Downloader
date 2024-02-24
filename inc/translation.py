from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import ttkbootstrap as tb
# from ttkbootstrap.icons import Icon
# from PIL import Image, ImageTk
# from ttkbootstrap.icons import Emoji
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
# from youtube_transcript_api.formatters import WebVTTFormatter
# from youtube_transcript_api.formatters import TextFormatter
# from youtube_transcript_api.formatters import PrettyPrintFormatter


from inc.config import YPD_Config
# from inc.helper import window_center
import inc.helper as helper

class mySRTFormatter(SRTFormatter):
    def _format_transcript_helper(self, i, time_text, line):
        # rtl_char = '‫'
        # rtl_char = '\u202B'
        # ascii_unsupported = '\u202B'
        
        # https://www.w3.org/International/questions/qa-bidi-unicode-controls

        start = u'\u200F' + u'\u202E' + u'\u202B'
        end = u'\u202C'
        
        text = ""
        ary = line['text'].split("\n")
        for l in ary:
            text += start + l + end + "\n"
        # rtl_char = str(ascii_unsupported.encode('utf-8'))
        # rtl_char = str(int('202B', 16).to_bytes(4, 'big'), 'utf_32_be')
        return "{}\n{}\n{}".format(i + 1, time_text, text)



class YPT_Translations:
    current = {}
    rownum = 0
    url = ""
    url_var2 = None
    file_info = {}
    video_id = ""
    langs = {}
    download_path = ""
    var_from = ""
    var_to = ""

    # ----------------------------------------------------------------------------
    def __init__(self, file_info):
        self.config = YPD_Config()
        self.file_info = file_info
           
        
        w = 700
        h = 250
        
        window = tb.Toplevel(minsize=(w, h))
        window.configure(padx=20, pady=20)
        window.title("Translations")
        window.iconbitmap('images/YouTube.ico')
        
        helper.window_center(window, w, h)

        self.init_current_settings()
        self.layout(window)
        self.controls(window)
        self.window = window
        self.window.after(400, self.set_file_info )
        self.window.after(500, self._fill_lang_list )
        self.window.after(600, self.set_current_settings )

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    def init_current_settings(self):
        self.current['lang_from'] = self.config.get(section='MAIN', key='lang_from')
        self.current['lang_to'] = self.config.get(section='MAIN', key='lang_to')
    
    # ----------------------------------------------------------------------------
    def set_current_settings(self):
        if len(self.current):
            lang_from = self.current['lang_from']
            lang_to = self.current['lang_to']
            
            # _from = lang_from.split(' - ')[0]
            # _to = lang_to.split(' - ')[0]
            
            self.var_from.set(lang_from)
            self.var_to.set(lang_to)
        
        else:
            print("Couldn't set default values")
        
    # ----------------------------------------------------------------------------
    def save_settings(self, lang_from, lang_to):
        try:
            self.config.save(section='MAIN', key='lang_from', value=lang_from)
            self.config.save(section='MAIN', key='lang_to', value=lang_to)
            
            helper.toast_notify("Save Setting", 'Settings saved successfully')
            
        except Exception as e:
            print(e)
   
    # ----------------------------------------------------------------------------
    def set_url(self):
        # string_var = StringVar()
        # string_var.set(url)
        # self.url_var2 = string_var
        # video_id = self.url.split('?v=')[1]
        # video_id = self.url_ctrl.get()
        # self.url_var2.set(video_id)
        pass        
    
    # ----------------------------------------------------------------------------
    def set_file_info(self):

        if self.file_info['video_id']:
            self.video_id = self.file_info['video_id']
            self.url_var2.set(self.video_id)
            
        else:
            print('Errrrorrrr--------')
        
    # ----------------------------------------------------------------------------
    def layout(self, window):
        window.grid_columnconfigure(index=0, weight=2, uniform='a')
        window.grid_columnconfigure(index=1, weight=2, uniform='a')
        window.grid_columnconfigure(index=2, weight=2, uniform='a')
        # window.grid_columnconfigure(index=3, weight=2, uniform='a')

        window.grid_rowconfigure(index=0, weight=3, uniform='a')
        window.grid_rowconfigure(index=1, weight=2, uniform='a')
        window.grid_rowconfigure(index=2, weight=2, uniform='a')
        window.grid_rowconfigure(index=3, weight=2, uniform='a')
        window.grid_rowconfigure(index=4, weight=2, uniform='a')
    
    # ----------------------------------------------------------------------------
    def controls(self, window):
        self.header(window)
        self.url_controls(window)
        self.from_control(window)
        self.to_control(window)
        self.footer_buttons(window)
    
    # ----------------------------------------------------------------------------
    def header(self, window):
        tb.Label(window, text="Translations", font=('Arial', 20), justify=tb.CENTER).grid(row=0, column=0, columnspan=4)
    
    # ----------------------------------------------------------------------------
    def url_controls(self, window):
        self.rownum += 1
        tb.Label(window, text="Video URL:").grid(row=self.rownum, column=0, sticky="ew")
        
        url_var2 = StringVar()
        self.url_var2 = url_var2


        self.url_ctrl = tb.Entry(window, textvariable=self.url_var2)
        self.url_ctrl.grid(row=self.rownum, column=1, columnspan=2, sticky="ew")
        
        
        # print('self.url:', self.url)
        # print('url_var2.get', url_var2.get(), url_var2)
        # print('self.url_var2.get', self.url_var2.get(), self.url_var2)

        
        # photo = PhotoImage(file = "../images/YouTube.ico") 
        # photo = ImageTk.PhotoImage(Image.open('images/YouTube-png-16.png'))
        # search_icon = Emoji.get('RIGHT-POINTING MAGNIFYING GLASS')
        # self.url_var2.set(self.url)
        # tb.Button(window, text="Start", cursor="hand2", compound=tb.LEFT, command=self.set_url).grid(row=self.rownum, column=3, sticky="ew")
    
    # ----------------------------------------------------------------------------
    def from_control(self, window):
        self.rownum += 1
        tb.Label(window, text="From:").grid(row=self.rownum, column=0, sticky="ew")
        
        lang_list = []
        var_from = StringVar()
        self.var_from = var_from
        self.lang_from = tb.Combobox(window, name="lang_from", values=lang_list, textvariable=var_from)
        self.lang_from.grid(row=self.rownum, column=1, columnspan=2, sticky="ew")
        
        # var_from.trace('w', self.get_index)
        # self.lang_from.bind("<<ComboboxSelected>>", self.get_index)
        # var1.set('720')
        # self.lang_from.current(0)

        self.lang_from['state'] = 'readonly'
    
    # def get_index(self, arg):
    #     g = self.lang_from.get()
    #     c = self.lang_from.current()
    #     print(g, c)

    # ----------------------------------------------------------------------------
    def to_control(self, window):
        self.rownum += 1
        tb.Label(window, text="To:").grid(row=self.rownum, column=0, sticky="ew")

        lang_list = []
        var_to = StringVar()
        self.var_to = var_to
        self.lang_to = tb.Combobox(window, name="lang_to", values=lang_list, textvariable=var_to)
        self.lang_to.grid(row=self.rownum, column=1, columnspan=2, sticky="ew")

        # var1.set('720')
        # self.lang_to.current(0)

        self.lang_to['state'] = 'readonly'

    # ----------------------------------------------------------------------------
    def footer_buttons(self, window):
        self.rownum += 1
        tb.Button(window, text="Start", command=self.download_translate).grid(row=self.rownum, column=1, sticky="ew")
        tb.Button(window, text="Open Folder", command=self.open_folder, bootstyle="outline").grid(row=self.rownum, column=2, sticky="ew")
    
    # ----------------------------------------------------------------------------
    def _fill_lang_list(self):
        video_id = self.video_id
        # f = self.lang_from.get()
        # t = self.lang_to.get()
        
        self.lang_list = []
        if video_id:
            # print(video_id, f, t)
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                
                for transcript in transcript_list:
                    self.langs = transcript.translation_languages
                    break
                
                for lang in self.langs:
                    # lang_name = lang['language_code'] +' - ' + lang['language']
                    lang_name = (lang['language_code']).upper() +' - ' + lang['language']
                    self.lang_list.append(lang_name)
                                
                self.lang_from.config(values=self.lang_list)
                self.lang_from.current(0)
                
                self.lang_to.config(values=self.lang_list)
                self.lang_to.current(1)
                # self.qualities.config(values=self.resolutions, state=READONLY, takefocus=True)
            except Exception as e:
                # self.method['toast_notify']("Error", "Couldn't downloaded translation")
                # self.method['print_line']("Error", "Couldn't downloaded translation")
                print('ERROR::', e)
    
    # ----------------------------------------------------------------------------
    def download_translate(self):
        
        # video_id = self.url_var2
        video_id = self.video_id
        try:
            if self.video_id:
                
                lang_from = str(self.lang_from.get()) or 'en - English'   
                lang_to = str(self.lang_to.get()) or 'ar - Arabic'
                
                self.save_settings(lang_from, lang_to)
                              
                lang_to = (lang_to.split(' - ')[0]).lower()
                lang_from = (lang_from.split(' - ')[0]).lower()

                
                # print('lang_from', lang_from)
                # print('lang_to', lang_to)
                
                filename = self.file_info['file_name']
                self.download_dir = self.config.get("MAIN", 'downloads_dir')
                self.download_path = self.download_dir +"/"+filename+"@"+lang_to+".srt"      
                # YouTubeTranscriptApi.get_transcript(self.video_id, languages=['de', 'en'])
                transcript_list = YouTubeTranscriptApi.list_transcripts(self.video_id)
                            
                # # filter for manually created transcripts
                # transcript_manually = transcript_list.find_manually_created_transcript([lang_from, 'en'])
                # # or automatically generated ones
                # transcript_automaticlly = transcript_list.find_generated_transcript([lang_from, 'en'])
                
                # # print(transcript_manually.translation_languages)
                
                # print('manually', transcript_manually.is_translatable, transcript_manually.translation_languages)
                # print('automaticlly', transcript_automaticlly.is_translatable, transcript_automaticlly.translation_languages)
                transcript = transcript_list.find_transcript([lang_from, 'en'])
                
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
                                
                    selected_lang = transcript.translate(lang_to).fetch(preserve_formatting=True)
                    
                    # https://youtu.be/tvtb6Bg8CFU
                    
                    formater = mySRTFormatter()
                    
                    # To support RTL in srt files.. I did some updates in the next library:
                    # venv\Lib\site-packages\youtube_transcript_api\formatters.py
                    # updated code in the file ./transcript-update.txt
                    # more info: https://www.w3.org/International/questions/qa-bidi-unicode-controls
                    
                    srt_formatted = formater.format_transcript(selected_lang)
                    with open(self.download_path, 'w', encoding='utf-8') as srt_file:
                        srt_file.write(srt_formatted)
        
                    print(self.download_path)
                    print("SUCCESS")
                    helper.explore_file(self.download_path)
                    helper.toast_notify("Success", "Translation downloaded successfully")
                    # helper.print_line("Success", "Translation downloaded successfully")
                    
                else:
                    print("This video is not translatable!")  
                                    
            else:
                # raise Exception("Video is is empty!")
                print("Video is is empty!")
                
        # except TranscriptsDisabled as e:
        #     print('TranscriptsDisabled Exception::', e)
            
        except Exception as e:
            print('Exception::', e)
            helper.show_error(e)
            
    # ----------------------------------------------------------------------------
    def open_folder(self):
        if self.download_path != "":
            helper.explore_file(self.download_path)
        else:
            downloads_dir = self.config.get(section='MAIN', key='downloads_dir')
            helper.explore_file(downloads_dir)
    # ----------------------------------------------------------------------------
