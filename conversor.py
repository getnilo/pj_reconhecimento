import pandas as pd
import sys

def convert(csv_,output_):
    csv_file = csv_
    df = pd.read_csv(csv_file)

    excel_file = output_
    df.to_excel(excel_file, index=False, engine='openpyxl')

    print(f"Arquivo '{csv_file}' transformado em: '{excel_file}'")
