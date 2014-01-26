import terminal
import curses
import time
from curses import panel

class InfoContainer(object):

    def __init__(self, stdscreen, title, debug_console, threadcount):
        self.debug_console = debug_console
        self.threadcount = threadcount
        self.runningthreads = threadcount

        self.title = title

        self.index = []
        self.totalsums = []
        
        self.height = int(terminal.height/2)
        self.width = terminal.width - 2
        
        self.window = stdscreen.subwin(self.height,self.width,1,1)
        self.window.border(0)
        self.window.addstr(0,1,title)
        self.padding = 1 #padding between drawed items
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()
        # Add the Border

        for i in range(0, self.threadcount):
            self.index.append(0)
            self.totalsums.append(0)

        #for the running time
        self.i = 7
        self.start_time = time.time()

        self.debug_console.log("Init of InfoContainer complete")

    def display(self):
        self.panel.top()
        self.panel.show()
        #self.window.clear()

    def hide(self):
        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

    def refresh(self):
        self.window.border(0)
        self.window.addstr(0,1,self.title)
        
        self.window.addstr(1,1,"Number of threads: "+str(self.threadcount))

        linecount = 2+self.padding
        for i in range(0, self.threadcount):
            index = str(self.index[i])
            totalsum = str(self.totalsums[i])

            ##procent balk
            if(self.index[i]>0):
                workdoneindicator = int(self.index[i] / self.totalsums[i] * 20)
            else: 
                workdoneindicator = 0
            worktodoindicator = 20-workdoneindicator
            indicatorstring = "["+(">"*workdoneindicator)+('.'*worktodoindicator)+"]"
            ##

            self.window.addstr(linecount,1,"Thread("+str(i+1)+") :: "+indicatorstring+": "+index+"/"+totalsum+" calculations")
            linecount += 1
        linecount += self.padding
        
        self.window.addstr(linecount, 1, "Running for : "+str(int(time.time() - self.start_time))+" seconds")
        linecount += 1+self.padding

        if(self.runningthreads == 0):
            self.window.addstr(linecount, 1, "Task done in "+str(self.taskdonetimer)+" seconds")

        self.window.refresh()
        curses.doupdate()

    def updateIndex(self, thread_n):
        self.index[thread_n] += 1

    def initTotalSums(self, i,thread_n):
        self.totalsums[thread_n] = i

    def taskDone(self):
        self.runningthreads -= 1
        if(self.runningthreads == 0):
            self.taskdonetimer = int(time.time() - self.start_time)

    def add(self, message):
        self.window.addstr(self.i,1,message)
        self.refresh()
        self.i += 1