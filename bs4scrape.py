import requests
from bs4 import BeautifulSoup
import pandas as pd

# The URL of the search results page on Airbnb
url = "https://www.airbnb.com/s/Honolulu--HI--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&query=Honolulu%2C%20HI&place_id=ChIJTUbDjDsYAHwRbJen81_1KEs&date_picker_type=calendar&checkin=2023-03-03&checkout=2023-03-06&source=structured_search_input_header&search_type=autocomplete_click"

# Send a GET request to the URL and parse the page content with BeautifulSoup
page = requests.get(url)
soup = BeautifulSoup(page.text, "lxml")

# Create an empty DataFrame to store the scraped data
df = pd.DataFrame({'Title': [], 'Details': [], 'Price': [], 'Rating': [], 'Links': []})

# Loop through each page of search results
while True:
    # Find all the posting div elements on the page
    postings = soup.find_all('div', class_='c4mnd7m dir dir-ltr')
    print(f"Scraping {len(postings)} posts...")

    # Loop through each posting and extract the relevant information
    for post in postings:
        try:
            # Extract the link to the posting, and create a full URL by appending the base Airbnb URL
            link = post.find('a', class_='l1j9v1wn bn2bl2p dir dir-ltr').get('href')
            link_full = 'https://www.airbnb.com/' + link

            # Extract the title, price, rating, and other details of the posting
            title = post.find('span', class_='t6mzqp7 dir dir-ltr').text
            preprice = post.find('span', class_='a8jt5op dir dir-ltr').text
            price = preprice.replace(' per night', '').replace('originally', '')
            rating = post.find('span', class_='t5eq1io r4a59j5 dir dir-ltr').get('aria-label')
            details = post.find('span', class_='dir dir-ltr').text

            # Add the extracted data to the DataFrame
            df = pd.concat([df, pd.DataFrame(
                {'Title': [title], 'Details': [details], 'Price': [price], 'Rating': [rating], 'Links': [link_full]})])

        # Print an error message if there is an issue extracting data from a posting
        except Exception as e:
            print(f"Error processing post: {e}")

    # Check if there is a "Next" button on the page; if not, exit the loop
    next_page = soup.find('a', {'aria-label': 'Next'})
    if not next_page:
        break

    # Create the URL for the next page of search results and send a GET request
    next_page_full = 'https://www.airbnb.com/' + next_page.get('href')
    url = next_page_full
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")

# Print the total number of posts scraped, and save the data to a CSV file
print(f"Scraped {len(df)} posts.")
df.to_csv('airbnb_Data_listing.csv', index=False)