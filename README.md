# wikipedia_web_scraping

Webscrapes user inputted Wikipedia articles, returns content, and saves content to a database for faster future retrieval.


Locally hosted website to take in user input (in this case Wikipedia URLs) and send the request to a server whereby content from the Wiki page was returned.

Front End: HTML, CSS, and JavaScript.

Back End: Python (includes database reading and writing component with built-in SQLite).

Server operations included some URL validation, checking for already existing content in a database (searched by Wiki page name), website web scraping and formatting via BeautifulSoup, saving content to a database, and returning the content to be displayed to the user on the webpage.


## Expanding the project:

Plan to expand this project by incorporating the ChatGPT API (or possibly any other AI API available) to send Wikipedia links after some validation and display a returned summarization of the content to users.

Baked into the project was an option to return internal Wiki link summaries which referred to returning summaries of internal Wikipedia links of the queried page. These are planned to be displayed a expandable drop-down menus where they are collapsed by default when returned.

Had thoughts of again utilizing the ChatGPT API to give points to the internal Wiki links from 1-10 regarding their relevance to the queried Wiki page. These would then determine, based on a certain threshold (e.g. >5), internal pages would be summarized by ChatGPT to be returned and displayed to the user.

These related Wikis could be stored in the database with indications of their relevance to other Wiki pages.


## Included Folders:

#### Static

Includes HTML and CSS files for displaying the website and minamally stylizing it. Used built in VS Code Live Server extension to run the website live on a local machine.

#### Dynamic

Includes JavaScript code which listens to events, passes user input to server, and returns the server response to the website to be displayed.

#### Server

Includes Python server and database which takes the client request, breaks it up, validates it, checks the page against the database, and web scrapes the Wikipedia page for content if it is not found in the database. The content is then saved to the database along with the wiki link and wiki page name for later quicker retrieval and the web scraped content is returned to the client.

#### settings.json

The Live Server VS Code extension caused issues where its live reloading feature would cause the client page to reload following every initial request to the server when web scraped wikipedia page content was saved to the database. It would then display and not reload on a subsequent request of the same Wikipedia page. To prevent this feature, code was included in this file to ignore the extension's live reloading feature. 
