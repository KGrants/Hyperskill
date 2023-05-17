import pandas as pd
from pathlib import Path

print("Input file name")
user_input = input(">")
my_df = pd.read_excel(user_input, sheet_name='Vehicles', dtype=str)
csv_name = Path(user_input)
csv_name.rename(csv_name.with_suffix('.csv'))
my_df.to_csv(csv_name)
print(f"{my_df.shape[0]} lines were imported to {csv_name}")

# Unexpected error in test #1
# We have recorded this bug and will fix it soon.
