__author__ = 'jeff'

# import tkinter
import tkinter.messagebox
from tkinter import *
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter import Tk, Label, Entry, StringVar, Button, Pack, BOTTOM, LEFT

from word_replace import pares


class GuiHandler(object):

    @staticmethod
    def test(cls):
        pass

    @classmethod
    def select_path(cls, path):
        p = askdirectory()
        if p is None:
            pass
        else:
            path.set(p)

    @classmethod
    def select_file(cls, path):
        """"""
        p = askopenfilename()
        if p is None:
            pass
        else:
            path.set(p)

    @classmethod
    def render(cls, **kwargs):
        """"""
        settings = kwargs['settings_file'][0].get()
        sub_dir = kwargs['sub_dir'][0].get()
        temp_dir = kwargs['template'][0].get()
        output_dir = kwargs['output_dir'][0].get()
        for k, v in kwargs.items():
            if len(v[0].get().strip()) == 0:
                msg = "请注意， %s   必须填" % v[1]
                tkinter.messagebox.showwarning(title="错误提示", message=msg)
                return
        try:
            pares(
                settings=settings,
                sub_dir=sub_dir,
                temp_dir=temp_dir,
                output_dir=output_dir
            )
        except Exception as e:
            msg = e.msg
            tkinter.messagebox.showwarning(title="错误提示", message=msg)
        else:
            tkinter.messagebox.showinfo(title="提示", message="渲染成功")


class RenderGui(object):

    def __init__(self):
        self.root = self.generate_root()
        # Pack()
        # self.template = self.generate_ask_directory('template', '模板文件夹:')
        # self.sub_file = self.generate_ask_file('sub_file', '子文件:')
        self.template = FileAskFrame(master=self.root, label_name='template',
                                     handler=GuiHandler.select_path, description='模板文件夹:')
        self.sub_dir = FileAskFrame(master=self.root, label_name='sub_file',
                                    handler=GuiHandler.select_path, description='子文件夹:')
        self.settings_file = FileAskFrame(master=self.root, label_name='settings',
                                          handler=GuiHandler.select_file, description="配置文件")
        self.output_dir = FileAskFrame(master=self.root, label_name='output_dir',
                                       handler=GuiHandler.select_path, description="输入文件夹")
        self.render_button = self.generate_confirm_button()
        self.cancel_button = self.generate_cancel_button()
        self.layout()

    def generate_root(self):
        root = Tk()
        root.title('test1')
        root.geometry('600x800')
        screen_with, screen_hei = root.maxsize()
        # current_with = root.winfo_reqwidth()
        current_with = 600
        # current_hei = root.winfo_reqheight()
        current_hei = 800
        root.geometry(
            "{}x{}+{}+{}".format(current_with, current_hei, int(screen_with / 2 - current_with / 2),
                                 int(screen_hei / 2 - current_hei / 2)))
        return root

    def layout(self):
        """"""
        # self.layout_rows(self.template, 1)
        # self.layout_rows(self.sub_file, 3)
        self.template.place(relx=0.2, rely=0.1)
        self.settings_file.place(relx=0.2, rely=0.2)
        self.sub_dir.place(relx=0.2, rely=0.3)
        self.output_dir.place(relx=0.2, rely=0.4)
        self.render_button.place(relx=0.2, rely=0.6)
        self.cancel_button.place(relx=0.4, rely=0.6)

    def layout_rows(self, kj, row):
        """"""
        kj['label'].grid(row=row, column=1, )
        kj['ent'].grid(row=row, column=2, columnspan=2)
        kj['button'].grid(row=row, column=4, sticky=E)

    def generate_confirm_button(self):
        """"""
        name = 'confirm'
        description = '渲染'
        kwargs = {
            'template': (self.template.cmp['path_var'], self.template.cmp['description']),
            'sub_dir': (self.sub_dir.cmp['path_var'], self.sub_dir.cmp['description']),
            'settings_file': (self.settings_file.cmp['path_var'], self.settings_file.cmp['description']),
            'output_dir': (self.output_dir.cmp['path_var'], self.output_dir.cmp['description'])
        }
        button = Button(text=description or name, command=lambda: GuiHandler.render(**kwargs))
        return button

    def generate_cancel_button(self):
        """"""
        return Button(text="退出", command=self.root.quit)

    def run(self):
        self.root.mainloop()



def test():
    # x = 1
    # z = lambda m: x+1
    # # print(z())
    tkinter.messagebox.showinfo(title="提示", message="渲染成功")


class FileAskFrame(Frame):
    """"""

    def __init__(self, master, label_name, handler, *args, description=None, **kwargs):
        super(FileAskFrame, self).__init__(master, *args, **kwargs)
        self.master = master
        self.cmp = self.init_ask(label_name, handler, description)

    def init_ask(self, label_name, handler, description=None):
        path_var = StringVar()
        label = Label(self, text=description or label_name, width=10).grid(row=0, column=0)
        ent = Entry(self, text=path_var, width=30).grid(row=0, column=1, columnspan=3)
        button = Button(self, text='请选择路径', command=lambda: handler(path_var)).grid(row=0, column=5)
        res = {
            'label': label,
            'button': button,
            'ent': ent,
            'path_var': path_var,
            'description': description or label_name
        }
        return res


if __name__ == '__main__':
    RenderGui().run()
    # test()

    # r = Tk()
    # a = FileAskFrame(r, 'test')
    # a.pack()
    # r.mainloop()


