import sys
from openpyxl import load_workbook
import pandas as pd

# ship_excel_schema contains facts about about how the ship data is organized in Excel
import ship_excel_schema
import json
import time


# represent each sheet in an Excel workbook as a separate JSON object
# returns a list of JSON ship objects

def get_ships(excel_ship_file):
    # ships is the list of JSON ship objects that will be returned
    ships = []
    labels = ['name', 'year_of_birth', 'age', 'place_of_birth', 'home_address', 'last_ship_name', 'last_ship_port',
              'last_ship_leaving_date', 'this_ship_joining_date', 'this_ship_joining_port', 'this_ship_capacity',
              'this_ship_leaving_date', 'this_ship_leaving_port', 'this_ship_leaving_cause', 'signed_with_mark',
              'additional_notes']
    t_names = [str(i) for i in range(1, 18)]

    df_data = pd.read_excel(excel_ship_file, skiprows=8, names=t_names)
    df_data.drop(['6'], axis=1, inplace=True)
    df_data.columns = labels
    df_data.dropna(axis=0, how='all', inplace=True)

    tmp_file_name = str(time.time())
    tmp_file_path = "./tmp/" + tmp_file_name + ".csv"
    df_data.to_csv(tmp_file_path, index=False)

    df_p = df_data = pd.read_csv(tmp_file_path)

    df_data.fillna(axis=0, method='ffill', inplace=True)

    # df_data.fillna(value='unknow', inplace=True)
    # load the Excel workbook
    try:
        wb = load_workbook(filename=excel_ship_file)

        # assume the vessel data is on sheet 1 of the workbook
        vessel_name = wb.active[ship_excel_schema.vessel_name].value
        official_number = wb.active[ship_excel_schema.official_number].value
        port_of_registry = wb.active[ship_excel_schema.port_of_registry].value

        for sheet in wb:
            # get ship attributes from the first worksheet in the workbook
            ship = {}
            ship["vessel_name"] = vessel_name
            ship["official_number"] = official_number
            ship["port_of_registry"] = port_of_registry
            ship["mariners"] = []

            # get the start row for mariner data
            mariners_start_row = ship_excel_schema.mariners_start_row

            # iterate over the worksheets to find all the mariner data
            row = mariners_start_row
            col = 1
            while not (sheet.cell(column=col, row=row).value is None):
                mariner = {}
                for attr, col in ship_excel_schema.mariner_attributes.items():
                    if not sheet.cell(column=col, row=row).value is None:
                        mariner[attr] = sheet.cell(column=col, row=row).value
                ship["mariners"].append(mariner)
                row += 1

            ships.append(ship)

    except:
        # deal with the error if the file cannot be opened
        print(excel_ship_file)

    return ships


# /home/hr/PycharmProjects/Demo818/ABERSHIP_transcription_vtls004566921/Series 1 - 10/Series_1_vtls004566957/File_1-1_vtls004583057.xlsx

if __name__ == "__main__":
    # get the name of the Excel File
    print("Input the name of the Excel Ship File")
    # excel_ship_file = sys.stdin.readline().strip()
    excel_ship_file = "/home/hr/PycharmProjects/Demo818/ABERSHIP_transcription_vtls004566921/Series 1 - 10/Series_1_vtls004566957/File_1-1_vtls004583057.xlsx"

    ships = get_ships(excel_ship_file)
    for ship in ships:
        print(json.dumps(ship))
