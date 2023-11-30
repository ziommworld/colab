import gspread
from google.auth import default
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

from src.shared.common import list_converter, try_convert_to_numeric, tuple_converter


class GoogleSheetsClient:
    def __init__(self):
        # Try to detect if we are running on Google Colab
        try:
            import google.colab

            self.is_colab = True
        except ImportError:
            self.is_colab = False

            # Authenticate using Colab's authentication methods
            from google.colab import auth

            auth.authenticate_user()
            from google.auth import default

            credentials, _ = default()
        else:
            # Authenticate using a service account in a local environment
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
            ]
            key_file_path = "../env/colab.json"  # Ensure this path is correct in your local environment
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                key_file_path, scope
            )

        self.client = gspread.authorize(credentials)

    def get_spreadsheet(self, spreadsheet_name):
        return self.client.open(spreadsheet_name)

    def get_worksheet(self, spreadsheet_name, worksheet_name):
        spreadsheet = self.get_spreadsheet(spreadsheet_name)
        return spreadsheet.worksheet(worksheet_name)

    def get_df(
        self, spreadsheet_name, worksheet_name, tuple_columns=None, list_columns=None
    ):
        worksheet = self.get_worksheet(spreadsheet_name, worksheet_name)
        records = worksheet.get_all_records()
        df = pd.DataFrame(records)

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

    def update_worksheet(self, spreadsheet_name, worksheet_name, df):
        spreadsheet = self.client.open(spreadsheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())

    def add_worksheet(self, spreadsheet_name, worksheet_name, df=pd.DataFrame()):
        spreadsheet = self.client.open(spreadsheet_name)
        worksheet = spreadsheet.add_worksheet(
            title=worksheet_name, rows=str(df.shape[0]), cols=str(df.shape[1])
        )
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())

    def get_or_add_worksheet(self, spreadsheet_name, worksheet_name, df=pd.DataFrame()):
        spreadsheet = self.client.open(spreadsheet_name)
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(
                title=worksheet_name, rows=str(df.shape[0]), cols=str(df.shape[1])
            )
            worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        return worksheet

    def delete_worksheet(self, spreadsheet_name, worksheet_name):
        spreadsheet = self.client.open(spreadsheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)
        spreadsheet.del_worksheet(worksheet)

    def clear_worksheet(self, spreadsheet_name, worksheet_name):
        spreadsheet = self.client.open(spreadsheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)
        worksheet.clear()

    def get_cell(self, spreadsheet_name, worksheet_name, cell="A1"):
        """Get the value of a cell."""
        worksheet = self.get_worksheet(spreadsheet_name, worksheet_name)
        return worksheet.acell(cell).value

    def set_cell(self, spreadsheet_name, worksheet_name, cell="A1", value=""):
        worksheet = self.get_worksheet(spreadsheet_name, worksheet_name)
        worksheet.update_acell(cell, value)

    def get_range(self, spreadsheet_name, worksheet_name, range="A1:B2"):
        worksheet = self.get_worksheet(spreadsheet_name, worksheet_name)
        return worksheet.get(range)

    def set_range(self, spreadsheet_name, worksheet_name, range, values=[]):
        """
        Sets a range of cells in a specified worksheet with given values.

        Parameters:
        range (str): Range of cells to update. Example: 'A1:B2'.
        values (list): List of values to set in the specified range. Defaults to an empty list.
        """
        worksheet = self.get_worksheet(spreadsheet_name, worksheet_name)
        worksheet.update(range, values)
