from bs4 import BeautifulSoup
import requests
import csv
import re
import os
  
# get a list of all sefarim 
URL = "https://api.tanachstudy.com/sefarim"
  
# make the get request
r = requests.get(url = URL) 

# convert response to json
data = r.json() 

# compile the regex string to remove newlines
# pattern = re.compile('(?<!\n)\n(?!\n)|\n{3,}')
pattern = re.compile('\n{1,}')

# get a csv output file
with open("summaries.csv", mode="w", encoding="utf-8") as out_file:
    # get a writer for the file
    out_writer = csv.writer(out_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # write a header row
    out_writer.writerow(["Sefer", "Perek", "Summary"])

    # loop through all our books, writing to the file
    for book in data:
        if book["seferMeta"]["part_id"] != 5:
            # get the name of the current sefer
            sefer = book["seferMeta"]["book_name_pretty_eng"]
            match = re.match(r'(\w+)(\d+)', sefer)
            if match:
                sefer = str.join('-', match.groups());
            # loop through all the perakim in the sefer
            for perek in book["allPerakim"]:
                if perek["perek_id"] == 0:
                    perek_num = "intro"
                else:
                    perek_num = str(perek["perek_id"])

                file_name = "./site/" + sefer.lower() + "-" + perek_num + ".html"
                print("attempting to open", file_name)
                if os.path.isfile(file_name.encode('ascii')):
                    with open(file_name.encode('ascii'), mode='r') as perek_file:
                        soup = BeautifulSoup(perek_file, 'html.parser')
                        summaries = soup.find_all(class_="perek-summary")
                        final = ""
                        for summary in summaries:
                            print(summary)
                            str_summary = str(summary)
                            clean = re.sub(pattern, ' ', str_summary)
                            new_soup = BeautifulSoup(clean, 'html.parser', from_encoding='utf-8')
                            temp = new_soup.text
                            if len(temp) > len(final):
                                final = temp
                            # print(new_soup.original_encoding)
                            print()
                        print()
                        print()
                        out_writer.writerow([sefer, perek_num, final])
