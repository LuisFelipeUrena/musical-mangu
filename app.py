from flask import Flask, render_template, jsonify
from schema_extractor import extract_schema
from description_generator import generate_description

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/schema')
def get_schema():
    schema_info = extract_schema()
    return jsonify(schema_info)

@app.route('/api/description/<schema>/<table>')
def get_description(schema, table):
    schema_info = extract_schema()
    columns = schema_info[schema][table]
    description = generate_description(table, columns)
    return jsonify({"description": description})

if __name__ == '__main__':
    app.run(debug=True)