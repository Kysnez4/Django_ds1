from flask import Flask, Response

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def contacts_page(path):
    # Читаем содержимое HTML-файла
    with open('templates/index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Возвращаем ответ с типом content-type text/html
    return Response(html_content, mimetype='text/html')


if __name__ == '__main__':
    app.run(debug=True)