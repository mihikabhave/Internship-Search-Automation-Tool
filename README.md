# Internship-Search-Automation-Tool

## Overview
This project is a Python desktop app that helps automate searching for internships. It creates smart Boolean search queries from user inputs, fetches live results using Google Custom Search API, and saves useful links locally. The app has a friendly interface so users can easily customize searches and manage results.

## Why This Project
I built this tool because searching for internships manually was taking up a lot of time. I saw that the same results were repeated and some of the search results were not relevant to me. My project creates customized search queries and fetches real-time results using Google’s Custom Search API. To keep things flexible, users can add their own keywords through an Excel sheet, so the results cater to their needs. I also added a local database to store only unique links and keep everything organized. While this project is used for finding internships, it can easily be reused for job searching, research, or anything else that needs focused searching. This project helped me use real-world skills like using APIs, making a simple interface, and saving data—while building something useful that others can also benefit from.

## Features
- Builds Boolean search queries from an Excel file.
- Fetches real-time search results via Google Custom Search API.
- Filters out irrelevant websites like Reddit and TikTok.
- Saves unique results in a local SQLite database (results.db).
- Lets users view and export saved URLs as CSV files.
- Provides a simple graphical interface using Tkinter.

## Tools and Technology
- Python 3.7 — coding language used
- Tkinter — for building the desktop GUI
- pandas — for reading and parsing Excel files
- openpyxl — Excel file engine (used by pandas)
- requests — for making API calls
- SQLite — for saving and managing search results
- Google Custom Search API — for search integration

## Prerequisites

### 1. Valid Custom Search JSON API key and Search Engine ID
- This code uses Google Custom Search API to fetch real-time results. To set this up you can refer to the following link: https://developers.google.com/custom-search/v1/overview.
- Note that Custom Search JSON API provides 100 search queries per day for free. If you need more, you may sign up for billing in the API Console. Additional requests cost $5 per 1000 queries, up to 10k queries per day.
- When you run the code, keep track of the number of requests that have been made if you do not want to exceed the daily quota.

### 2. An Excel File for generating query
- Each user should create their own Excel file, as their queries will be specific to their individual needs.
- The following image shows you how the file should be structured. The file should follow the structure shown in the image below, using the same column names. You are free to use any keywords or phrases that suit your purpose when building the query.
<img width="448" height="130" alt="image" src="https://github.com/user-attachments/assets/12edd974-236e-44d6-acef-1a5322783fa6" />

- This will generate a query as follows:

  `" internship summer 2026" ("Computer Science" OR SWE OR "Software Engineer") -"2025 internship" -"2024 internship" -"Fall 2025" -"summer 2024" -"summer 2025"`

- The query must include all required keywords, contain at least one of the alternative keywords, and exclude any results with the restricted keywords. For more information on good Boolean Search Queries, refer to the following link: https://bsharptech.com.au/how-to-use-boolean-search-on-google/.

## Environment Setup
1. Make sure Python 3.7 or higher is installed on your machine. You can download it from https://www.python.org/downloads/.
2. Set up a code editor. I have used VS Code (https://code.visualstudio.com/).
3. Fork and clone the GitHub Repository (https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo).
4. Pip install the required dependencies (pandas, openpyxl, requests). You can use https://packaging.python.org/en/latest/tutorials/installing-packages/ to understand the process.
5. Run the forked script.

## Working Steps
1. Run the python `run_interface.py` script in your code editor.
2. When you run the script a GUI window opens,correctly enter the API Key (described in prerequisites) and click OK.
  <img width="208" height="94" alt="image" src="https://github.com/user-attachments/assets/8e1de78a-4ea1-493c-9a74-0dee03722d8f" />

   - Correctly enter the Search Engine ID and click OK (described in prerequisites).
   
 <img width="208" height="96" alt="image" src="https://github.com/user-attachments/assets/ef8dcce7-c43c-4592-8327-38a2a26b3032" />


   - If either are missing/incorrect, the app exits.
3. If the above details were entered correctly, you will be led to the main GUI interface.

<img width="270" height="200" alt="image" src="https://github.com/user-attachments/assets/c99e4ba3-43ac-4dd2-b8ca-0b7a2e31c692" />

   - Select a valid Excel file (Construction shown in prerequisites).
   - Click on Display Query to generate Boolean Search Query.
  <img width="316" height="79" alt="image" src="https://github.com/user-attachments/assets/028d036c-ddc3-4690-bffe-c394568226b4" />


   - Click 'Query Shuffle' to randomize and regenerate your Boolean query.

<img width="311" height="83" alt="image" src="https://github.com/user-attachments/assets/c2819d61-75ca-4e42-a95c-5489dd2f2196" />

   - Choose how many pages (Google result pages) to search between.
   - Click on Run a search. New results are saved if they do not already exist in the database (stored as results.db in project file).
   - Click on View Saved URLs to view that database which leads you to relevant search results.

<img width="312" height="198" alt="image" src="https://github.com/user-attachments/assets/b61908b6-a792-4384-8099-b875c415a6e3" />

   - Click on Export results as CSV file to save valid URLs in a “results.csv” file in your project folder.

## Viewing/Resetting Database
- After saving necessary results, you can go to `view_database.py`.
- Run script to view and find number of search results.
- To reset database and start with fresh results, uncomment the following line:

  ```python
  # cursor.execute("DROP TABLE IF EXISTS urls")
Note: This action is irreversible so all saved links will be permanently deleted so you can start afresh.
# Debugging and Error Handling

- You can get pop-up error messages for the following reasons:

1. "API Key required."  
Fix: Enter a valid Google API key (don’t leave it blank or cancel).

2. "Search Engine ID required."  
Fix: Enter a valid Custom Search Engine ID (do not skip or cancel).

3. "Please select an Excel file."  
Fix: Use the “Select Excel File” button to choose a proper `.xlsx` or `.xls` file.

4. "Excel file must contain column”  
Fix: Make sure your Excel file has these exact column headers spelled correctly.

5. str(e) during Excel reading or query building  
Fix: Check the error message shown; ensure your Excel file data is clean and that no unexpected data is present.

6. "Empty query."  
Fix: Generate and display a search query before running the search (not empty).

7. str(e) during search/database operations  
Fix: Read the error message and check your API key and database access.

8. "Failed to save CSV”  
Fix: Make sure you have write permission in the project folder and no file lock on `results.csv`.

- You may see these terminal messages/errors while running the search:

1. Value Error: Missing API key or CX ID.  
Fix: Provide a valid API key and Custom Search Engine ID.

2. API Error {status code}: {response.text} (e.g., 403 or 400 errors)  
Fix: Check your API key, query format, and quota limits; ensure the key is active and not exceeded.

3. API Error: {data['error']['message']}  
Fix: Review the specific API error message; correct your query or API setup as needed.

4. No more items returned.  
Fix: This means all available results have been fetched.

5. Reached Google search limit (start > 91). Stopping search.  
Fix: Limit the number of pages to avoid exceeding Google’s start parameter limit (max start=91).

6. Database insert error during saving URLs  
Fix: Duplicate URLs are ignored by design; other database errors are printed to the terminal for debugging.

7. Error parsing JSON response from API  
Fix: Handles invalid JSON responses gracefully.# Internship-Search-Automation-Tool
# Internship-Search-Automation-Tool
