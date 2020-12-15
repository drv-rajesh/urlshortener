#Created by Dhruv Rajesh

#Import Libraries
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import requests

#Create the class to nest all functions
class Url_Shorten:

    #Constructor
    def __init__(self, master):

        #UI Code
        #----------------------
        #Create the Root Window
        master.title('URL Shortener by Dhruv R')
        master.geometry("330x100")
        master.resizable(False, False)

        #Create the URL Entry Box
        self.url = ttk.Entry(master, width=30, font=('Arial',9))
        self.url.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.url.insert(0, "Enter URL to Shorten")

        #Create the Username Entry Box
        self.username = ttk.Entry(master, width=30, font=('Arial',9))
        self.username.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.username.insert(0, "Enter Bitly Username")

        #Create the Password Entry Box
        self.password = ttk.Entry(master, width=30, font=('Arial',9))
        self.password.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.password.insert(0, "Enter Bitly Password")

        #Create the Shorten URL Button
        ttk.Button(master, text="Shorten!", command=self.shorten_url).grid(row=0, column=1, rowspan=3, padx=5, sticky='e')
        #----------------------

    def get_groupuid(self, uname, pwd):

        #API Invocation
        #------------------------
        #Fetch Access Token to Use Bitly's API
        self.access_token = requests.post("https://api-ssl.bitly.com/oauth/access_token", auth=(uname, pwd)).content.decode()

        try:
            
            #Fetch GroupUID for Authorization using the Access Token
            self.gUID = requests.get("https://api-ssl.bitly.com/v4/groups", headers={"Authorization": f"Bearer {self.access_token}"}).json()['groups'][0]
            
        except KeyError:

            #Display an Error and Stop Execution
            messagebox.showinfo(title="Url Shortener by Dhruv R", message="The specified credential combination does not exist.")
            exit()
            
        self.gUID = self.gUID['guid']
        #-------------------------

        #Return the Access Token and GroupUID
        return self.access_token, self.gUID

    def shorten_url(self):

        #API Invocation
        #--------------------------
        self.uname = self.username.get()
        self.pwd = self.password.get()

        try:
            
            #Try to Get the URL from the URL Entry Box
            self.url = self.url.get()
            
        except AttributeError:

            #Display an Error and Stop Execution
            messagebox.showinfo(title="Url Shortener by Dhruv R", message="The specified credential combination does not exist.")
            exit()

        #Fetch the Shortened URL
        self.shortened_req = requests.post("https://api-ssl.bitly.com/v4/shorten", json={"group_guid": self.get_groupuid(self.uname, self.pwd)[1], "long_url": self.url}, headers={"Authorization": f"Bearer {self.get_groupuid(self.uname, self.pwd)[0]}"})
        self.link = self.shortened_req.json().get("link")

        #Display the Link as a Popup
        messagebox.showinfo(title="Url Shortener by Dhruv R", message=f"{self.link}")
        #-----------------------------

#Display the GUI by running the class
def main():
    root = Tk()
    shortened_url = Url_Shorten(root)
    root.mainloop()

#Set the "Name" Attribute to Main, Not Another Module
if __name__ == "__main__":
    main()
