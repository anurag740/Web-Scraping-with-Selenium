# Web-Scraping-with-Selenium

Objective
To extract structured data from Genesys Cloud customer case studies and build a dataset with the following columns:
1.
Company Name
2.
Industry / Vertical
3.
Person Quoted
4.
Role / Designation
5.
Region
6.
Country
Tools and Libraries Used
•
Python: Programming language used for the script.
•
Selenium: For automating browser interaction and handling dynamic content.
•
Pandas: For data structuring and saving the extracted data into a CSV file.
•
Chromedriver: WebDriver for automating Google Chrome.
Approach
1.
Scraping Case Study Links:
o
Accessed the Genesys Customer Stories page.
o
Identified links to individual case studies using Selenium and XPath.
2.
Extracting Data:
o
Navigated to each case study link and extracted the following details:
▪
Company Name: Found in an anchor tag following the label "Customer:".
▪
Industry / Vertical: Found as text following the label "Industry:".
▪
Person Quoted & Role: Extracted from the paragraph containing the quote and designation.
▪
Region and Country: Extracted from the text following the label "Location:", with the country parsed separately.
3.
Data Handling:
o
Ensured missing values were handled gracefully by setting "N/A" where data was unavailable.
o
Added exception handling to log any errors during extraction without interrupting the process.
4.
Output:
o
Saved the structured dataset to a CSV file named genesys_case_studies.csv.
