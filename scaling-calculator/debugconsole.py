import terminal
import curses
import time
from curses import panel

class DebugConsole(object):

    def __init__(self, stdscreen, title):
        self.height = int(terminal.height/2)
        self.width = terminal.width - 2
        self.title = title

        self.window = stdscreen.subwin(self.height-1,self.width,self.height+1,1)
        self.window.border(0)
        self.window.addstr(0,1,title)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()
        # Add the Border
        self.second = time.time()
        self.writebuffer = []

    def display(self):
        self.panel.top()
        self.panel.show()

    def hide(self):
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

    def refresh(self):
        
        self.window.refresh()
        self.window.border(0)
        self.window.addstr(0,1,self.title)
        #draw the last N items
        #foreach i from 0 till (self.height-2) 
        #draw string on i place
        #self.writebuffer[-(self.height-2):]
        
        maxlength = (self.height-3)
        lengthofbuffer = len(self.writebuffer)
        if(lengthofbuffer>maxlength):
            startindex = (lengthofbuffer)-maxlength
        else:
            startindex = 0
            maxlength = lengthofbuffer

        for i in range(0, maxlength):
            logitem = self.writebuffer[i+startindex]
            whitespace = " "*self.width
            self.window.addnstr(i+1,1,logitem+whitespace, self.width-2)

        self.window.refresh()
        curses.doupdate()
        
    def log(self, logitem):

        #1 refresh per second// or 2?
        if(time.time() - self.second >= 0):
            self.writebuffer.append(logitem)
            self.second = time.time()
        else:
            self.writebuffer.append(logitem)

