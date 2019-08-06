from http.server import BaseHTTPRequestHandler, HTTPServer
import sys, os, subprocess

# 服务器内部异常
class ServerException(Exception):
    pass

# 条件处理基类
class base_case(object):

    # 文件处理函数
    def handle_file(self, handler, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            handler.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(full_path, msg)
            handler.handle_error(msg)
    
    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    def test(self, handler):
        assert False, 'Not implemented.'

    def act(self, handler):
        assert False, 'Not implemented.'

# 文件或目录不存在
class case_no_file(base_case):
    def test(self, handler):
        return not os.path.exists(handler.full_path)
    
    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))

# 处理脚本文件
class case_cgi_file(base_case):
    def run_cgi(self, handler):
        data = subprocess.check_output(["python3", handler.full_path], shell=False)
        handler.send_content(data)

    def test(self, handler):
        return os.path.isfile(handler.full_path) and handler.full_path.endswith('.py')

    def act(self, handler):
        self.run_cgi(handler)

# 文件存在
class case_existing_file(base_case):
    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        self.handle_file(handler, handler.full_path)

# 根路径下返回主页文件
class case_directory_index_file(base_case):
    def test(self, handler):
        return os.path.isdir(handler.full_path) and os.path.isfile(self.index_path(handler))

    def act(self, handler):
        self.handle_file(handler, self.index_path(handler))

# 所有情况都不符合时的默认处理类
class case_always_fail(base_case):
    def test(self, handler):
        return True

    def act(self, handler):
        raise ServerException("Unknown object '{0}'".format(handler.path))

# 处理请求并返回页面
# 路径合法则返回相应处理
# 否则返回错误页面
class RequestHandler(BaseHTTPRequestHandler):

    Cases = [
        case_no_file(),
        case_cgi_file(),
        case_existing_file(),
        case_directory_index_file(),
        case_always_fail()
    ]

    # 错误页面模板
    Error_Page = '''\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
    '''

    # 处理GET请求
    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path
            for case in self.Cases:
                print(case)
                if case.test(self):
                    case.act(self)
                    break
        except Exception as msg:
            self.handle_error(msg)

    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content.encode('utf-8'), 404)

    # 发送内容
    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()