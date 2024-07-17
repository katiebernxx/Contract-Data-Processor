<h3>BIG DATA: Cleaning and Processing a Dataset of Points of Contact</h3>
<h6>Project Summary</h6>
This python code takes in a CSV file of opportunity contracts, and outputs a new CSV file of unique points of contact and their respective information.
The core of this project is the implementation of a dictionary method for data organization and analysis. This approach allows for the efficient consolidation of contact information, ensuring that each unique point of contact is represented once, and their information is associated directly with them. The output CSV file gives the POC name, email, phone, state, city, and agency. Additionally, I performed further opportunity analysis to report the number and type of opportunities the POCs each work on. This is represented in their opportunity count, associated departments, and specific opportunity titles.

A key feature of my solution is the custom sorting functionality, which offers flexibility in how the final dataset is organized. Users can sort the data alphabetically by name, by city/state, by department, or by the number of associated opportunities, catering to their analytical needs. This enhances the usability and readability of the dataset.

Since the given dataset had extreme variation in the contact name formatting, I have implemented my own data cleaning method for contact names. This method standardizes the format of names and filters out invalid entries to specifically select for real name data. 

See the docstrings and code header for further details of the script.
