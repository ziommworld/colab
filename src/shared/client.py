import gspread
from google.auth import default
import pandas as pd

from src.shared.common import list_converter, try_convert_to_numeric, tuple_converter


class GoogleSheetsClient:
    def __init__(self):
        self.online = True
        try:
            credentials, _ = default()
        except:
            self.online = False

        if self.online:
            self.client = gspread.authorize(credentials)
        else:
            pass

    def get_spreadsheet(self, spreadsheet_name):
        if self.online:
            return self.client.open(spreadsheet_name)
        else:
            pass

    def get_worksheet(self, spreadsheet_name, worksheet_name):
        if self.online:
            spreadsheet = self.client.open(spreadsheet_name)
            return spreadsheet.worksheet(worksheet_name)
        else:
            pass

    def get_df(
        self, spreadsheet_name, worksheet_name, tuple_columns=None, list_columns=None
    ):
        if self.online:
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
        else:
            # Handle the offline case as necessary, possibly raise an error or return an empty DataFrame
            return None

    def get_dict(self, spreadsheet_name, worksheet_name):
        if self.online:
            df = self.get_df(spreadsheet_name, worksheet_name)

            # Apply the function to the 'Value' column
            df["Value"] = df["Value"].apply(try_convert_to_numeric)

            # Convert the DataFrame to a dictionary with 'Name' as keys and 'Value' as values
            df_dict = pd.Series(df["Value"].values, index=df["Name"]).to_dict()
            return df_dict
        else:
            pass

    def update_worksheet(self, spreadsheet_name, worksheet_name, df):
        if self.online:
            spreadsheet = self.client.open(spreadsheet_name)
            worksheet = spreadsheet.worksheet(worksheet_name)
            worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        else:
            pass

    def add_worksheet(self, spreadsheet_name, worksheet_name, df=pd.DataFrame()):
        if self.online:
            spreadsheet = self.client.open(spreadsheet_name)
            worksheet = spreadsheet.add_worksheet(
                title=worksheet_name, rows=str(df.shape[0]), cols=str(df.shape[1])
            )
            worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        else:
            pass

    def get_or_add_worksheet(self, spreadsheet_name, worksheet_name, df=pd.DataFrame()):
        if self.online:
            spreadsheet = self.client.open(spreadsheet_name)
            try:
                worksheet = spreadsheet.worksheet(worksheet_name)
            except gspread.WorksheetNotFound:
                worksheet = spreadsheet.add_worksheet(
                    title=worksheet_name, rows=str(df.shape[0]), cols=str(df.shape[1])
                )
                worksheet.update([df.columns.values.tolist()] + df.values.tolist())
            return worksheet
        else:
            pass

    def delete_worksheet(self, spreadsheet_name, worksheet_name):
        if self.online:
            spreadsheet = self.client.open(spreadsheet_name)
            worksheet = spreadsheet.worksheet(worksheet_name)
            spreadsheet.del_worksheet(worksheet)
        else:
            pass

    def clear_worksheet(self, spreadsheet_name, worksheet_name):
        if self.online:
            spreadsheet = self.client.open(spreadsheet_name)
            worksheet = spreadsheet.worksheet(worksheet_name)
            worksheet.clear()
        else:
            pass

    def get_cell(self, spreadsheet_name, worksheet_name, cell="A1"):
        if self.online:
            worksheet = self.get_worksheet(spreadsheet_name, worksheet_name)
            return worksheet.acell(cell).value
        else:
            pass

    def set_cell(self, spreadsheet_name, worksheet_name, cell="A1", value=""):
        if self.online:
            worksheet = self.get_worksheet(spreadsheet_name, worksheet_name)
            worksheet.update_acell(cell, value)
        else:
            pass

    def get_range(self, spreadsheet_name, worksheet_name, range="A1:B2"):
        if self.online:
            worksheet = self.get_worksheet(spreadsheet_name, worksheet_name)
            return worksheet.get(range)
        else:
            pass

    def set_range(self, spreadsheet_name, worksheet_name, range="A1:B2", values=[]):
        if self.online:
            worksheet = self.get_worksheet(spreadsheet_name, worksheet_name)
            worksheet.update(range, values)
        else:
            pass
