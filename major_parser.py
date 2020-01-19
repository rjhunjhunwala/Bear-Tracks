from html.parser import HTMLParser
FILENAME = "major_page"
import os


edges = []


class ClassParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self.isInCourseBlock = False
        self.nesting = 0
        pass

    def handle_starttag(self, tag, attrs):
        # if tag == "div":
         #   print(attrs)
        if tag == "div" and (attrs +["aa"])[0][1] == "courseblock":
            self.isInCourseBlock = True
            self.nesting = 0
        elif tag == "div":
            self.nesting += 1


        pass


    def handle_endtag(self, tag):
        if tag == "div":
            if self.nesting == 0:
                self.isInCourseBlock = False
            else:
                self.nesting -= 1
        pass
    def handle_data(self, data):
        if self.isInCourseBlock:
            print(data)
        pass

def process(major_name):
    os.system("curl http://guide.berkeley.edu/undergraduate/degree-programs/{}/#majorrequirementstext >> data/{}".format(major_name, major_name))
    parser = ClassParser()

    text = ""
    with open("data/" + major_name, "r") as f:
        text = f.read()

    parser.feed(text)

def print_cleaned(st):
    def cap_first_letter(st):
        return st[0].upper() + st[1:]
    # print(st + "," + " ".join(map(cap_first_letter, st.split("-"))))
    # print(" ".join(map(cap_first_letter, st.split("-"))))
    print(st)
class MajorParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self.enabled = False
        self.in_list_tag = False
        pass

    def handle_starttag(self, tag, attrs):

        if tag == "a" and self.enabled and self.in_list_tag and dict(attrs)['href'] != "#program-preview":
            ...
            # print(dict(attrs)['href'])
            # print_cleaned(dict(attrs)['href'])
            process(dict(attrs)['href'])
        elif tag == "li":
            self.in_list_tag = "filter_6" in dict(attrs).get('class','').split(" ")


    def handle_endtag(self, tag):
        if tag == "li":
            self.in_list_tag = False
        pass
    def handle_data(self, data):
        if data == "Degree Programs":
            # print("Found it!")
            self.enabled = True

        pass


from datetime import datetime
from pytz import timezone
import pytz

parser = MajorParser()

text = ""
with open(FILENAME, "r") as f:
    text = f.read()

parser.feed(text)

