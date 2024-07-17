'''
BIG DATA: Cleaning and Processing a Dataset of Points of Contact
Katie Bernard
12/21/2023

Takes in a CSV file of opportunity contracts, and outputs a new CSV file of unique
points of contact and their respective information. The method of organization can
be specified as alphabetically by name, by city/state, by department, or by number
of associated opportunities.

'''
import pandas as pd
import csv
import re

# Global Constants / User-specified Parameters
FILE_PATH = 'POC_LIST.csv'  # CSV file path
OUTPUT_CSV_PATH = 'processed_contacts.csv' # Name/path of output CSV
SORTING_PARAMETER = 'name'  # What to sort by: 'name', 'city', 'department', or 'opportunity'

# Initialize a dictionary to store the unique points of contact
contact_dict = {}

# Function Definitions
def add_to_dict(contact_name, contact_info, opportunity_info):
    """
    Adds or updates a contact in the contact dictionary.
    
    Parameters:
    contact_name (str): The name of the contact.
    contact_info (list): List containing contact's email, phone number, state, city, and agency.
    opportunity_info (list): List containing opportunity-related information: associated departments and opportunity titles.
    
    Returns:
    None: Modifies the contact_dict in place.
    """
    if contact_name and not pd.isna(contact_name):
        formatted_name = contact_name.title()  # Format the name
        if formatted_name not in contact_dict:
            contact_dict[formatted_name] = contact_info + [1] + [set([opportunity_info[0]])] + [set([opportunity_info[1]])]
        else:
            # Update the existing entry
            existing_info = contact_dict[formatted_name]
            existing_info[5] += 1  # Increment the opportunity count
            existing_info[6].add(opportunity_info[0])  # Add new department
            existing_info[7].add(opportunity_info[1])  # Add new contract type
            
def clean_name(name):
    """
    Cleans and standardizes the contact name by removing unwanted characters, formatting,
    and correcting common errors. Names deemed not valid (e.g., containing more than 4 words
    or being a telephone entry) are marked as "N/A".
    
    Parameters:
    name (str): The raw name string to be cleaned.
    
    Returns:
    str: The cleaned and standardized name, or "N/A" if the name is not valid.
    """
    #If the entry for name is >4 words, it is not a name and is likely just a message
    if len(name.split()) > 4:
        return "N/A"
    if re.match(r'^\s*Telephone:', name):
        # Extract phone number and place it in the phone number column
        phone_number = re.findall(r'\d+', name)[0]
        new_df.loc[new_df['name'] == name, 'phone number'] = phone_number
        return "N/A"
    clean = re.sub(r'[\"\']', '', name)  # Remove quotes
    clean = re.sub(r'^\d+\s*', '', clean)  # Remove leading numbers
    clean = re.sub(r'A1C', '', clean)  # Remove common prefix
    clean = re.sub(r'\s+', ' ', clean).title().strip()  # Standardize format
    return clean

def custom_sort_key(name):
    """
    Custom sorting key function for names with prefixes like Dr. or unusual formats.
    
    Parameters:
    name (str): The name to generate a sorting key for.
    
    Returns:
    str: A sorting key derived from the given name.
    """
    if name == "N/A":
        return "zzz"  # This ensures N/A values are sorted at the end
    name = re.sub(r'^\([^)]*\)\s*', '', name)  # Remove parentheses content
    name = re.sub(r'^(Dr\.|Lt\.)\s*', '', name)  # Remove prefixes like Dr. or Lt.
    return name

def sort_dataframe(df, sort_by):
    """
    Sorts the given DataFrame according to the specified method.
    
    Parameters:
    df (DataFrame): The DataFrame to sort.
    sort_by (str): The sorting criteria ('name', 'city', 'department', 'opportunity').
    
    Returns:
    DataFrame: The sorted DataFrame.
    """
    if sort_by == 'name':
        return df.sort_values(by='name', key=lambda x: x.map(custom_sort_key))
    elif sort_by == 'city':
        return df.sort_values(by=['city', 'state'])
    elif sort_by == 'department':
        return df.sort_values(by='associated_departments')
    elif sort_by == 'opportunity':
        return df.sort_values(by='opportunity_count', ascending = False)
    else:
        return df  # return unsorted if sort_by parameter is not recognized

# Main
def main():
    ''' Main function to process a CSV file of opportunity contracts.'''
    # Load the CSV file into a DataFrame
    df = pd.read_csv(FILE_PATH, quoting=csv.QUOTE_ALL, escapechar="\\")
    
    # Iterate through each row in the dataframe
    for _, row in df.iterrows():
         # Opportunity-related information
        opportunity_info = [row['sub_tier'], row['title']]
        # Extracting primary contact information
        primary_contact = row['primary_contact_full_name']
        primary_contact_info = [
            row['primary_contact_email'],
            row['primary_contact_phone'],
            row['State'],
            row['City'],
            row['agency']
        ]

        add_to_dict(primary_contact, primary_contact_info, opportunity_info)

        # Extracting secondary contact information if present
        if 'secondary_contact_full_name' in df.columns and row['secondary_contact_full_name'] and not pd.isna(row['secondary_contact_full_name']):
            secondary_contact = row['secondary_contact_full_name']
            secondary_contact_info = [
                row['secondary_contact_email'],
                row['secondary_contact_phone'],
                row['State'],
                row['City'],
                row['agency']
            ]
            add_to_dict(secondary_contact, secondary_contact_info, opportunity_info)

    # Convert sets to strings for the new DataFrame
    for key in contact_dict:
        contact_dict[key][6] = ', '.join(contact_dict[key][6])  # Departments
        contact_dict[key][7] = ', '.join(contact_dict[key][7])  # Contract types

    # Update columns
    new_df = pd.DataFrame.from_dict(contact_dict, orient='index', columns=['email', 'phone number', 'state', 'city', 'agency', 'opportunity_count', 'associated_departments', 'contract_types'])
    new_df['opportunity_count'] = new_df['opportunity_count'].astype(int)

    # Format names and sort
    new_df.reset_index(inplace=True)
    new_df['index'] = new_df['index'].str.title()  # Format names
    new_df.rename(columns={'index': 'name'}, inplace=True)
    new_df['name'] = new_df['name'].apply(clean_name)
    sorted_df = sort_dataframe(new_df, SORTING_PARAMETER)

    # Save the new dataframe to a CSV file
    sorted_df.to_csv(OUTPUT_CSV_PATH, index=False)

    print(f"Processed contacts saved to {OUTPUT_CSV_PATH}")

if __name__ == "__main__":
    main()