import scrapeFunctions
"""
This is the main menu logic
"""
def main():
    while True:
        print("***** Web Scraping Adventure *****\n"
              "1. Display Latest Deals\n"
              "2. Analyze Deals by Category\n"
              "3. Find top Stores\n"
              "4. Log Deal Information\n"
              "5. Exit")
        choice = input("Enter your choice (1-5): ") # We use if/else because there are no switch statements in Python
        if choice == "1":
            scrapeFunctions.main()
        elif choice == "2":
            scrapeFunctions.catSorter()
        elif choice == "3":
            sizeChoice = input("Enter the number of top stories to display: ")
            scrapeFunctions.topStores(sizeChoice)
        elif choice == "4":
            scrapeFunctions.log()
        elif choice == "5":
            exit(1)

if __name__ == "__main__":
    main()