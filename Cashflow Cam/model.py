import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np


class LoanModel:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.df = pd.DataFrame(self.data)

        # Preprocess Population Data (Scaling)
        self.scaler = StandardScaler()
        self.df['Population_in_Area_scaled'] = self.scaler.fit_transform(self.df[['Population_in_Area']])

        # Features and Target (Assume Loan Amount is the target)
        self.X = self.df[['Work_Experience', 'Google_Maps_Presence', 'Google_Maps_Rating',
                          'Population_in_Area_scaled', 'Raw_Material_Cost',
                          'Monthly_Income', 'Monthly_Expenditure', 'CF_Rating', 'Consistency',
                          ]]

        self.y = self.df['Loan_Amount']  # Example target (you can adjust based on your use case)

        # Train-Test Split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2,
                                                                                random_state=42)

        # XGBoost Model
        self.model = xgb.XGBRegressor()
        self.model.fit(self.X_train, self.y_train)

    def evaluate(self):
        # Make Predictions
        predictions = self.model.predict(self.X_test)

        # Calculate performance metrics
        mae = mean_absolute_error(self.y_test, predictions)
        mse = mean_squared_error(self.y_test, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_test, predictions)

        print(f"Mean Absolute Error (MAE): {round(mae, 2)}")
        print(f"Mean Squared Error (MSE): {round(mse, 2)}")
        print(f"Root Mean Squared Error (RMSE): {round(rmse, 2)}")
        print(f"R-squared (R²): {round(r2, 2)}")

    def adjust_loan(self, X_test_data):
        # Make Predictions
        predictions = self.model.predict(X_test_data)

        adjusted_predictions = []
        for i, consistency in enumerate(X_test_data['Consistency']):
            loan = predictions[i]
            # If Consistency is greater than 7, reduce loan by 0.5%
            if consistency > 7:
                adjusted_loan = round(float(loan * (1 - 0.005)), 2)  # Reducing loan by 0.5%
                # print(f"the dynamically adjusted loan comes up to be {adjusted_loan}")
            else:
                adjusted_loan = round(float(loan), 2)  # Just rounding to 2 decimals if no adjustment
                # print(f"the static loan will be {adjusted_loan}")
            adjusted_predictions.append(adjusted_loan)

        return adjusted_predictions


# Example usage
data_path = "/home/greatness-within/Documents/data.csv"
loan_model = LoanModel(data_path)

# Evaluate the model
loan_model.evaluate()

# Adjust loan predictions based on Consistency
# Example X_test data needs to be a DataFrame, here's a sample row with proper structure:
sample_data = pd.DataFrame({
    'Work_Experience': [10],
    'Google_Maps_Presence': [1],
    'Google_Maps_Rating': [4.5],
    'Population_in_Area_scaled': [0.2],  # this should be scaled before use
    'Raw_Material_Cost': [5000],
    'Monthly_Income': [20000],
    'Monthly_Expenditure': [15000],
    'CF_Rating': [4],
    'Consistency': [8],  # Consistency above 7 to trigger interest reduction
})

adjusted_loans = loan_model.adjust_loan(sample_data)
# print("Adjusted Loan Amounts: ", adjusted_loans)
