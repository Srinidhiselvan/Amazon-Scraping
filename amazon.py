import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# Define the headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.amazon.in/",
}

# Amazon search URL
url = 'https://www.amazon.in/s?k=shoe+stand+for+home+with+cover&crid=2CPLSLAR6LAJ4&sprefix=shoestand%2Caps%2C292&ref=nb_sb_ss_ts-doa-p_2_9'

# Send a GET request
response = requests.get(url, headers=headers)

# Check the status code
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all products on the page
    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    if not products:
        print("No products found. Check the HTML structure or if you're being blocked.")
        print(soup.prettify())  # Debug the response content if no products are found
    else:
        # Create a list to store product data
        data = []

        for product in products:
            try:
                # Extract product title
                title = product.h2.a.text.strip() if product.h2 else "N/A"

                # Extract the direct product link
                link = product.h2.a['href'] if product.h2 else ""
                direct_link = 'https://www.amazon.in' + link if link.startswith('/') else "N/A"

                # Extract product price
                price = product.find('span', 'a-price-whole')
                price = price.text.strip() if price else "N/A"

                # Extract ratings
                rating = product.find('span', 'a-icon-alt')
                rating = rating.text.strip() if rating else "N/A"

                # Append product data to the list
                data.append({
                    'Title': title,
                    'Direct Link': direct_link,
                    'Price': price,
                    'Rating': rating
                })
            except Exception as e:
                print(f"Error processing product: {e}")

        # Convert data to a pandas DataFrame
        df = pd.DataFrame(data)

        # Save DataFrame to Excel
        df.to_excel('amazon_products_updated.xlsx', index=False)

        print("Data has been saved to amazon_products_updated.xlsx")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Pause to avoid detection (if making subsequent requests)
time.sleep(random.uniform(2, 5))
