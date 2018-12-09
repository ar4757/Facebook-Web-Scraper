# Facebook Web Scraper

Created for a friend who asked how to go about scraping a user's list of friends from Facebook

Uses regular expressions to extract friend names and their usernames. Facebook doesn't display all friends at once, so regular expressions are also needed to fetch the "See More" link to then retrieve the next set of friends. This runs in a loop until there's no more friends left.

Developed for Python 3.7.0
