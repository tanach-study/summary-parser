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

non_ascii_characters = []

replacements = {
    8211: '-',
    8216: '\'',
    8217: '\'',
    8220: '"',
    8221: '"',
    8226: '-',
    8230: '...',
    8232: ' ',
}

book_name_mappings = {
    'yehoshua': 'yehoshua',
    'shofetim': 'shofetim',
    'shemuel1': 'shemuel1',
    'shemuel2': 'shemuel2',
    'melachim1': 'melachim1',
    'melachim2': 'melachim2',
    'yeshayahu': 'yeshayahu',
    'yirmiyahu': 'yirmiyahu',
    'yehezkel': 'yehezkel',
    'hoshea': 'hoshea',
    'yoel': 'yoel',
    'amos': 'amos',
    'ovadia': 'ovadiah',
    'yonah': 'yonah',
    'michah': 'michah',
    'nahum': 'nahum',
    'habakuk': 'habakuk',
    'sephania': 'sefaniah',
    'hagai': 'hagai',
    'zecharia': 'zecharia',
    'malachi': 'malachi',
    'divre-hayamim-1': 'divre-hayamim-1',
    'divre-hayamim-2': 'divre-hayamim-2',
    'tehillim': 'tehillim',
    'mishle': 'mishle',
    'iyov': 'iyov',
    'shir-hashirim': 'shir-hashirim',
    'ruth': 'ruth',
    'eichah': 'eichah',
    'kohelet': 'kohelet',
    'esther': 'esther',
    'daniel': 'daniel',
    'ezra': 'ezra',
    'nehemya': 'nehemya',
}

# get a csv output file
with open("summaries.csv", mode="w", encoding="ascii") as out_file:
    # get a writer for the file
    out_writer = csv.writer(out_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # write a header row
    out_writer.writerow(["Sefer", "Perek", "Summary"])

    # loop through all our books, writing to the file
    for book in data:
        if book["seferMeta"]["part_id"] != 5:
            # get the name of the current sefer
            sefer = book["seferMeta"]["book_name"]
            sefer = book_name_mappings[sefer]
            # loop through all the perakim in the sefer
            for perek in book["allPerakim"]:
                if perek["perek_id"] == 0:
                    perek_num = "intro"
                else:
                    perek_num = str(perek["perek_id"])

                file_name = "./site/" + sefer + "-" + perek_num + ".html"
                # print("attempting to open", file_name)
                if os.path.isfile(file_name.encode('ascii')):
                    with open(file_name.encode('ascii'), mode='r') as perek_file:
                        soup = BeautifulSoup(perek_file, 'html.parser')
                        summaries = soup.find_all(class_="perek-summary")
                        final = ""
                        for summary in summaries:
                            # print(summary)
                            str_summary = str(summary)
                            # str_summary.replace(chr(8211), '-')
                            # str_summary.replace(chr(8216), '\'')
                            # str_summary.replace(chr(8217), '\'')
                            # str_summary.replace(chr(8220), '"')
                            # str_summary.replace(chr(8221), '"')
                            # str_summary.replace(chr(8226), '-')
                            # str_summary.replace(chr(8232), '\n')
                            # str_summary.replace(u"\u2013", '-')
                            # str_summary.replace(u"\u2018", '\'')
                            # str_summary.replace(u"\u2019", '\'')
                            # str_summary.replace(u"\u201C", '"')
                            # str_summary.replace(u"\u201D", '"')
                            # str_summary.replace(u"\u2022", '-')
                            # str_summary.replace(u"\u2028", '\n')
                            clean = re.sub(pattern, ' ', str_summary)
                            new_soup = BeautifulSoup(clean, 'html.parser')
                            temp = new_soup.text
                            temp_list = list(temp)
                            for i, c in enumerate(temp_list):
                                if ord(c) > 127:
                                    # print(c)
                                    non_ascii_characters.append(c)
                                    temp_list[i] = replacements[ord(c)]
                            temp = "".join(temp_list)
                            if len(temp) > len(final):
                                final = temp
                            # print(new_soup.original_encoding)
                        #     print()
                        # print()
                        # print()
                        final.encode('ascii')
                        out_writer.writerow([sefer, perek_num, final])
                else:
                    print(file_name, "DNE")

with open("non_ascii.txt", mode="w", encoding="utf-8") as out_file:
    non_ascii_character_set = set(non_ascii_characters)
    print(non_ascii_character_set)
    for c in non_ascii_character_set:
        out_file.write("%s : %d\n" % (c, ord(c)))
    out_file.close()
