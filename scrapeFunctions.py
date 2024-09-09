import requests
from bs4 import BeautifulSoup


def get_store(listing):
    """
    Extracts the store name from the given listing.

    Parameters:
    - listing (BeautifulSoup): The BeautifulSoup object representing a deal listing.

    Returns:
    - str: The extracted store name.
    """
    store_element_retailer = listing.select_one('.topictitle_retailer')
    store_element = listing.select_one('.topictitle')

    if store_element_retailer:
        return store_element_retailer.text.strip()
    elif store_element:
        # Extract store from the square brackets, if available
        store_text = store_element.text.strip()
        return store_text.split(']')[0][1:].strip() if ']' in store_text else store_text
    else:
        return "N/A"


def main():
    """
    Main function to scrape and display deal information from the RedFlagDeals forum.

    Parameters: none

    Returns: The 4 latest deals
    """
    url = "https://forums.redflagdeals.com/"
    response = requests.get("https://forums.redflagdeals.com/hot-deals-f9/")
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    # Base URL
    base_url = "https://forums.redflagdeals.com/"

    i = 0
    flag = False
    j = 0
    for listing in soup.find_all("li", class_="row topic"):  ## Loop for counting the number of total deals
        i += 1

    for listing in soup.find_all("li", class_="row topic"):  # Loop to scrape every necessary element per site
        j += 1
        if j == 4:  # Only show the first 3 sites (prevents clutter)
            break
        store = get_store(listing)

        item_element = listing.select_one('.topic_title_link')  # All elements being scraped from the site
        votes_element = listing.select_one('.total_count_selector')
        user_element = listing.select_one('.thread_meta_author')
        timestamp_element = listing.select_one('.first-post-time')
        category_element = listing.select_one('.thread_category a')
        reply_element = listing.select_one('.posts')
        view_element = listing.select_one('.views')

        item = item_element.text.strip() if item_element else "N/A"
        votes = votes_element.text.strip() if votes_element else "N/A"
        username = user_element.text.strip() if user_element else "N/A"
        timestamp = timestamp_element.text.strip() if timestamp_element else "N/A"
        category = category_element.text.strip() if category_element else "N/A"
        reply = reply_element.text.strip() if reply_element else "N/A"
        views = view_element.text.strip() if view_element else "N/A"

        # Extract the URL and prepend the base URL
        url_element = item_element['href'] if item_element else "N/A"
        url = base_url + url_element

        if not flag:  # Only prints for the first iteration
            print(f"Total deals found: {i}\n")
            flag = True

        print(f"   Store: {store}")
        print(f"    Item: {item}")
        print(f"   Votes: {votes}")
        print(f" Username: {username}")
        print(f"Timestamp: {timestamp}")
        print(f" Category: {category}")
        print(f"  Replies: {reply}")
        print(f"    Views: {views}")
        print(f"      Url: {url}")
        print("-------------------------")


def catSorter():
    """
    This function deals with sorting the deals by category

    Parameters: none

    Returns: The number of deals by category
    """
    catDict = {}  # Empty dict for all deals (value) by category (key)

    response = requests.get("https://forums.redflagdeals.com/hot-deals-f9/")
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    for listing in soup.find_all("li", class_="row topic"):

        category_element = listing.select_one('.thread_category a')

        category = category_element.text.strip() if category_element else "N/A"  # Reads the category of the current iteration of the loop, uses that as a key in the dict.

        if category not in catDict:  # If the category is not a key in the dict, it is initialized in the dict along with a value of 1. If it is present in the dict, we add another value of 1
            catDict[category] = 1
        else:
            catDict[category] += 1

    longestString = len(
        max(catDict.keys(), key=len))  # The longest category name (needed to properly format the output of our code)
    print("\nDeals by Category:\n")
    for key, value in catDict.items(): #Prints the contents of our dict
        print(f"{key: >{longestString}}: {value} deals")  # All lines are aligned based on the longest category name
    print("-----------------------------------------------------------------\n")


def topStores(choice):
    """
    This function deals with determining the top stores depending on the user's input on how many they want displayed

    Parameters: the number of top stores we want to see

    Returns: The top stores
    """
    topStoreDict = {}  # Empty dict of the top stores (key) and the number of deals each (value)

    response = requests.get("https://forums.redflagdeals.com/hot-deals-f9/")
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    for listing in soup.find_all("li", class_="row topic"):  # Same principle as in catSorter
        store = get_store(listing)

        if store not in topStoreDict:
            topStoreDict[store] = 1
        else:
            topStoreDict[store] += 1

    res = {key: val for key, val in sorted(topStoreDict.items(), key=lambda ele: ele[1],reverse=True)}  # Sorting algorithm for dicts (since I am working in Python 3.8, dicts are ordered in this version)

    counter = 0

    longestString = len(max(res.keys(), key=len))  # Same as in catSorter
    print("\nTop Stores: \n")
    for key, value in res.items():
        counter += 1
        if counter == int(choice) + 1:  # Breaks the for loop if the counter corresponds to the choice of stores the user wants displayed
            break
        print(f"{key:>{longestString}}: {value} deals")
    print("-----------------------------------------------------------------\n")


def log():
    """
    This function creates a log file of the scraped URLs. Mostly the same principle as the other functions concerning working with dicts to determine the number of urls per category

    Parameters: none

    Returns: a log.txt file containing the latest deals of the chosen category
    """
    response = requests.get("https://forums.redflagdeals.com/hot-deals-f9/")
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    base_url = "https://forums.redflagdeals.com/"  # Call the URL

    urlPerCategory = {} # Empty dict of URLs (values) per category (key)

    for listing in soup.find_all("li", class_="row topic"):
        item_element = listing.select_one('.topic_title_link')
        category_element = listing.select_one('.thread_category a')
        url_element = item_element['href'] if item_element else "N/A"

        category = category_element.text.strip() if category_element else "N/A"
        url = base_url + url_element

        if category not in urlPerCategory:
            urlPerCategory[category] = [url]  # Unlike the previous dicts in our other functions, here we are working with nested lists to be able to have all our URLs per category
        else:
            urlPerCategory[category] += [url]

    counter = 1
    print("\nList of Categories:\n")
    for key, value in urlPerCategory.items():  # Printing the categories found by the web scraper in no particular order
        print(f"{counter}. {key}")
        counter += 1

    choice = int(input("Enter the number corresponding to the category: "))  # Choice of category to write to log file

    newCounter = 0
    f = open("log.txt", "w")  # Creates a .txt file called log
    for key, value in urlPerCategory.items():  # Writing to that file depending on the choice of category
        if newCounter == choice - 1:
            f.write(f"{key}:{value}")
        newCounter += 1
