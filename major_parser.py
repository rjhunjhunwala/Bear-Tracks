from html.parser import HTMLParser
FILENAME = "major_page"
import csv
import os


edges = []


class ClassParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self.isInCourseBlock = False
        self.nesting = 0
        self.prepped_for_desc = False
        self.desc = False

        self.classes = []
        pass

    def handle_starttag(self, tag, attrs):
        # if tag == "div":
         #   print(attrs)
        if tag == "div" and (attrs +["aa"])[0][1] == "courseblock":
            self.isInCourseBlock = True
            self.nesting = 0
            self.classes.append([])
        elif tag == "div":
            self.nesting += 1
        elif tag == "span" and attrs and "descshow" in attrs[0][1]:
            self.prepped_for_desc = True
            # input(":")

        self.tag = tag
        self.attrs = attrs

        pass
    def clean(self, st):
        ALL = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join(ch if ch in ALL else " " for ch in st)
    def handle_endtag(self, tag):

        if tag == "div":
            if self.nesting == 0:
                self.isInCourseBlock = False
            else:
                self.nesting -= 1
        if self.prepped_for_desc and tag == "br":
            # print("Here!")
            self.desc = True
            self.prepped_for_desc = False
        pass
    def handle_data(self, data):
        if self.isInCourseBlock:
            # print(data)
            if self.tag == "span" and self.attrs and self.attrs[0][1] == "code":
                self.classes[-1].append(self.clean(data))
            if self.desc:
                self.desc = False
                self.classes[-1].append(data[1:])


        pass

def process(major_name):

    os.system("curl http://guide.berkeley.edu/undergraduate/degree-programs/{}/#majorrequirementstext >> data/{}".format(major_name, major_name))

    parser = ClassParser()


    text = ""
    with open("data/" + major_name, "r") as f:
        text = f.read()

    parser.feed(text)
    print(parser.classes)
    with open("data/" + major_name + "_vertices.csv", "w") as vertices:
        fieldnames = ["name", "size", "about"]
        writer = csv.DictWriter(vertices, fieldnames=fieldnames)
        writer.writeheader()
        for bk_class in parser.classes:
            name = bk_class[0]
            about = "" if len(bk_class) == 2 else bk_class[2]
            writer.writerow({"name":name, "size":"1", "about":about})
    with open("data/" + major_name + "_edges.csv", "w") as vertices:
        fieldnames = ["source", "target", "type", "weight"]
        writer = csv.DictWriter(vertices, fieldnames=fieldnames)
        writer.writeheader()
    # print(parser.classes)

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

