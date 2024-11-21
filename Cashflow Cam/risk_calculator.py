def calculate_interest_rate(base_rate, risk_multiplier, risk_multiplier_factor, consistency):
    # Calculate the interest rate based on risk multiplier
    interest_rate = base_rate + (risk_multiplier_factor * (1 - risk_multiplier))

    # Apply consistency adjustment (drop interest rate by 0.5% if consistency > 7)
    if consistency > 7:
        interest_rate -= 0.5

    return interest_rate


def calculate_total_repayment(loan_amount, interest_rate):
    # Calculate the total interest
    interest = loan_amount * interest_rate / 100
    # Calculate the total repayment
    total_repayment = loan_amount + interest
    return interest, total_repayment


# Example data
base_rate = 7.0  # Base interest rate (in percentage)
risk_multiplier = 0.85  # Risk multiplier (lower risk)
risk_multiplier_factor = 0.1  # Factor that adjusts based on the risk multiplier
loan_amount = 20000  # Loan amount in USD
consistency = 8  # Consistency score

# Step 1: Calculate Interest Rate
interest_rate = calculate_interest_rate(base_rate, risk_multiplier, risk_multiplier_factor, consistency)
print(f"Interest Rate: {interest_rate:.2f}%")

# Step 2: Calculate Interest and Total Repayment
interest, total_repayment = calculate_total_repayment(loan_amount, interest_rate)
print(f"Interest: ${interest:.2f}")
print(f"Total Repayment: ₹{total_repayment:.2f}")
