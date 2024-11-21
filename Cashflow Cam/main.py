from model import LoanModel
import pandas as pd

data_path = "/home/greatness-within/Documents/data.csv"
obj = LoanModel(data_path)


ans = obj.adjust_loan(sample_data)
print(ans)