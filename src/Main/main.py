'''
Created on Jun 4, 2013

@author: jason.aeh
'''
import Tkinter as tk
import tkFileDialog
import ttk
import os
import getpass

class main_window( ttk.Frame ):
    '''
    Class to generate main window using Tkinter 8.5
    Class to execute permissions changes on target directory
    '''

    #   defining options for opening a directory
    def __init__( self, master = None ):
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = True
        options['title'] = 'Choose a target directory'
        #   Create Frame
        ttk.Frame.__init__( self, master )
        self.grid()
        self.create_widgets()


    def get_dir_rights( self ):

        if self.rights.get() == 'read':
            self.pass_to_dir = '(R)'
            return self.pass_to_dir
        if self.rights.get() == 'write':
            self.pass_to_dir = '(W)'
            return self.pass_to_dir
        if self.rights.get() == 'readwrite':
            self.pass_to_dir = '(R,W)'
            return self.pass_to_dir
        if self.rights.get() == 'full':
            self.pass_to_dir = '(F)'
            return self.pass_to_dir
        return self.pass_to_dir

    def fill_path( self, dn ):
        pe = self.path_entry.get()
        self.path_entry.delete( 0, len( pe ) )
        self.path_entry.insert( 0, dn )
    def traverse( self ):
        if self.oi.get():
            obinher = '(OI)'
        else:
            obinher = ''
        if self.ci.get():
            coinher = '(CI)'
        else:
            coinher = ''
        dir_rights = self.get_dir_rights()
        fn = os.path.normpath( self.dir_name )
        gr = r" /grant:r "
        inher = r"/inheritance:e "
        current_user = getpass.getuser()
        if self.cb1.get() == 1:    #   Everyone
            cmd = "icacls %(fn)s %(inher)s %(gr)sEveryone:%(obinher)s%(coinher)s%(dir_rights)s /T /C" % locals()
            os.system( cmd )
        if self.cb4.get() == 1:    #   All users
            cmd = "icacls %(fn)s %(inher)s %(gr)sUsers:%(obinher)s%(coinher)s%(dir_rights)s /T /C" % locals()
            os.system( cmd )
        if self.cb3.get() == 1:    #   current user
            cmd = "icacls %(fn)s %(inher)s %(gr)s%(current_user)s:%(obinher)s%(coinher)s%(dir_rights)s /T /C" % locals()
            os.system( cmd )
        if self.cb2.get() == 1:    #   Administrators
            "icacls %(fn)s %(inher)s %(gr)sAdministrators:%(obinher)s%(coinher)s%(dir_rights)s /T /C" % locals()
            os.system( cmd )

        '''
        Method generates file/directory dialog and traverses directory and sub-folders passing filenames
        to
        '''

    def file_browse( self ):
        self.dir_name = tkFileDialog.askdirectory( initialdir = "/", title = 'Choose a target directory' )
        pe_name = str( os.path.normpath( self.dir_name ) )
#           print pe_name
        self.fill_path( str( pe_name ) )


    def create_widgets( self ):
        '''
        Method to create the various buttons and other items needed for the GUI
        '''

        self.path_from_browse = tk.StringVar()
        self.title = ttk.Label( self, text = 'Please Select a Target Directory:' )
        self.title.grid( row = 1, columnspan = 2 )
        self.path_display_label = ttk.Label( self, text = 'Path: ' )
        self.path_display_label.grid( row = 2, column = 0 )
        self.quit_button = ttk.Button( self, text = 'Quit', command = self.quit )
        self.quit_button.grid( row = 5, column = 4 )
        self.go_button = ttk.Button( self, text = 'Go!' , command = self.traverse )
        self.go_button.grid( row = 5, column = 3 )
        self.browse_button = ttk.Button( self, text = 'Browse', command = self.file_browse )
        self.browse_button.grid( row = 2, column = 2 )
        self.path_entry = tk.Entry( self, textvariable = self.path_from_browse )
        self.path_entry.grid( row = 2, column = 1 )
        self.cb1 = tk.IntVar()
        self.cb2 = tk.IntVar()
        self.cb3 = tk.IntVar()
        self.cb4 = tk.IntVar()
        self.checkbox_everyone = tk.Checkbutton( self, text = 'Everyone', variable = self.cb1 )
        self.checkbox_everyone.grid( row = 3 , column = 0 )
        self.checkbox_everyone.deselect()
        self.checkbox_admins = tk.Checkbutton( self, text = 'Admins', variable = self.cb2 )
        self.checkbox_admins.grid( row = 3 , column = 1 )
        self.checkbox_admins.deselect()
        self.checkbox_current_user = tk.Checkbutton( self, text = 'Current User', variable = self.cb3 )
        self.checkbox_current_user.grid( row = 3 , column = 2 )
        self.checkbox_current_user.deselect()
        self.checkbox_all_users = tk.Checkbutton( self, text = 'All Users', variable = self.cb4 )
        self.checkbox_all_users.grid( row = 3 , column = 3 )
        self.checkbox_all_users.deselect()
        self.rights = tk.StringVar()
        self.radio_read = ttk.Radiobutton( self, text = 'Read', variable = self.rights, value = 'read' )
        self.radio_write = ttk.Radiobutton( self, text = 'Write', variable = self.rights, value = 'write' )
        self.radio_read_write = ttk.Radiobutton( self, text = 'Read & Write', variable = self.rights, value = 'readwrite' )
        self.radio_full_control = ttk.Radiobutton( self, text = 'Full Control', variable = self.rights, value = 'full' )
        self.radio_read.grid( row = 4, column = 0 )
        self.radio_write.grid( row = 4, column = 1 )
        self.radio_read_write.grid( row = 4, column = 2 )
        self.radio_full_control.grid( row = 4, column = 3 )
        self.oi = tk.StringVar()
        self.ci = tk.StringVar()
        self.checkbox_oi = tk.Checkbutton( self, text = 'Object Inheritance?', variable = self.oi )
        self.checkbox_ci = tk.Checkbutton( self, text = 'Container Inheritance?', variable = self.ci )
        self.checkbox_oi.grid( row = 5, column = 0 )
        self.checkbox_ci.grid( row = 5, column = 1 )

app = main_window()
app.master.title( 'WinCHMod' )
app.mainloop()

