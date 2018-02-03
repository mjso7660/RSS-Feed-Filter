# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Min Joon So
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory


#======================
# Triggers
#======================

class NewsStory:
    def __init__(self, guid, title, description, link, pubdate):
        """initialization"""
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate =pubdate

    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate

class Trigger:
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase=phrase 
        
    def is_phrase_in(self, text):
        for x in string.punctuation:
            text = text.replace(x, " ")
        phrase = self.phrase.lower()
        phrase_list = phrase.split(" ")
        text = text.lower()
        for x in string.punctuation:
            str.replace(text, x, " ")
        text_list = text.split(" ")
        found = False
        
        for x in range(len(text_list)):
            if text_list[x] != phrase_list[0]:
                continue
            temp = x
            for y in range(len(phrase_list)):
#                if temp >= len(text_list):
#                    break
                while temp < len(text_list)-1 and text_list[temp] == "":
                    temp+=1
                if text_list[temp] == phrase_list[y]:
                    temp += 1
                    if y == len(phrase_list)-1:
                        return True
                else:
                    break
        
        return found
    


# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):  
    def evaluate(self, story):
        if self.is_phrase_in(story.get_title()):
            return True
        return False
    
    
# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        if self.is_phrase_in(story.get_description()):
            return True
        return False


# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, pubdate):
        pubdate = datetime.strptime(pubdate, "%d %b %Y %H:%M:%S")
        pubdate = pubdate.replace(tzinfo=pytz.timezone("EST"))
        self.pubdate = pubdate

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        if self.pubdate > story.get_pubdate().replace(tzinfo=pytz.timezone("EST")):
            return True
        return False

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        if self.pubdate < story.get_pubdate().replace(tzinfo=pytz.timezone("EST")):
            return True
        return False

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
        
    def evaluate(self, news):
        return not self.trigger.evaluate(news)
        
# Problem 8
# TODO: AndTrigger

class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
        
    def evaluate(self, news):
        return self.trigger1.evaluate(news) and self.trigger2.evaluate(news)

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
        
    def evaluate(self, news):
        return self.trigger1.evaluate(news) or self.trigger2.evaluate(news)



#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
                break
    return filtered_stories


#======================
# User-Specified Triggers   
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    dict = {}
    trigger_list= []
    for line in lines:
        line_list = line.split(',')
        if line_list[0] == 'ADD':
            
            for x in range(1, len(line_list)):
                trigger_list.append(dict[line_list[x]])
                    
        else:
            if line_list[1] == "TITLE":
                new_trigger = TitleTrigger(line_list[2])
                dict[line_list[0]] = new_trigger
            elif line_list[1] == 'DESCRIPTION':
                dict[line_list[0]] = DescriptionTrigger(line_list[2])
            elif line_list[1] == 'AFTER':
                dict[line_list[0]] = AfterTrigger(line_list[2])
            elif line_list[1] == 'BEFORE':
                dict[line_list[0]] = BeforeTrigger(line_list[2])
            elif line_list[1] == 'NOT':
                dict[line_list[0]] = NotTrigger(dict[line_list[2]])
            elif line_list[1] == 'AND':
                dict[line_list[0]] = AndTrigger(dict[line_list[2]], dict[line_list[3]])
            elif line_list[1] == 'OR':
                dict[line_list[0]] = OrTrigger(dict[line_list[2]], dict[line_list[3]])
            else:
                print('ERROR!')
            
        
        
#    print(lines)
#    print('--------------')
#    print(dict)
#    print('--------------')
    return(trigger_list) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
#        t1 = TitleTrigger("nuclear")
#        t2 = DescriptionTrigger("Trump")
#        t3 = DescriptionTrigger("Obama")
#        t4 = AndTrigger(t2, t3)
#        triggerlist = [t1, t4]
#
        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

