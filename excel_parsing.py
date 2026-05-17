import openpyxl
from os import path
from constants import HEADERS


def load_file(filepath):
    table = []
    workbook = openpyxl.load_workbook(filepath)
    sheet = workbook.active
    for row in sheet:
        row_data = []
        for cell in row:
            row_data.append(cell.value)
        table.append(row_data)
    return table


   
def remove_first_col(table):
    without_first_col = []
    for row in table:
        without_first_col.append(row[1:])
    return without_first_col

    

def remove_empty_rows(without_first_col):
    clear_data_table = []
    for row in without_first_col:
        has_data = False
        for cell in row:
            if cell:
                has_data = True
        if has_data:
            clear_data_table.append(row)
    return clear_data_table


    
def build_objects(clear_data_table):
    objects = []
    for row in clear_data_table:
        new_object = dict(zip(HEADERS, row))
        objects.append(new_object)
    return objects


def do_callable_phones(objects):
    upd = '+'
    for row in objects:
        row['phone'] = upd + str(row['phone'])
    return objects

def process_file(filepath):
    table = load_file(filepath)
    removed_first_col = remove_first_col(table)
    removed_empty_rows = remove_empty_rows(removed_first_col)
    built_objects = build_objects(removed_empty_rows)
    done_table = do_callable_phones(built_objects)
    return done_table