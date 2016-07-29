from urllib.request import urlopen
from htmlTagExtractor import *
from utilityFunctions import *



class Bot:

    # shared variables among threads
    shared_repository_name = ''
    shared_firstURL = ''
    shared_domain = ''
    shared_waitingToCrawlFile = ''
    shared_crawledFile = ''
    shared_noOfCrawledLinks = ''
    shared_outOfScopeFile = ''
    shared_unique_links_from_queueTextfile = set()
    shared_unique_links_from_crawledTextfile = set()


    def __init__(self, repository_name, firstURL, noOfCrawledLinks, domain, waitingToCrawlFile, crawledFile ,outOfScopeFile):
        Bot.shared_repository_name = repository_name
        Bot.shared_firstURL = firstURL
        Bot.shared_domain = domain
        Bot.shared_waitingToCrawlFile = waitingToCrawlFile
        Bot.shared_crawledFile = crawledFile
        Bot.shared_noOfCrawledLinks = noOfCrawledLinks
        Bot.shared_outOfScopeFile = outOfScopeFile
        self.updateDirFiles()
        self.crawl_page( Bot.shared_firstURL)

    # Creates and Update Repository with links
    @staticmethod
    def updateDirFiles():
        add_repository(Bot.shared_repository_name)
        create_repository_files(Bot.shared_repository_name, Bot.shared_firstURL)
        Bot.shared_unique_links_from_queueTextfile = dump_to_set(Bot.shared_waitingToCrawlFile)
        Bot.shared_unique_links_from_crawledTextfile = dump_to_set(Bot.shared_crawledFile)

    # Update Queue text fie and Crawls text file with links
    @staticmethod
    def update_files():
        dump_to_file(Bot.shared_unique_links_from_queueTextfile, Bot.shared_waitingToCrawlFile)
        dump_to_file(Bot.shared_unique_links_from_crawledTextfile, Bot.shared_crawledFile)

    # Crawled links will be displayed on Screen
    @staticmethod
    def crawl_page( page_url):
        if page_url not in Bot.shared_unique_links_from_crawledTextfile:
            try:
                if len(Bot.shared_unique_links_from_crawledTextfile) <= Bot.shared_noOfCrawledLinks:
                    print(str(len(Bot.shared_unique_links_from_crawledTextfile)) +' link has been crawled ')
                    print('Now crawling  ' + page_url)
                    Bot.add_links_to_queue(Bot.gather_links(page_url))
                    Bot.shared_unique_links_from_queueTextfile.remove(page_url)
                    Bot.shared_unique_links_from_crawledTextfile.add(page_url)
                    Bot.update_files()
            except:
                pass

    # open page url and gather all links in page url
    @staticmethod
    def gather_links(page_url):
        try:
            htmltext = urlopen(page_url).read()
            find_a_tag(htmltext,Bot.shared_firstURL)
        except:
            return set()
        return fetch_url()

    # links  will be added in a set variable to remove duplicate links & outOfscope links will be appended in outOfScopeLinks.txt file
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Bot.shared_unique_links_from_queueTextfile) or (url in Bot.shared_unique_links_from_crawledTextfile):
                continue
            if Bot.shared_domain != find_doamin(url):

                append_file(Bot.shared_outOfScopeFile, Netloc(url))
                continue
            Bot.shared_unique_links_from_queueTextfile.add(url)


