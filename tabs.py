try:
    import requests 
    import ttkbootstrap as ttk
    import pandas as pd
    from tkinter import filedialog,StringVar
    from ttkbootstrap.constants import *
    from ttkbootstrap.dialogs import Messagebox
    from Backend_AkhtarT_Damco.Akhtar_Textiles.main import initiate_driver,login,fill_form,quit
    from Backend_AkhtarT_Damco.DAMCO.dynamic2 import Automate
    from Backend_AkhtarT_Damco.DAMCO.ammend import Ammend_Fields
    



    '''
    function to to change text color back on click on entry
    '''
    def on_entry_click(event, entry_widget, default_text):
        if entry_widget.get() == default_text:
            entry_widget.delete(0, 'end')
            entry_widget.config(foreground='black')  # Change text color to black

    '''
    function to to change text color back on away click from entry
    '''
    def on_focus_out(event, entry_widget, default_text):
        if not entry_widget.get():
            entry_widget.insert(0, default_text)
            entry_widget.config(foreground='grey')

    def apply_placeholder(entry_widget, default_text):
        entry_widget.insert(0, default_text)
        entry_widget.config(foreground='grey')  # Set initial text color to grey
        entry_widget.bind('<FocusIn>', lambda event: on_entry_click(event, entry_widget, default_text))
        entry_widget.bind('<FocusOut>', lambda event: on_focus_out(event, entry_widget, default_text))


    def browse_file(entry):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        entry.delete(0, 'end')
        entry.insert(0, file_path)
        entry.config(foreground='black') 
    # root.mainloop()


    root1 = ttk.Window(themename='flatly')

    style = ttk.Style()
    style.configure('success.Outline.TButton',font = ('Helvetica',11))
    style.configure('primary.TButton',font = ('Helvetica',13))


    nb = ttk.Notebook(root1,style='dark')

    '''
    Akhtar textiles Tab code 
    '''

    frame = ttk.Frame(nb,height=600,width=500)


    label_AT = ttk.Label(frame, text='Akhtar Textile Automation',
                        font=('Helvetica',18))
    label_AT.place(relx=0.5,rely=0.05,anchor=N)

    # seperator_AT = ttk.Separator(bootstyle='primary')
    # seperator_AT.place(relx=0.5,rely=0.15,anchor=N,)

    # # frame.grid_columnconfigure(0, weight=1)
    # frame.grid_rowconfigure(0, weight=1)

    browse_button_AT = ttk.Button(frame,
                    width=10, text="Browse", 
                    bootstyle=SUCCESS,command=lambda: browse_file(file_entry_AT),
                    style='success.Outline.TButton')
    browse_button_AT.place(relx=0.95,rely=0.2,anchor=E)

    label_filepath_AT = ttk.Label(frame, text='Filepath:',
                        font=('Helvetica',11))
    label_filepath_AT.place(relx=0.13,rely=0.145,anchor=N)

    file_entry_AT = ttk.Entry(frame,bootstyle='primary',width=50)

    apply_placeholder(file_entry_AT, 'Path to file')

    file_entry_AT.place(relx=0.7,rely=0.2,anchor=E)
    # file_entry_1.place(re)

    nb.add(frame,text='Akhtar Textile Automation')


    username_AT = ttk.Entry(frame,bootstyle='primary',width=50)

    apply_placeholder(username_AT, 'Username')

    username_AT.place(relx=0.7,rely=0.25,anchor=E)

    password_AT = ttk.Entry(frame,bootstyle='primary',width=50)

    apply_placeholder(password_AT, 'Password')

    password_AT.place(relx=0.7,rely=0.3,anchor=E)
                            

    def execute_bot():
        filepath = file_entry_AT.get()
        email = username_AT.get()
        pwd  = password_AT.get()
        if filepath == 'Path to file' or filepath == '':
            Messagebox.show_warning(message='Filepath cannot be empty',
                                    title='Warning',
                                    alert=True)
            return 1
        elif (email == 'Username' or email == '') or (pwd == 'Password' or pwd == ''):
            Messagebox.show_warning(message='username or password cnnot be empty',
                                    title='Warning',
                                    alert=True)
            return 1
        login_data = {
        "email" : email,
        "password" : pwd
        }
        df = pd.read_excel(r'{}'.format(filepath),dtype={'Seal Number': str})
        # root1.withdraw()
        driver = initiate_driver("https://network.infornexus.com/")
        if driver != 'error':
            lgn = login(driver,login_data)
        # else:
        #     lgn = 
        if lgn == 'Login error':
            quit(driver)
            # root1.deiconify()
            error_msg = Messagebox.show_error(message="error in login please check email or passrowd and try again",
                                            title='login error',
                                            alert=True)
            
        elif lgn == 'Login success':
            # try:
            print(f'[INFO] Running in {mode.get()} mode')
            fill_form(driver,df,mode.get())
            # if form == 'closed':
            #     root1.deiconify()
            # except:
            #     root1.deiconify()

    mode = StringVar()

    preview_button = ttk.Radiobutton(frame,text='Preview',variable=mode,value='Preview')
    preview_button.place(relx=0.20,rely=0.35,anchor=E)

    approve_button = ttk.Radiobutton(frame,text='Approve',variable=mode,value='Approve')
    approve_button.place(relx=0.40,rely=0.35,anchor=E)

    execute_button_AT = ttk.Button(
                    frame,
                    width=46, text="Execute", 
                    bootstyle=PRIMARY,command=execute_bot,
                    style='primary.TButton')
    execute_button_AT.place(relx=0.95,rely=0.40,anchor=E)

    try:
        cond_AT = requests.get("https://saim2481.pythonanywhere.com/ATactivation-response/")
        cond_AT.raise_for_status()
        cond_AT = cond_AT.text
    except requests.exceptions.RequestException as e:
        cond_AT = False
        Messagebox.show_error("Connection Error","Please Check your internet Connection")
    except:
        cond_AT = False
        Messagebox.show_error("Something Went Wrong","Unexpected Error")
        
    print(cond_AT)
    print(type(cond_AT))
    print(cond_AT == "true")
    if cond_AT != "true":
        execute_button_AT.configure(state='disabled') 



    '''
    DAMCO Tab code 
    '''
    def execute():
        file_path = file_entry_DAMCO.get()
        username = username_DAMCO.get()
        password = password_DAMCO.get()
        
        file_entry_DAMCO.delete(0, 'end')
        print("Reading From:", file_path)
        # Call the sample function from the dynamic module
        ret = Automate(file_path, username, password)
        if ret == False:
            Messagebox.show_error("Error","Something went wrong")

    def Ammend_data():
        file_path = file_entry_DAMCO.get()
        username = username_DAMCO.get()
        password = password_DAMCO.get()
        
        file_entry_DAMCO.delete(0, 'end')
        print("Reading From:", file_path)
        # Call the sample function from the dynamic module
        ret = Ammend_Fields(file_path, username, password)
        if ret == False:
            Messagebox.show_error("Error","Something went wrong")


    frame2 = ttk.Frame(nb,height=900,width=500)

    label_DAMCO = ttk.Label(frame2, text='DAMCO Automation',
                        font=('Helvetica',18))
    label_DAMCO.place(relx=0.5,rely=0.05,anchor=N)


    browse_button_DAMCO = ttk.Button(frame2,
                    width=10, text="Browse", 
                    bootstyle=SUCCESS,command=lambda: browse_file(file_entry_DAMCO),
                    style='success.Outline.TButton')
    browse_button_DAMCO.place(relx=0.95,rely=0.2,anchor=E)

    label_filepath_DAMCO = ttk.Label(frame2, text='Filepath:',
                        font=('Helvetica',11))
    label_filepath_DAMCO.place(relx=0.13,rely=0.145,anchor=N)
    file_entry_DAMCO = ttk.Entry(frame2,bootstyle='primary',width=50)

    apply_placeholder(file_entry_DAMCO, 'Path to file')

    file_entry_DAMCO.place(relx=0.7,rely=0.2,anchor=E)
    # file_entry_1.place(re)



    username_DAMCO = ttk.Entry(frame2,bootstyle='primary',width=50)

    apply_placeholder(username_DAMCO, 'Username')

    username_DAMCO.place(relx=0.7,rely=0.25,anchor=E)

    password_DAMCO = ttk.Entry(frame2,bootstyle='primary',width=50)

    apply_placeholder(password_DAMCO, 'Password')

    password_DAMCO.place(relx=0.7,rely=0.3,anchor=E)


    try:
        cond = requests.get("https://saim2481.pythonanywhere.com/ATactivation-response/")
        cond.raise_for_status()
        cond = cond.text
    except requests.exceptions.RequestException as e:
        cond = False
        Messagebox.show_error("Connection Error","Please Check your internet Connection")
    except:
        cond = False
        Messagebox.show_error("Something Went Wrong","Unexpected Error")

    print(cond)


    execute_button_DAMCO = ttk.Button(
                    frame2,
                    width=46, text="Execute", 
                    bootstyle=PRIMARY,command=execute,
                    style='primary.TButton')
    execute_button_DAMCO.place(relx=0.95,rely=0.37,anchor=E)

    ammend_button_AT = ttk.Button(
                    frame2,
                    width=46, text="Ammend", 
                    bootstyle=PRIMARY,command=Ammend_data,
                    style='primary.TButton')
    ammend_button_AT.place(relx=0.95,rely=0.43,anchor=E)

    print("-->",cond)
    if not cond == "true":
        execute_button_DAMCO.configure(state=DISABLED)

    nb.add(frame2,text='Damco Automation')
    nb.pack()
    root1.mainloop()

except Exception as e:
    print(e)
    while True:
        pass
