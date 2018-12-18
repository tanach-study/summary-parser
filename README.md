# Summary Parser

This script uses BeautifulSoup to parse individual text files from our old Weebly site to obtain the summary text for each chapter and saves them in a CSV.

This works by first requesting the list of sefarim from our API, then looping through and attempting to open HTML files for each one. 

In order to use this, follow these steps:

1. Obtain a site export archive from Weebly, and extract the archive to `./site` in this repo.
2. Check the name mappings in the `book_name_mappings` dictionary.
3. Run with Python 3.

This script also replaces all the Unicode characters in our dataset with ASCII translations, and can be found in the `replacements` dictionary in [parser.py](parser.py).

Note that this code is seriously naive - it is extremely unoptimized, doesn't check much for edge cases, and doesn't do much error handling.
