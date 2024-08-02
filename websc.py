import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Function to initialize the Selenium WebDriver
def init_driver():
    # Set the path to your Geckodriver
    service = FirefoxService(executable_path='C:\\Users\\Perfect\\MLT\\geckodriver.exe')
    driver = webdriver.Firefox(service=service)
    return driver

# Function to scrape product data from Amazon
def scrape_amazon_product(url):
    driver = init_driver()
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Extract the product title
    try:
        title = soup.find('span', {'id': 'productTitle'}).get_text(strip=True)
    except AttributeError:
        title = 'N/A'

    # Extract the product price
    try:
        price = soup.find('span', {'class': 'a-price-whole'}).get_text(strip=True)
    except AttributeError:
        price = 'N/A'

    # Extract the product description
    try:
        description = soup.find('div', {'id': 'feature-bullets'}).get_text(strip=True)
    except AttributeError:
        description = 'N/A'

    # Extract the product reviews
    try:
        reviews = soup.find('span', {'id': 'acrCustomerReviewText'}).get_text(strip=True)
    except AttributeError:
        reviews = 'N/A'

    return {
        'Title': title,
        'Price': price,
        'Description': description,
        'Reviews': reviews
    }

# Function to scrape data for multiple URLs
def scrape_multiple_urls(urls):
    data = []
    for url in urls:
        product_data = scrape_amazon_product(url)
        data.append(product_data)
    return data

# Function to browse and select a file
def browse_file():
    filename = filedialog.askopenfilename(
        title="Select file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    if filename:
        file_path.set(filename)

# Function to load URLs from a file
def load_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls

# Function to start scraping process
def start_scraping():
    urls = []
    if url_entry.get():
        urls.append(url_entry.get().strip())
    elif file_path.get():
        urls = load_urls_from_file(file_path.get())
    else:
        messagebox.showerror("Error", "Please enter a URL or select a file.")
        return

    if not urls:
        messagebox.showerror("Error", "No URLs provided.")
        return

    try:
        scraped_data = scrape_multiple_urls(urls)
        df = pd.DataFrame(scraped_data)
        output_file = 'amazon_product_data.csv'
        df.to_csv(output_file, index=False)
        messagebox.showinfo("Success", f"Data saved to {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the GUI application
app = tk.Tk()
app.title("Amazon Product Scraper")

# URL entry field
tk.Label(app, text="Enter Amazon Product URL:").pack(pady=5)
url_entry = tk.Entry(app, width=50)
url_entry.pack(pady=5)

# File selection
file_path = tk.StringVar()
tk.Button(app, text="Select File with URLs", command=browse_file).pack(pady=5)
tk.Entry(app, textvariable=file_path, width=50).pack(pady=5)

# Start scraping button
tk.Button(app, text="Start Scraping", command=start_scraping).pack(pady=20)

# Run the GUI event loop
app.mainloop()
