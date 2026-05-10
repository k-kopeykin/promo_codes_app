import openpyxl
import json
from os import path

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

def do_callable_phones(objects):
    upd = '+'
    for row in objects:
        row['Телефон'] = upd + str(row['Телефон'])
    return objects

    
def save_json(objects):
    with open('data/output.json', 'w', encoding='utf-8') as data:
        json.dump(objects, data, ensure_ascii=False, indent=4)
    return 'data/output.json'
    

def process_file(filepath):
    table = load_file(filepath)
    removed_first_col = remove_first_col(table)
    removed_empty_rows = remove_empty_rows(removed_first_col)
    built_objects = build_objects(removed_empty_rows)
    done_table = do_callable_phones(built_objects)
    return done_table

def merge_data(done_table):
    if not path.exists('data/output.json'):
        
        return {'json_path': save_json(done_table),
                 'total_count': len(done_table), 
                 'added_count': len(done_table)}
    else:
        with open('data/output.json', 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        old_numbers = {row['Телефон'] for row in old_data}
        
        added_count = 0
        for row in done_table:
            if row['Телефон'] not in old_numbers:
                old_data.append(row)
                old_numbers.add(row['Телефон'])
                added_count += 1
        return  {'json_path': save_json(old_data),
                 'total_count': len(old_data), 
                 'added_count': added_count}



def find_by_id(id):
    with open('data/output.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for row in data:
            if str(row['id']) == str(id):
                return row
        
