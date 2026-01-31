class SpreadsheetBackend:
    def list_sheets(self):
        raise NotImplementedError

    def read_range(self, sheet, cell_range):
        raise NotImplementedError
