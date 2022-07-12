import pandas as pd

def write_chart(writer, sheet, shape):
    workbook  = writer.book
    worksheet = writer.sheets[sheet]
    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({'values': [sheet, 1, 1, shape[0], 1]})
    worksheet.insert_chart(1, 3, chart)


# Write data to excek file
def write_excel(spreadsheet, data):
    # data[0] -> correlation matrix
    # data[1] -> data for no del toggle bar chart
    # data[2] -> data for  del toggle bar chart
    # data[3] -> data for in_del toggle bar chart

    with pd.ExcelWriter("./spreadsheets/" + spreadsheet + ".xlsx") as writer:
        # correlation matrix on first sheet
        data[0].to_excel(writer, index=True, sheet_name="Correlation matrix")

        # no del toggles bar chart
        data[1].to_excel(writer, index=True, sheet_name="Toggles no del")
        write_chart(writer, "Toggles no del", data[1].shape)

        # no del toggles bar chart
        data[2].to_excel(writer, index=True, sheet_name="Toggles del")
        write_chart(writer, "Toggles del", data[2].shape)

        # no del toggles bar chart
        data[3].to_excel(writer, index=True, sheet_name="Toggles input del")
        write_chart(writer, "Toggles input del", data[3].shape)