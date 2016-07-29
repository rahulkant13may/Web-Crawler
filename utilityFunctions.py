import threading
import os
from urllib.parse import urlparse

#Locks to use shared resources
dumpfileWrite_lock = threading.Lock()
appendfileWrite_lock = threading.Lock()
dumptoSet_lock = threading.Lock()


# For Creating Repository/folder
def add_repository(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


# Create Text files in Repository to store waiting,crawled and out of scope links
def create_repository_files(folderName, firstURL):
    queue = os.path.join(folderName , 'waitingToCrawlLinks.txt')
    crawled = os.path.join(folderName,'crawledLinks.txt')
    outOfScope =  os.path.join(folderName,'outOfScopeLinks.txt')
    if not os.path.isfile(queue):
        append_file(queue, firstURL)
    if not os.path.isfile(crawled):
        append_file(crawled, '')
    if not os.path.isfile(outOfScope):
        append_file(outOfScope, '')


# Append links to text file
def append_file(filepath, data):
    # f = open(os.path.join(root, file), 'a')
    with open(filepath, 'a') as file:
        with appendfileWrite_lock:

            file.write(data + '\n')


# Delete Crawled links waiting text file
def delete_file_contents(filepath):
    open(filepath, 'w').close()


# Transfer links from text file to set to remove duplicates
def dump_to_set(fileName):
    results = set()
    with open(fileName, 'rt') as file:
        for line in file:
            # with dumptoSet_lock:
            results.add(line.replace('\n', ''))
    return results


# Transfer links stored in Set to file
def dump_to_file(links, fileName):
    try:
        with open(fileName,"w") as file:
                for url in links:
                        file.write(url  +  "\n")
    except:
        pass

# Extract domain Name from URL
def find_doamin(url):
    try:
        array = Netloc(url).split('.')
        return array[-2] + '.' + array[-1]
    except:
        return ''


# Extract Sub domain name
def Netloc(url):
    try:
        return urlparse(url).netloc
    except:
        return ''



