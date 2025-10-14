from http.server import HTTPServer, SimpleHTTPRequestHandler
import os


class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Устанавливаем корневую директорию для сервера
        self.templates_dir = os.path.abspath('.')
        super().__init__(*args, directory=self.templates_dir, **kwargs)

    def do_GET(self):
        # Обрабатываем маршруты
        if self.path == '/':
            self.serve_file('templates/main.html')
        elif self.path == '/catalog.html':
            self.serve_file('templates/catalog.html')
        elif self.path == '/category.html':
            self.serve_file('templates/category.html')
        elif self.path == '/contacts.html':
            self.serve_file('templates/contacts.html')
        elif self.path.startswith('/static/'):
            # Обрабатываем статические файлы
            self.serve_static_file(self.path[8:])  # Убираем '/static/' из пути
        else:
            # Для всех остальных путей возвращаем главную страницу
            self.serve_file('templates/main.html')

    def serve_file(self, file_path):
        try:
            full_path = os.path.join(self.templates_dir, file_path)
            if not os.path.exists(full_path):
                self.send_error(404, "Страница не найдена")
                return

            with open(full_path, 'r', encoding='utf-8') as file:
                content = file.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))

        except Exception as e:
            self.send_error(500, f"Ошибка сервера: {str(e)}")

    def serve_static_file(self, filename):
        static_dir = os.path.join(self.templates_dir, 'static')
        try:
            full_path = os.path.join(static_dir, filename)
            if not os.path.exists(full_path):
                self.send_error(404, "Файл не найден")
                return

            # Определяем MIME-тип по расширению файла
            ext = os.path.splitext(filename)[1].lower()
            mime_types = {
                '.css': 'text/css',
                '.js': 'application/javascript',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.svg': 'image/svg+xml',
                '.ico': 'image/x-icon'
            }
            content_type = mime_types.get(ext, 'application/octet-stream')

            with open(full_path, 'rb') as file:
                content = file.read()

            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)

        except Exception as e:
            self.send_error(500, f"Ошибка сервера: {str(e)}")


def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, CustomHandler)
    print("Сервер запущен на http://localhost:8000")
    print("Для остановки сервера нажмите Ctrl+C")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        httpd.shutdown()


if __name__ == '__main__':
    run_server()