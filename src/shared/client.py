import gspread
from google.auth import default
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import pandas as pd
from src.shared.common import list_converter, try_convert_to_numeric, tuple_converter


class GoogleSheetsClient:
    def __init__(self, json_keyfile_path="../env/colab.json", test_mode=False):
        self.test_mode = test_mode
        # Try to detect if we are running on Google Colab
        try:
            from google.colab import auth

            # Authenticate using Colab's authentication methods

            auth.authenticate_user()
            from google.auth import default

            credentials, _ = default()
        except ImportError:
            # Authenticate using a service account in a local environment
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
            ]
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                json_keyfile_path, scope
            )

        self.client = gspread.authorize(credentials)

    # ===================== SPREADSHEETS =====================

    def create_spreadsheet(self, spreadsheet_name):
        """Create a new spreadsheet with the given name."""
        return self.client.create(spreadsheet_name)

    def read_spreadsheet(self, spreadsheet_name):
        """Get a spreadsheet by name. Create it if it does not exist."""
        try:
            return self.client.open(spreadsheet_name)
        except gspread.SpreadsheetNotFound:
            return self.create_spreadsheet(spreadsheet_name)

    def delete_spreadsheet(self, spreadsheet_name):
        """Delete a spreadsheet with the given name."""
        # Attempt to open the spreadsheet by name to get its ID
        try:
            spreadsheet = self.client.open(spreadsheet_name)
            spreadsheet_id = spreadsheet.id
        except gspread.SpreadsheetNotFound:
            raise Exception(f"Spreadsheet named '{spreadsheet_name}' not found.")

        # Delete the spreadsheet using the Google Drive API
        drive_service = build("drive", "v3", credentials=self.client.auth)
        drive_service.files().delete(fileId=spreadsheet_id).execute()

    def spreadsheet_exists(self, spreadsheet_name):
        try:
            self.client.open(spreadsheet_name)
            return True
        except gspread.SpreadsheetNotFound:
            return False

    # ===================== WORKSHEETS =====================

    def create_worksheet(self, spreadsheet_name, worksheet_name):
        spreadsheet = self.client.open(spreadsheet_name)
        worksheet = spreadsheet.add_worksheet(
            title=worksheet_name, rows=str(1), cols=str(1)
        )

    def read_worksheet(self, spreadsheet_name, worksheet_name, rows=1000, cols=26):
        """Get a worksheet by name. Create it if it does not exist."""
        spreadsheet = self.read_spreadsheet(spreadsheet_name)
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(
                title=worksheet_name, rows=str(rows), cols=str(cols)
            )
        return worksheet

    def update_worksheet(self, spreadsheet_name, worksheet_name, df):
        spreadsheet = self.client.open(spreadsheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)
        # Convert DataFrame to a list of lists
        values = [df.columns.values.tolist()] + df.values.tolist()
        print(type(values), values)
        # Update the worksheet starting at 'A1'
        worksheet.update(values=values, range_name="A1")

    def delete_worksheet(self, spreadsheet_name, worksheet_name):
        spreadsheet = self.client.open(spreadsheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)
        spreadsheet.del_worksheet(worksheet)

    def get_all_worksheets(self, spreadsheet_name):
        """Get all worksheets in the specified spreadsheet."""
        try:
            spreadsheet = self.read_spreadsheet(spreadsheet_name)
            return spreadsheet.worksheets()
        except gspread.SpreadsheetNotFound:
            raise Exception(f"Spreadsheet named '{spreadsheet_name}' not found.")

    def clear_worksheet(self, spreadsheet_name, worksheet_name):
        spreadsheet = self.client.open(spreadsheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)
        worksheet.clear()

    # ===================== VALUES =====================

    def get_cell(self, spreadsheet_name, worksheet_name, cell="A1"):
        """Get the value of a cell."""
        worksheet = self.read_worksheet(spreadsheet_name, worksheet_name)
        return worksheet.acell(cell).value

    def set_cell(self, spreadsheet_name, worksheet_name, cell="A1", value=""):
        worksheet = self.read_worksheet(spreadsheet_name, worksheet_name)
        worksheet.update_acell(cell, value)

    def get_range(self, spreadsheet_name, worksheet_name, range="A1:B2"):
        worksheet = self.read_worksheet(spreadsheet_name, worksheet_name)
        return worksheet.get(range)

    def set_range(self, spreadsheet_name, worksheet_name, range, values=[]):
        """
        Sets a range of cells in a specified worksheet with given values.

        Parameters:
        range (str): Range of cells to update. Example: 'A1:B2'.
        values (list): List of values to set in the specified range. Defaults to an empty list.
        """
        worksheet = self.read_worksheet(spreadsheet_name, worksheet_name)
        worksheet.update(range, values)

    # ===================== CONVERT =====================

    def get_df(
        self, spreadsheet_name, worksheet_name, tuple_columns=None, list_columns=None
    ):
        if not self.test_mode:
            worksheet = self.read_worksheet(spreadsheet_name, worksheet_name)
            records = worksheet.get_all_records()
            df = pd.DataFrame(records)
        else:
            df = pd.read_csv(
                f"../data/{worksheet_name}.csv", dtype="object", na_filter=False
            )
            for col in df.columns:
                df[col] = df[col].apply(
                    lambda x: try_convert_to_numeric(x) if x != "" else x
                )

        # Apply tuple converter to specified tuple columns
        if tuple_columns:
            for column in tuple_columns:
                if column in df.columns:
                    df[column] = df[column].apply(tuple_converter)

        # Apply list converter to specified list columns
        if list_columns:
            for column in list_columns:
                if column in df.columns:
                    df[column] = df[column].apply(list_converter)

        return df

    def get_dict(self, spreadsheet_name, worksheet_name):
        df = self.get_df(spreadsheet_name, worksheet_name)

        # Apply the function to the 'Value' column
        df["Value"] = df["Value"].apply(try_convert_to_numeric)

        # Convert the DataFrame to a dictionary with 'Name' as keys and 'Value' as values
        df_dict = pd.Series(df["Value"].values, index=df["Name"]).to_dict()
        return df_dict
