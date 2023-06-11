from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import urlparse, parse_qs
from num2words import num2words

def num_to_word(num):
    text = num2words(num, lang='es')
    return text

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            with open('index.html') as file:
                template = file.read()
                
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(template, 'utf-8'))
       

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)

        if 'number' in params:
            num = int(params['number'][0])

            result = num_to_word(num)

            response = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <link rel="stylesheet" href="https://bootswatch.com/5/darkly/bootstrap.min.css">
                <title>Miniproyectos | Numeros a Texto</title>
            </head>
            <body>
                <main class="container text-center ">
                    <h1>Conversión de número a texto</h1>
                    <form method="POST" action="/">
                        <label for="number">Ingresa un número:</label>
                        <input type="number" name="number" id="number">
                        <input type="submit" value="Convertir">
                    </form>
                    <p>El número ingresado es: <span class="text-info">{num}</span></p>
                    <p>El número en palabras es: <span class="text-success">{result}</span></p>
                </main>
            </body>
            </html>
            """

            # Envía la respuesta al cliente
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(response, 'utf-8'))

# Configura el servidor
def run(server_class=HTTPServer, handler_class=MyRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Servidor en ejecución en el puerto', port)
    httpd.serve_forever()

# Ejecuta el servidor
if __name__ == '__main__':
    run()
