from flask import Flask, render_template, request
from functions import process_file, find_by_id
from os import path


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        file = request.files['file']
        dir_name = 'C:/promo_codes/uploads/'
        file_name = file.filename
        filepath = path.join(dir_name, file_name)
        file.save(filepath)
        process_file(filepath)
        
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