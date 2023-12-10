import pandas as pd

# Example CSV file path
csv_path = 'C:/Users/marce/OneDrive/School/233/Project/dummy_table.csv'

# Load the original table from the CSV file
try:
    original_table = pd.read_csv(csv_path)
    #print("Original Table:")
    #print(original_table)
except FileNotFoundError:
    print(f"CSV file not found at {csv_path}. Please make sure the file exists.")

# Create a new table with qIDs including "Age"
quasi_identifiers_table = original_table[['Gender', 'Type of Report', 'Age']].copy()

# Create a new table with age categories
age_categories_table = quasi_identifiers_table.copy()

# Define age categories in increments of 5
age_categories_table['Age Category'] = pd.cut(age_categories_table['Age'], bins=range(0, 101, 5), labels=[f"{i}-{i+4}" for i in range(0, 100, 5)])

# Drop the original "Age" column
age_categories_table.drop(['Age'], axis=1, inplace=True)

# Display the new table with qIDs and Age Category
#print("\nTable with Quasi-Identifiers and Age Category:")
#print(age_categories_table)

# Count the number of records in each age category for each gender
records_count_by_age_category_gender = age_categories_table.groupby(['Age Category', 'Gender']).size().reset_index(name='Record Count')

# Filter out records with zero counts
records_count_by_age_category_gender = records_count_by_age_category_gender[records_count_by_age_category_gender['Record Count'] > 0]

# Sort by gender and age category
records_count_by_age_category_gender = records_count_by_age_category_gender.sort_values(by=['Gender', 'Age Category'])

# Calculate k-anonymity score for each age category for each gender
k_scores = records_count_by_age_category_gender.groupby(['Gender'])['Record Count'].min()

# Display the k-anonymity score for each gender
print("\nK-Anonymity Score for Each Gender:")
for gender, k in k_scores.items():
    print(f"k-anonymity for {gender} is {k}")

# Publish a table with only "Gender," "Age Category," and "Type of Report"
published_table = age_categories_table[['Gender', 'Age Category', 'Type of Report']]


# Display the published table
print("\nPublished Table:")
print(published_table)

# Export to CSV
export_csv_path = 'C:/Users/marce/OneDrive/School/233/Project/published_table.csv'
published_table.to_csv(export_csv_path, index=False)

print(f"\nPublished Table Exported to {export_csv_path}")
