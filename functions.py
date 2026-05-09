import openpyxl
import json

HEADERS = [
        'id',
        'Имя',
        'Рацион',
        'Интервал',
        'Адрес',
        'Телефон',
        'Комментарий'
        ]


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

    
def save_json(objects):
    with open('data/output.json', 'w', encoding='utf-8') as data:
        json.dump(objects, data, ensure_ascii=False, indent=4)
    return 'output.json'
    

def process_file(filepath):
    
    return save_json(build_objects(remove_empty_rows(remove_first_col(load_file(filepath)))))


def find_by_id(id):
    with open('data/output.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for row in data:
            if str(row['id']) == str(id):
                return row
        
