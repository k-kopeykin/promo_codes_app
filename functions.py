import openpyxl
import json
from os import path




    
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
        old_ids = {row['id'] for row in old_data}
        
        added_count = 0
        for row in done_table:
            if row['id'] not in old_ids:
                old_data.append(row)
                old_ids.add(row['id'])
                added_count += 1
        return  {'json_path': save_json(old_data),
                 'total_count': len(old_data), 
                 'added_count': added_count}



def find_by_id(id):
                
    # with open('data/output.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    #     for row in data:
    #         if str(row['id']) == str(id):
                return row
        
def insert_client(cursor,client):
    cursor.execute(
        """
            INSERT INTO clients (id, 
                        name, 
                        diet, 
                        time_interval, 
                        address, 
                        phone, 
                        comment) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)

        """,
        (
           client['id'], 
            client['name'], 
            client['diet'], 
            client['time_interval'], 
            client['address'], 
            client['phone'], 
            client['comment'] 
        )
    )

def insert_clients(done_table):
    for client in done_table:
        insert_client(client)
    

def build_objects(row):
    client = dict(zip(HEADERS, row))
    return client

def do_callable_phones(client):
    client['phone'] = '+' + str(client['phone'])
    return client