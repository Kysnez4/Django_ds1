from flask import Flask, Response, send_from_directory
import os

app = Flask(__name__)

# Путь к директории с шаблонами
TEMPLATES_DIR = os.path.abspath('.')

# Маршрут для статических файлов (CSS, JS, изображения)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(TEMPLATES_DIR, 'static'), filename)

# Функция для загрузки HTML-страницы
def load_html_page(page_name):
    try:
        with open(f'templates/{page_name}', 'r', encoding='utf-8') as file:
            return Response(file.read(), mimetype='text/html')
    except FileNotFoundError:
        return Response("Страница не найдена", status=404)

# Главная страница
@app.route('/')
def main_page():
    return load_html_page('main.html')

# Страница каталога
@app.route('/catalog.html')
def catalog_page():
    return load_html_page('catalog.html')

# Страница категории
@app.route('/category.html')
def category_page():
    return load_html_page('category.html')

# Страница контактов
@app.route('/contacts.html')
def contacts_page():
    return load_html_page('contacts.html')

# Обработка всех остальных путей (возвращаем главную страницу)
@app.route('/<path:path>')
def catch_all(path):
    return load_html_page('main.html')

if __name__ == '__main__':
    app.run(debug=True)