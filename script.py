import camelot
import requests
from datetime import datetime
from facebook_scraper import get_posts
import tempfile
temp_file = tempfile.NamedTemporaryFile(suffix = '.pdf')
today = datetime.today().strftime("%d %B %Y").upper()
for post in get_posts('OfficialPageIGNOU', pages=3):
    text = post.get("text")
    if 'counselling schedule for '+ today  in text:
        link = post.get('link')
        print(temp_file)
        file_id = link[link.find('/d/')+3:link.rfind('/view')]
        r = requests.get('https://drive.google.com/u/0/uc?id=' + file_id + '&export=download')
        temp_file.write(r.content)
        tables = camelot.read_pdf(temp_file.name , pages='all')
        result = 'Today\'s Classes ' + today
        for page in range(0, len(tables)):
            for row_index,row  in tables[page].df.iterrows():
                course = row[4]
                if course == 'MAPC':
                    # print(row)
                    result += '\n---------\n'
                    result +=row[5] + '  -  ' + row[3] + '\n'
                    result += 'Link ' + ' -  ' + row[7].replace(' ', '').replace('\n', '') + '\n'
                    result += 'Region ' + ' - ' + row[1]

# print(result)
temp_file.close()
print(result)