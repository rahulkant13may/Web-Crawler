

from queue import Queue
from bot import Bot
from utilityFunctions import *
from tkinter import *
import threading
from tkinter import Frame,Tk,END,ttk
from tkinter import filedialog

# Tkinter Class and UI(User Interface)
class Tkinter_GUI(Frame,Tk):

    def __init__(self, master):
        Frame.__init__(self, master)

        self.master = master
        self.user_interface()


    # # Buttons and Entry Widgets
    def user_interface(self):

        self.master.title("Web Crawler")
        self.master.configure(background="#1976AB")

        self.firstlabel = ttk.tkinter.Label(self.master, text="Web Crawler",font=("Arial", 32, "bold"), bg = "#1976AB")
        self.firstlabel.grid(row=0)

        self.label = ttk.tkinter.Label(self.master, text="Enter Repository Name",font=("Arial", 15, "bold"),pady=5, bg = "#1976AB")
        self.label.grid(row=2)

        self.e1 = Entry(self.master,font=("Arial", 14, "bold"))
        self.e1.grid(row=3, column=0, columnspan=500)

        self.labe2 = ttk.tkinter.Label(self.master, text="Enter URL",font=("Arial", 15, "bold"),pady=5, bg = "#1976AB" )
        self.labe2.grid(row=4 )

        self.e2 = Entry(self.master,font=("Arial", 15, "bold"))
        self.e2.grid(row=5, column=0, columnspan=500  )

        self.labe3 = ttk.tkinter.Label(self.master, text="Enter No of Links to Crawl",font=("Arial", 15, "bold"),pady=5 , bg = "#1976AB")
        self.labe3.grid(row=6 )

        self.e3 = Entry(self.master,font=("Arial", 15, "bold"))
        self.e3.grid(row=7, column=0, columnspan=500  )


        self.submit = ttk.tkinter.Button(self.master, text='Start Crawling', command=self.connect_userinput,width=15, font=("Arial", 15, "bold"),pady=9,relief=SOLID, bg = "#8cbad5")
        self.submit.grid(row=8, column=0 )

        self.quit = ttk.tkinter.Button(self.master, text='Open Repository', command=self.file_open,width=15, font=("Arial", 15, "bold"),pady=9,relief=SOLID, bg = "#8cbad5")
        self.quit.grid(row=9, column=0 )


    # open repository button will be redirected to this function
    def file_open(self):
        ftypes = [('Text files', '*.txt')]
        dlg = filedialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
        if fl != '':
            text = self.read_file(fl)
            self.txt.insert(END, text)


    # For reading a file
    def read_file(self, filename):
        f = open(filename, "r")
        text = f.read()
        return text


    # Start Crawling Button will redirect to this function
    def connect_userinput(self):
        repository_name = self.e1.get()
        firstURL = self.e2.get()
        noOfCrawledLinks = int(self.e3.get())
        stopWaitingLimitLinks = noOfCrawledLinks * 50
        domain = find_doamin(firstURL)
        waitingToCrawlFile = repository_name + '/waitingToCrawlLinks.txt'
        crawledFile = repository_name + '/crawledLinks.txt'
        outOfScopeFile = repository_name + '/outOfScopeLinks.txt'
        threadsCount = 10
        queue = Queue()
        Bot(repository_name, firstURL,noOfCrawledLinks, domain, waitingToCrawlFile, crawledFile,outOfScopeFile)


        # For crawling links that are stored in queue text file
        def startCrawling():
            queued_links = dump_to_set(waitingToCrawlFile)
            if len(queued_links) > 0 and len(queued_links) < stopWaitingLimitLinks:
                create_jobs()

        # For creation of Threads
        def create_threads():
            for thread in range(threadsCount):
                t = threading.Thread(target=job)
                t.daemon = True
                t.start()


        # Take out link from queue and start crawling
        def job():
            while True:
                url = queue.get()
                Bot.crawl_page( url)
                queue.task_done()


        # Each queued link is a new job
        def create_jobs():
            for link in dump_to_set(waitingToCrawlFile):
                queue.put(link)
            queue.join()
            startCrawling()

        create_threads()
        startCrawling()


def main():

    root = Tk()
    c = Tkinter_GUI(root)

    root.mainloop()


if __name__ == '__main__':
    main()




