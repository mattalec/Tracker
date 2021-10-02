import tkinter as tk
from tkinter import filedialog, Text, PhotoImage
import os
import pandas as pd
import numpy as np
import datetime as dt

# sleep stuff

qs = ['get into bed','sleep','wake','get out of bed']
ans = ['','','','']

def valid_input(entry):
    valid = False
    try:
        x = dt.datetime.strptime(entry,'%H:%M').time()
        valid = True
    except:
        try:
            x = dt.datetime.strptime(entry,'%H').time()
            valid = True
        except:
            sleep_err_label['text'] = 'please input time in HH:MM or H format'
    return valid

def sleepclick(event):
    entry = str(sleep_entry_text.get())
    sleep_entry_text.set('')
    q = int(q_count['text'])
    sleep_err_label['text'] = ''
    if ((q == -1) and (entry.lower() == 'start')):
        q += 1
        sleep_o_label['text'] = f'what time did you {qs[q]}?'
    elif ((q >= 0) and (q < 4)):
        if (valid_input(entry)):
            ans[q] = entry
            q += 1
            if (q == 4):
                efficiency = efficiency_calc(ans)
                sleep_o_label['text'] = f'Youve completed the sleep tracker, \nYour efficiency for last night was {efficiency*100}% \nPlease type "retry" if you would like to go again'                
                q += 1
            else:
                sleep_o_label['text'] = f'what time did you {qs[q]}?'
    elif ((q == 5) and (entry.lower() == 'retry')):
        q = -1
        sleep_o_label['text'] = 'type "start" below to input sleep'
    elif (entry == ''):
        return
    elif (((q == -1) or (q == 5)) and ((entry.lower() != 'start') or (entry.lower() != 'retry'))):
        sleep_err_label['text'] = 'please input the "word" in quotation marks'
    q_count['text'] = int(q)            

def efficiency_calc(ans):
    for num, i in enumerate(ans):
        if ':' in i:
            ans[num] = dt.datetime.strptime(i,'%H:%M').time()
        else:
            ans[num] = dt.datetime.strptime(i,'%H').time()
            
    day = dt.datetime.now().date()
    next_day = day
    next_sleep = day
    in_bed = ans[0]
    sleep = ans[1]
    wake = ans[2]
    out_bed = ans[3]
    
    if in_bed > dt.time(12,0):
        next_day = day + dt.timedelta(days=1)
    if sleep > dt.time(12,0):
        next_sleep = day + dt.timedelta(days=1)
    time_bed = dt.datetime.combine(next_day, out_bed) - dt.datetime.combine(day, in_bed)
    time_asleep = dt.datetime.combine(next_sleep, wake) - dt.datetime.combine(day,sleep)
    efficiency = np.round(time_asleep/time_bed, 4)
	
    ds = pd.read_csv('daily_tracks.csv').drop('Unnamed: 0',axis = 1)
    header = ['date', 'in_bed', 'sleep', 'wake', 'out_bed', 'efficiency']

        
    to_add = pd.DataFrame([[day.strftime("%d/%m/%y"),
                            in_bed.strftime('%H:%M'),
                            sleep.strftime('%H:%M'),
                            wake.strftime('%H:%M'),
                            out_bed.strftime('%H:%M'),
                            efficiency]], columns=header)
    ds = ds.append(to_add)
    ds.to_csv('./daily_tracks.csv')
    return efficiency            

# task stuff
def load_tasks():
    ds_tasks = pd.read_csv('tasks.csv').drop('Unnamed: 0',axis = 1)
    for i in range(ds_tasks.shape[0]):
        task_label[i]['text'] = ds_tasks.iloc[i]['header']

def task_save():
    task_number = int(task_track['text'])
    header = str(task_header_text.get())
    content = str(task_o_entry.get(1.0,'end'))
    
    ds_tasks = pd.read_csv('tasks.csv').drop('Unnamed: 0',axis = 1)
    ds_tasks.iloc[task_number] = [header, content]    
    ds_tasks.to_csv('tasks.csv')
    load_tasks()
            
def task_open(task_number):
    ds_tasks = pd.read_csv('tasks.csv').drop('Unnamed: 0',axis = 1)
    header, content = ds_tasks.iloc[task_number]
    
    task_track['text'] = task_number
    task_header_text.set(header)
    task_o_entry.delete(1.0,'end')
    task_o_entry.insert(1.0,content)

def task_delete(task_number):
    ds_tasks = pd.read_csv('tasks.csv').drop('Unnamed: 0',axis = 1)
    done_tasks = pd.read_csv('tasks.csv').drop('Unnamed: 0',axis = 1)
    done_tasks = done_tasks.append(ds_tasks.iloc[task_number])
    ds_tasks.iloc[task_number] = [' ',' ']
    ds_tasks.to_csv('tasks.csv')
    done_tasks.to_csv('done_tasks.csv')

    load_tasks()

# planner stuff
    
def hour_save(hour_num):
    ds_planner = pd.read_csv('planner.csv').drop('Unnamed: 0',axis = 1)
    half1 = half1s[hour_num].get(1.0,'end')
    half2 = half2s[hour_num].get(1.0,'end')
    ds_planner.iloc[hour_num] = [half1, half2]

def hour_clear(hour_num):
    ds_plan = pd.read_csv('planner.csv').drop('Unnamed: 0',axis = 1)
    ds_plan.iloc[hour_num] = [' ',' ']
    ds_plan.to_csv('planner.csv')
    load_planner()

def load_planner():
    ds_plan = pd.read_csv('planner.csv').drop('Unnamed: 0',axis = 1)
    for i in range(ds_plan.shape[0]):
        half1, half2 = ds_plan.iloc[i]
        half1s[i].delete(1.0,'end')
        half1s[i].insert(1.0,half1)
        half2s[i].delete(1.0,'end')
        half2s[i].insert(1.0,half2)

# habit tracker

def check_track():
    varmed.get()

root = tk.Tk()

height = 1080
width = 1920

canvas = tk.Canvas(root, height=height, width=width, bg='grey')
canvas.pack()

bg = PhotoImage(file = "bg.png")
label1 = tk.Label(root, image = bg)
label1.place(x = 0, y = 0)

# sleep stuff
sleep_o_frame = tk.Frame(root, bg='white')
sleep_o_frame.place(relwidth=0.3, relheight=0.09, relx=0.01, rely=0.02)
sleep_i_frame = tk.Frame(root, bg='white')
sleep_i_frame.place(relwidth=0.3, relheight=0.03, relx=0.01, rely=0.14)
sleep_err_frame = tk.Frame(root, bg='black')
sleep_err_frame.place(relwidth=0.3, relheight=0.02, relx = 0.01, rely=0.12)
q_count_frame = tk.Frame(root)

q_count = tk.Label(q_count_frame, text=-1)
sleep_o_label = tk.Message(sleep_o_frame, text='type "start" below to input sleep', bg='white', aspect=1000, justify='center')
sleep_o_label.place(relwidth=1, relheight=1)
sleep_entry_text = tk.StringVar()
sleep_entry = tk.Entry(sleep_i_frame, textvariable=sleep_entry_text)
sleep_entry.place(relwidth=1, relheight=1, relx = 0.4)
root.bind('<Return>', sleepclick)
sleep_button =tk.Button(root, text='submit')
sleep_button.bind('<Button-1>', sleepclick)
sleep_button.pack()

sleep_err_label = tk.Label(sleep_err_frame, bg='black', fg='white')
sleep_err_label.place(relwidth=1, relheight=1)

# task stuff
task_o_frame = tk.Frame(root, bg='white')
task_o_frame.place(relwidth = 0.5, relheight = 0.27+0.16, relx = 0.48, rely=0.05)
task_track_frame = tk.Frame(root)
task_header_frame = tk.Frame(root)
task_header_frame.place(relwidth = 0.5, relheight = 0.02, relx = 0.48, rely=0.02)

task_track = tk.Label(task_track_frame, text=-1)
task_header_text = tk.StringVar()
task_header = tk.Entry(task_header_frame, textvariable=task_header_text)
task_header.place(relwidth = 0.8, relheight = 1, relx = 0.2)
subject_label = tk.Label(task_header_frame, text='subject: ', anchor='e')
subject_label.place(relheight=1, relwidth=0.2, relx=0)

task_o_entry = tk.Text(task_o_frame, padx=10, pady=10)
task_o_entry.place(relwidth=1, relheight=1)

n = 10
task_list = [f'task_frame_{i}' for i in range(n)]
task_list_open = [f'task_openframe_{i}' for i in range(n)]
task_list_del = [f'task_delframe_{i}' for i in range(n)]
task_label = [f'task_label_{i}' for i in range(n)]
task_open_button = [f'task_opbutton_{i}' for i in range(n)]
task_del_button = [f'task_delbutton_{i}' for i in range(n)]

for i in range(n):
    task_list[i] = tk.Frame(root, bg='white')
    task_list[i].place(relwidth=0.35, relheight=0.03, relx=0.50, rely=0.33+(i*0.04)+0.16)
    task_label[i] = tk.Label(task_list[i])
    task_label[i].place(relwidth=1, relheight=1)
    
    task_list_open[i] = tk.Frame(root, bg='white')
    task_list_open[i].place(relwidth=0.05, relheight=0.03, relx=0.855, rely=0.33+(i*0.04)+0.16)
    task_open_button[i] = tk.Button(task_list_open[i], text='OPEN', command=lambda i=i: task_open(int(i)), bg='green')
    task_open_button[i].place(relwidth=1, relheight=1)   
    
    task_list_del[i] = tk.Frame(root, bg='white')
    task_list_del[i].place(relwidth=0.05, relheight=0.03, relx=0.91, rely=0.33+(i*0.04)+0.16) 
    task_del_button[i] = tk.Button(task_list_del[i], text='DELETE', command=lambda i=i: task_delete(int(i)), bg='red')
    task_del_button[i].place(relwidth=1, relheight=1)  
    
task_rsidebar = tk.Frame(root, bg='black')
task_rsidebar.place(relwidth=0.015, relheight=(0.04*n-0.01), relx=0.965, rely=0.33+0.16 )
task_lsidebar = tk.Frame(root, bg='black')
task_lsidebar.place(relwidth=0.02, relheight=(0.04*n-0.01), relx=0.48, rely=0.33+0.16 )
task_rgap = tk.Label(task_rsidebar, bg='white')
task_rgap.place(relwidth = 0.1, relheight=0.97, relx = 0.55, rely=0.015)
task_lgap = tk.Label(task_lsidebar, bg='white')
task_lgap.place(relwidth = 0.3, relheight=0.97, relx = 0.25, rely=0.015)
task_ubar = tk.Frame(root, bg='black')
task_ubar.place(relwidth = 0.5, relheight = 0.005, relx = 0.48, rely=0.325+0.16)
task_dbar = tk.Frame(root, bg='black')
task_dbar.place(relwidth = 0.5, relheight = 0.005, relx = 0.48, rely=0.32+(n*0.04)+0.16)

task_save_button = tk.Button(task_o_frame, text='save task', command=task_save)
task_save_button.place(relwidth = 1, relheight = 0.08, relx = 0, rely=0.92)

load_tasks()

# planner stuff
hrs = 19
hour_list = [f'{i}hr_frame' for i in range(hrs)]
time_splits = [f'{i}hr_frame' for i in range(int((hrs+1)/2))]
half1s = [f'{i}halfhr' for i in range(hrs)]
half2s = [f'{i}halfhr' for i in range(hrs)]
savehr = [f'save{i}' for i in range(hrs)]
clearhr = [f'clear{i}' for i in range(hrs)]

for i in range(hrs):
    
    weekday = dt.datetime.now().weekday()
    if weekday in [0,1]:
        work_day = 'black'
        work_text = 'white'
    else:
        work_day = 'white'
        work_text = 'black'
    
    hour_list[i] = tk.Frame(root, bg='white')
    hour_list[i].place(relwidth=0.3, relheight=0.03, relx=0.01, rely=0.22+(0.035*i))

    if (i >= 6) and (i <= 12):
        half1s[i] = tk.Text(hour_list[i], bg=work_day, fg=work_text, padx=10)
        half1s[i].place(relwidth=0.42, relheight=1, relx=0.08)
        half2s[i] = tk.Text(hour_list[i], bg=work_day, fg=work_text, padx=10)
        half2s[i].place(relwidth=0.45, relheight=1, relx=0.5)
        hour = tk.Label(hour_list[i], text=f'{(i+7)%24}hr', bg=work_day, fg=work_text, anchor='e')
        hour.place(relwidth=0.08, relheight=1)
    else:
        half1s[i] = tk.Text(hour_list[i], bg='white', padx=10)
        half1s[i].place(relwidth=0.42, relheight=1, relx=0.08)
        half2s[i] = tk.Text(hour_list[i], bg='white', padx=10)
        half2s[i].place(relwidth=0.45, relheight=1, relx=0.5)
        hour = tk.Label(hour_list[i], text=f'{(i+7)%24}hr', bg='white', anchor='e')
        hour.place(relwidth=0.08, relheight=1)
    
    savehr[i] = tk.Button(hour_list[i], command=lambda i=i: hour_save(int(i)), bg='green')
    savehr[i].place(relheight=1, relwidth=0.025, relx=0.95)
    clearhr[i] = tk.Button(hour_list[i], command=lambda i=i: hour_clear(int(i)), bg='red')
    clearhr[i].place(relheight=1, relwidth=0.025, relx=0.975)
    
    if i % 2 == 0:
        num = int((i)/2)
        if (i == 4) or (i == 16):
            time_splits[num] = tk.Frame(root, bg='red')
            time_splits[num].place(relwidth=0.3, relheight=0.005, relx=0.01, rely=0.25+(0.035*i))   
        else:
            time_splits[num] = tk.Frame(root, bg='green')
            time_splits[num].place(relwidth=0.3, relheight=0.005, relx=0.01, rely=0.25+(0.035*i))           
            
load_planner()
    
vmed = tk.IntVar()
vread = tk.IntVar()

def checked(checkvar):
    if (checkvar.get()):
        checkvar.set(1)
    else:
        checkvar.set(0)

habit_frame = tk.Frame(root, bg='white')
habit_frame.place(relwidth=0.10, relheight=0.87, relx=0.345, rely=0.02)
medc = tk.Checkbutton(habit_frame, text='meditation', variable=vmed, onvalue=1, offvalue=0, command='checked(vmed)')
medc.place(relwidth=1, relheight=0.1, relx=0)
readc = tk.Checkbutton(habit_frame, text='reading', variable=vread, onvalue=1, offvalue=0, command='checked(vread)')
readc.place(relwidth=1, relheight=0.1, rely=0.1)
medc = tk.Checkbutton(habit_frame, text='meditation', variable=vmed, onvalue=1, offvalue=0, command='checked(vmed)')
medc.place(relwidth=1, relheight=0.1, relx=0)

root.mainloop()


