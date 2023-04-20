import requests, re
from bs4 import BeautifulSoup
from gsheet import update_values

WEB_ADDRESS = "https://fitgirl-repacks.site"
COUNT_LINK = "https://fitgirl-repacks-site.disqus.com/count-data.js?1="
SHEET_ID = "15pbjderIVcQKjGO8-iALltf5f-Dz6GKDqGWwxQsb1QE"
TOTAL_PAGES = 357

# r = requests.get(WEB_ADDRESS)

data = [["Sr. No.", "Name", "Date", "Number of Comments", "Link", "Genres/Tags", "Original Size", "Repack Size",
         "Magnet Link", "Image"]]
update_values(range_name=f"Main!A1", value_input_option="USER_ENTERED", _values=data,
              spreadsheet_id=SHEET_ID)
game_count = 1

for x in range(251, TOTAL_PAGES + 1):
    web_address = f'{WEB_ADDRESS}/page/{x}'
    print(f"Reading Page {x} -> {web_address}")
    r = requests.get(web_address)
    soup = BeautifulSoup(r.text, features="html.parser")
    articles = soup.find_all('article')
    for article in articles:
        # Game Name
        game_name = article.h1.text

        # Skip if article is about upcoming repacks
        if game_name == "Upcoming Repacks":
            continue

        # Game Link on FG Website
        game_link = article.h1.find('a')['href']
        # Finding Comment Count
        try:
            comment_elem = article.find('span', attrs={"class": "dsq-postid"})
            link = comment_elem['data-dsqidentifier']
            comments_count_file = requests.get(COUNT_LINK + link).text
            comments_count = re.findall(r'"comments":(\d*)', comments_count_file)[1]
        except TypeError:
            comments_count = 0

        # Finding Game Upload Date
        date = None
        date = article.find('time', attrs={"class": "entry-date"}).text

        # Finding Genre
        genre_text = re.findall(r"Genres/Tags:(.*)\n", article.text)
        genre = "None"
        if len(genre_text) > 0:
            genre = genre_text[0].strip()

        # Finding Original Size
        original_size_text = re.findall(r"Original Size:(.*)\n", article.text)
        try:
            original_size = original_size_text[0].strip()
        except IndexError:
            original_size = "None"

        # Finding Repack Size
        repack_size_text = re.findall(r"Repack Size:(.*)\n", article.text)
        try:
            repack_size = repack_size_text[0].strip()
        except IndexError:
            repack_size = "None"

        # Finding Magnet Link
        magnet_link = "None"
        download_ul = article.ul
        if download_ul is not None:
            try:
                magnet_link = download_ul.li.find_all('a')[1]['href']
            except IndexError:
                continue

        # Finding Image
        image_link = "None"
        image_elem = article.img
        if image_elem is not None:
            image_link = image_elem['src']
            image = f'=IMAGE("{image_link}")'
        else:
            image= "None"

        # Updating Values to Google Sheet
        data = [[game_count, game_name, date, comments_count, game_link, genre, original_size, repack_size, magnet_link,
                 image]]
        update_values(range_name=f"Main!A{game_count + 1}", value_input_option="USER_ENTERED", _values=data,
                      spreadsheet_id=SHEET_ID)
        print(f"Added {game_count} -> {game_name} ")
        game_count += 1
# print(data_array)
