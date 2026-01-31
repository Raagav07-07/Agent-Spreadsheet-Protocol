import os
import re
from narwhals import col
import pandas as pd
from asp.core.backend import SpreadsheetBackend
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
class CSVBackend(SpreadsheetBackend):
    def __init__(self, folder="data"):
        self.folder = os.path.join(BASE_DIR, folder)

    def list_sheets(self):
        return [
            f.replace(".csv", "")
            for f in os.listdir(self.folder)
            if f.endswith(".csv")
        ]
    
    def col_to_index(self, col):
        index = 0
        for c in col:
            index = index * 26 + (ord(c.upper()) - ord('A') + 1)
        return index - 1

    def parse_range(self, cell_range):
        match = re.match(r"([A-Z]+)(\d+):([A-Z]+)(\d+)", cell_range)
        if not match:
            raise ValueError("Invalid range format")
        start_col, start_row, end_col, end_row = match.groups()
        return (
            int(start_row) - 1,
            int(end_row),
            self.col_to_index(start_col),
            self.col_to_index(end_col) + 1
        )

    def read_range(self, sheet, cell_range):
        path = os.path.join(self.folder, f"{sheet}.csv")
        df = pd.read_csv(path)
        row_start, row_end, col_start, col_end = self.parse_range(cell_range)
        sliced_df = df.iloc[row_start:row_end, col_start:col_end]
        return sliced_df.to_dict(orient="records")
    


