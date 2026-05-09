from flask import Flask, render_template, request
from functions import process_file, find_by_id, merge_data
from os import path, makedirs, remove

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
        merge_data(done_table)
        remove(filepath)
        return render_template('search.html')

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
            return render_template('client.html', user=result)
        

if __name__ == '__main__':
    app.run()