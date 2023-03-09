from selenium import webdriver
import pandas as pd


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")  # Add this line to run headless

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.goat.com/sneakers")
    return driver


def details():
    driver = get_driver()
    # initialize the number of scraped products and the desired limit
    num_scraped = 0
    limit = 10

    # create a list to store details of all the products
    details_list = []

    # loop until the desired limit is reached or there are no more products to scrape
    while num_scraped < limit:
        # find all the products on the page
        products = driver.find_elements_by_css_selector('[data-qa="grid_cell_product"]')
        for product in products:
            title = product.find_element_by_css_selector('[data-qa="grid_cell_product_name"]').text
            date = product.find_element_by_css_selector('[data-qa="grid_cell_product_release_date"]').text
            price = product.find_element_by_css_selector('[data-qa="grid_cell_product_price"]').text
            result = {
                'Title': title,
                'Release Date': date,
                'Price': price
            }
            details_list.append(result)
            num_scraped += 1
            if num_scraped >= limit:
                break

    driver.quit()
    return details_list


def main():
    details_result = details()
    df = pd.DataFrame(details_result)
    df.to_csv('sneakerslist.csv', index=False)
    print(f'Successfully saved {len(details_result)} records to sneakerslist.csv')


if __name__ == '__main__':
    main()
