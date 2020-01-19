from html.parser import HTMLParser
FILENAME = "major_page"
import csv
import os


edges = []
classes = set()
add_edges = False

def add_split(st):
    builder = []
    for i in range(0, len(st), 60):
        builder.append(st[i: i + 60])
    return "\n".join(builder)

class ClassParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        global edges
        edges = []
        self.isInCourseBlock = False
        self.nesting = 0
        self.prepped_for_desc = False
        self.desc = False
        self.isOpenPre = False
        self.has_seen_prerequisites = False
        self.curr_class = "None 123"
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

        if self.isInCourseBlock and self.tag == "div" and self.attrs and self.attrs[0][1] == "course-section":
            self.isOpenPre = True
            # print("HERE!!!")

        pass
    def clean(self, st):
        ALL = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join(ch if ch in ALL else " " for ch in st)
    def handle_endtag(self, tag):

        if tag == "div":
            if self.nesting == 0:
                self.isInCourseBlock = False
                self.isOpenPre = False
                self.has_seen_prerequisites = False
            else:
                self.nesting -= 1
        if tag == "p" and self.has_seen_prerequisites and self.isOpenPre:
            self.has_seen_prerequisites = False

        if self.prepped_for_desc and tag == "br":
            # print("Here!")
            self.desc = True
            self.prepped_for_desc = False
        pass

    def handle_data(self, data):
        if self.isInCourseBlock:
            # print(data)
            if self.tag == "span" and self.attrs and self.attrs[0][1] == "code":
                if len(self.clean(data))<= 2:
                    return
                self.curr_class = self.clean(data)
                self.classes[-1].append(self.clean(data))
                classes.add(self.curr_class)

            elif self.desc:
                self.desc = False
                self.classes[-1].append(data[1:80] + "...")


            elif self.has_seen_prerequisites and self.isOpenPre and add_edges and self.has_seen_prerequisites:
                 words = data.split(" ")
                 prefix = self.curr_class.split(" ")[0]
                 for word in words:
                     if prefix + " " + word in classes and prefix + " " + word != self.curr_class:
                        edges.append((prefix + " " + word, self.curr_class))
        if "Prerequisites" in data:
            self.has_seen_prerequisites = True

        pass

COLORS = ["Blue", "Red", "Orange", "Yellow", "Green"]

def do_graph_coloring(parser):
    """k-color a graph in linear time by ignoring the definition of coloring, return a mapping from class name to coloring"""
    G = dict()
    V = [c[0] for c in parser.classes if c]
    E = edges
    coloring = dict() # V -> [0, 1, 2, 3]
    for e in E:
        if e[0] in G:
            G[e[0]].append(e[1])
        else:
            G[e[0]] = [e[1]]
        if e[1] in G:
            G[e[1]].append(e[0])
        else:
            G[e[1]] = [e[0]]
    print(G)
    visited = set()

    def explore(v, label):
        visited.add(v)
        coloring[v] = label
        for u in G[v]:
            if u not in visited:
                explore(u, label)
    label = 0
    for v in V:
        if v not in visited:
            if v not in G:
                 coloring[v] = 3
                 edges.append((v, v))
            else:
                explore(v, label)
                label += 1
                label = label % 3
    return coloring



def process(major_name):

    # os.system("curl http://guide.berkeley.edu/undergraduate/degree-programs/{}/#majorrequirementstext >> data2/{}".format(major_name, major_name))

    parser = ClassParser()


    text = ""
    with open("data/" + major_name, "r") as f:
        text = f.read()

    parser.feed(text)

    parser = ClassParser()

    global add_edges
    add_edges = True

    parser.feed(text)

    # print(parser.classes)
    # print(edges)

    color_map = do_graph_coloring(parser)
    print(color_map)
    # print(edges)
    # input(":")
    for color in range(4):
        with open("data2/" + major_name + "_{}_vertices.csv".format(color), "w") as vertices:
            fieldnames = ["name", "size", "about"]
            writer = csv.DictWriter(vertices, fieldnames=fieldnames)
            writer.writeheader()
            for bk_class in parser.classes:
                if not bk_class or color_map[bk_class[0]] != color:
                    continue
                name = bk_class[0]
                about = "" if len(bk_class) == 0 else bk_class[1]
                writer.writerow({"name":name, "size":"1", "about":about})
    for color in range(4):
        with open("data2/" + major_name + "_{}_edges.csv".format(color), "w") as vertices:
            fieldnames = ["source", "target", "type", "weight"]
            writer = csv.DictWriter(vertices, fieldnames=fieldnames)
            writer.writeheader()
            for u,v in edges:
                if color_map[u] == color:
                    writer.writerow({"source":u, "target": v, "type":"directed", "weight": 3})
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
# process("computer-science")
text = ""
with open(FILENAME, "r") as f:
    text = f.read()



parser.feed(text)

