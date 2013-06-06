'''
Created on Jun 4, 2013

@author: jason.aeh
'''
import Tkinter as tk
import tkFileDialog
import ttk 
import os
import sys
import win32security
import win32api
import ntsecuritycon as ntcon

class main_window(tk.Frame):
    '''
    Class to generate main window using Tkinter 8.5 and execute permission changes to all files under target directory
    '''
    #
    #Find SIDs for user groups Admin, User, and Everyone
    #
    
    def __init__(self, master=None):
        '''
        Constructor
        '''
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        # defining options for opening a directory
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = True
        options['title'] = 'Choose a target directory'
       
    def show_cacls (self, filename):
        print
        print
        for line in os.popen ("cacls %s" % filename).read ().splitlines ():
            print line
    def create_widgets(self):
        '''
        Method to create the various buttons and other items needed for the GUI
        '''
        self.quit_button = tk.Button(self, text = 'Quit', command = self.quit)
        self.quit_button.grid(row = 0 , column = 1)
        self.browse_button = tk.Button(self, text = 'Browse', command = self.traverse)
        self.browse_button.grid(row = 0, column = 2 )
        
    def get_file_attr(self, filename):
        '''
        Method to find current file attributes of files in target 
        directory and change file permissions
        '''
        if os.path.isfile(filename):#loop for files
            try:
                fn=os.path.normpath(filename)
                print fn
                everyone, domain, type = win32security.LookupAccountName ("", "Everyone")
                admins, domain, type = win32security.LookupAccountName ("", "Administrators")
                user, domain, type = win32security.LookupAccountName ("", win32api.GetUserName ())
                open(fn, "w").close()
                main_window.show_cacls(self, fn)
                #
                #Find the DACL
                #
                sec_des = win32security.GetFileSecurity (fn, win32security.DACL_SECURITY_INFORMATION)
                dacl = win32security.ACL()
                dacl.AddAccessAllowedAce(win32security.ACL_REVISION, ntcon.FILE_ALL_ACCESS,everyone)
                dacl.AddAccessAllowedAce(win32security.ACL_REVISION, ntcon.FILE_ALL_ACCESS, user)
                dacl.AddAccessAllowedAce(win32security.ACL_REVISION, ntcon.FILE_ALL_ACCESS,admins)
                #
                #Set ACLs
                #
                sec_des.SetSecurityDescriptorDacl (1, dacl, 0)
                win32security.SetFileSecurity (fn, win32security.DACL_SECURITY_INFORMATION, sec_des)
                self.show_cacls (fn)
                                
            except IOError:
                print 'Error'
                sys.exit()
        else:# loop for directories
            try:
                fn=os.path.normpath(filename)
                current_username = win32api.GetUserName()
                os.system("icacls " + fn + " /grant :r Everyone:(OI)(CI)F")
                os.system("icacls " + fn + " /grant :r "+current_username+":(OI)(CI)F")
                os.system("icacls " + fn + " /grant :r Users:(OI)(CI)F")
                                               
            except IOError:
                print 'Error'
                sys.exit()
    def traverse(self):
        '''
        Method generates file/directory dialog and traverses directory and sub-folders passing filenames
        to 
        '''
        self.dir_name = tkFileDialog.askdirectory(**self.dir_opt)
        print self.dir_name
        target_dir = self.dir_name
        for root, subFolders, files in os.walk(target_dir):
            
            for sf in subFolders:
                filename=(os.path.join(root,sf))
                self.get_file_attr(filename)
            for in_file in files:
                filename=(os.path.join(root,in_file))
                self.get_file_attr(filename)
                   
        
app = main_window()
app.master.title('WinCHMod')
app.mainloop()