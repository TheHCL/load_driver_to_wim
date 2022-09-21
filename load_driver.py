import os
import tkinter as tk
from tkinter import filedialog
import threading
import subprocess

def get_wim_info(): #get wim info
    global wim_selected
    wim_selected = filedialog.askopenfilename()
    wim_selected = wim_selected.replace("/","\\")
    global head,tail
    head,tail = os.path.split(wim_selected)
    os.system("Dism /get-imageinfo /imagefile:"+wim_selected)

def working_directory():
    directory_selected = filedialog.askdirectory()
    directory_selected = directory_selected.replace("/","\\")
    directory_selected+="\\modifiedWIM"
    global wim_file_loc
    wim_file_loc = directory_selected+"\\image"
    global offline_loc
    offline_loc = directory_selected+"\\offline"
    global driver_loc
    driver_loc = directory_selected+"\\drivers"
    global package_loc
    package_loc = directory_selected+"\\package"

    if os.path.exists(directory_selected):
        print("Working space exists.")
    else:
        os.mkdir(directory_selected)
        os.mkdir(wim_file_loc)
        os.mkdir(offline_loc)
        os.mkdir(driver_loc)
        os.mkdir(package_loc)
        os.system("cls")
        print("Working Directory created.\n")


def mount_image():
    lock.acquire()
    os.system("cls")
    print("Copying Wim file to working space.\n Please be patient.")
    os.system("copy "+wim_selected+" "+wim_file_loc)
    global new_wim_loc
    new_wim_loc = wim_file_loc+"\\"+tail
    os.system("cls")
    print("Start to mount image.")
    os.system("Dism /Mount-Image /imagefile:"+new_wim_loc+" /index:"+var.get()+" /MountDir:"+offline_loc)
    os.system("cls")
    print("mount image complete.")
    lock.release()


def add_package():
    tmp=[]
    files = filedialog.askopenfilenames()
    for x in files:
        x = x.replace("/","\\")
        tmp.append(" /PackagePath="+package_loc)
        os.system("copy "+x+" "+package_loc)
    cmd = "Dism /image:"+offline_loc+" /Add-Package"
    for x in tmp:
        cmd+=x
    os.system(cmd)

def get_package():
    os.system("Dism /image:"+offline_loc+" /Get-Packages")
  
        

def add_driver():
    #files = filedialog.askopenfilenames()
    driver_folder_loc = filedialog.askdirectory()
    driver_folder_loc = driver_folder_loc.replace("/","\\")
    # for x in files:
    #     x = x.replace("/","\\")
    #     print(x)
    #     os.system("copy "+x+" "+driver_loc)
    os.system("xcopy "+driver_folder_loc+" "+driver_loc)
    os.system("Dism /image:"+offline_loc+" /Add-Driver /Driver:"+driver_loc+" /Recurse /ForceUnsigned")

def get_driver():
    os.system("Dism /image:"+offline_loc+" /Get-Drivers")


def bypass_nro():
    os.system("cls")
    os.system("reg load HKLM\\OFFLINE "+offline_loc+"\\Windows\\System32\\Config\\SOFTWARE")
    os.system("reg add HKLM\\OFFLINE\\Microsoft\\Windows\\CurrentVersion\\OOBE /v BypassNRO /t REG_DWORD /d 1 /f")
    os.system("reg unload HKLM\\OFFLINE")
    
    #os.system("reg add HLKM\\OFFLINE\\SOFTWARE\\")
    #print("reg load HLKM\\OFFLINE "+offline_loc+"\\Windows\\System32\\Config\\SOFTWARE")
    print("\n\nBypassNRO complete.")


def unmount_image():
    lock.acquire()
    os.system("cls")
    os.system("Dism /Unmount-image /MountDir:"+offline_loc+" /commit")
    lock.release()
    print("\n\n\nUnmont complete.\n wim_file_loc:\n"+new_wim_loc)
    file_open = "explorer "+wim_file_loc
    os.startfile(wim_file_loc)

def thread_mount():
    threading.Thread(target=mount_image).start()
def thread_unmount():
    threading.Thread(target=unmount_image).start()

lock = threading.Lock()

window = tk.Tk()
window.geometry('350x300')
window.title("WIM Modification")
tk.Button(window,text="get Wim info",command=get_wim_info).pack()
var = tk.StringVar()
content = tk.Entry(window,textvariable=var).pack()
tk.Button(window,text="Choose working directory",command=working_directory).pack()
tk.Button(window,text="mount image",command=thread_mount).pack()
tk.Button(window,text="add packages",command=add_package).pack()
tk.Button(window,text="check packages on wim",command=get_package).pack()
tk.Button(window,text="bypass_nro",command=bypass_nro).pack()
tk.Button(window,text="add drivers",command=add_driver).pack()
tk.Button(window,text="check driver on wim",command=get_driver).pack()
tk.Button(window,text="unmount image",command=thread_unmount).pack()
window.mainloop()