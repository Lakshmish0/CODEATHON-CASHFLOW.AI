
# Import necessary libraries
import pandas as pd
import numpy as np

# Create a corrected dataset of 50 rows
data = {
    'Work_Experience': np.random.randint(1, 16, 50),
    'Google_Maps_Presence': np.random.choice([0, 1], 50),
    'Google_Maps_Rating': np.random.uniform(3.5, 5.0, 50).round(1),
    'Population_in_Area': np.random.randint(3000, 50000, 50),
    'Growth_Rate': np.random.randint(4, 21, 50),
    'Raw_Material_Cost': np.random.randint(120, 350, 50),
    'Monthly_Income': np.random.randint(10000, 35000, 50),
    'Monthly_Expenditure': np.random.randint(7000, 25000, 50),
    'CF_Rating': np.random.randint(2, 6, 50),
    'Consistency': np.random.randint(5, 11, 50),
    'Risk_Multiplier': np.random.uniform(0.70, 0.92, 50).round(2),
}

# Calculate loan amount based on some heuristics (as a placeholder)
# This is a dummy calculation for now
loan_amount = (
    data['Work_Experience'] * 1000 +
    data['Google_Maps_Rating'] * 1000 +
    data['Monthly_Income'] * 0.1 -
    data['Monthly_Expenditure'] * 0.1 -
    data['Raw_Material_Cost'] * 0.5
)

# Store the loan amount in the data dictionary
data['Loan_Amount'] = loan_amount.round(0)

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
csv_filename = "/home/greatness-within/PycharmProjects/LoanAproval/data.csv"
df.to_csv(csv_filename, index=False)

csv_filename  # Provide the path for download
