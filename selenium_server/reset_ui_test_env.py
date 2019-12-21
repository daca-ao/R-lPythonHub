import subprocess
import time

from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = ''
PORT_NUMBER = 9000

CLEAN_DRIVERS_CACHE = r'C:\\Selenium\\bin\\kill_browsers_drivers_proc.bat'
START_HUB = 'start C:\\Selenium\\bin\\start_selenium_hub.bat'
REGISTER_NODES = 'start C:\\Selenium\\bin\\start_selenium_node.bat'
STOP_HUB = r'C:\\Selenium\\bin\\stop_selenium_hub.bat'
UNREGISTER_NODES = r'C:\\Selenium\\bin\\unregister_selenium_node.bat'


class SeleniumHubHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        paths = {
            '/clean': self.clean_driver_cache,
            '/start': self.start_hub,
            '/stop': self.stop_hub,
            '/restart': self.restart_hub
        }

        if self.path in paths:
            self.respond_head(paths[self.path])
        else:
            self.respond_bad_request_error(self.path)

    def do_GET(self):
        self.do_HEAD()

    def respond_head(self, symbol):
        response = self.handle_http(symbol, self.path)
        self.wfile.write(response)

    def handle_http(self, batch_file, path):
        batch_file()

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        content = '''
        <html>
            <head>
                <title>UI Automation Test Hub</title>
            </head>
            <body>
                <p>You accessed path: {}.</p>
            </body>
        </html>
        '''.format(path)
        return bytes(content, 'UTF-8')

    def clean_driver_cache(self):
        subprocess.call(CLEAN_DRIVERS_CACHE)
        time.sleep(1)

    def start_hub(self):
        subprocess.Popen(START_HUB, shell=True)
        time.sleep(1)
        subprocess.Popen(REGISTER_NODES, shell=True)

    def stop_hub(self):
        subprocess.call(UNREGISTER_NODES)
        time.sleep(1)
        subprocess.call(STOP_HUB)

    def restart_hub(self):
        self.stop_hub()
        time.sleep(2)
        self.start_hub()

    def respond_bad_request_error(self, path):
        self.send_response(400)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        content = '''
        <html>
            <head>
                <title>UI Automation Test Hub</title>
            </head>
            <body>
                <p>You accessed path: {}, which is not legal.</p>
            </body>
        </html>
        '''.format(path)
        self.wfile.write(bytes(content, 'UTF-8'))


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), SeleniumHubHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(time.asctime(), 'Force management server to stop.')
        pass

    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
