from flask import Flask, render_template, request
from excel_parsing import process_file
from os import path, makedirs, remove
from db import save_to_db, find_by_id, get_connect
from presentation import do_callable_phone, build_object

makedirs('uploads', exist_ok=True)
makedirs('data', exist_ok=True)
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        file = request.files['file']
        dir_name = 'uploads'
        file_name = file.filename
        filepath = path.join(dir_name, file_name)
        file.save(filepath)
        done_table = process_file(filepath)
        result = save_to_db(done_table)
        remove(filepath)
        return render_template(
    "search.html",
    added_count=result["added_count"]
    
)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    else:
        id = request.form['id']
        result = find_by_id(id)
        if not result:
            return render_template('search.html')
        else:
            raw_client = build_object(result)
            client = do_callable_phone(raw_client)
            return render_template('client.html', user=client)
        



if __name__ == '__main__':
    app.run()