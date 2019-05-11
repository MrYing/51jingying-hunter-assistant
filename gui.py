import time
import random
import tkinter as tk
from tkinter import ttk
from threading import Thread
from utils import log_q, hunters
from assistant import HunterAssistant

root = tk.Tk()
root.geometry('400x320')
root.title('51jingying')
root.resizable(0, 0)


def deliever_card():
    """投递名片"""
    for hunter in hunters:
        hc = HunterAssistant(hunter)
        hc.deliver_card()
        # 切换账号
        time.sleep(random.random()*60)

    # 投递完成
    log_q.put('今日所有猎头任务完成！')
    # 点击退出销毁窗口
    btn.configure(text='退出', command=root.destroy)


def print_log():
    """打印日志信息到listbox"""
    while 1:
        lb.insert(tk.END, log_q.get()) 
        lb.yview_moveto(1)

def run():
    """button按下后的响应函数"""
    btn.configure(text="正在递名片...")
    p1 = Thread(target=deliever_card)
    p1.setDaemon(True)
    p1.start()
    p2 = Thread(target=print_log)
    p2.setDaemon(True)
    p2.start()

# start button
btn = ttk.Button(root, text='递名片', command=run)
btn.pack(pady=10)

# scrollbar
sb = ttk.Scrollbar(root)
sb.pack(side=tk.RIGHT, fill=tk.Y)

# listbox
lb = tk.Listbox(root, yscrollcommand=sb.set)

# 打印开始递名片前的信息
while not log_q.empty():
    lb.insert(tk.END, log_q.get())
    lb.yview_moveto(1)

lb.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)
sb.config(command=lb.yview)

root.mainloop()