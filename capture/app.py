"""Run the real Lazydocker against a local, read-only Docker API fixture.

Sample containers are fixture data, not hand-drawn UI. No user Docker socket is used.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import re
import threading

server = None


class DockerFixture(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        path = re.sub(r'^/v[\d.]+', '', self.path).split('?')[0]
        containers = [{'Id': name * 64, 'Names': ['/' + label], 'Image': image, 'ImageID': 'sha256:' + name * 64,
                       'Command': command, 'Created': 1767268800, 'State': 'running', 'Status': 'Up 2 hours',
                       'Ports': [], 'Labels': {}, 'HostConfig': {'NetworkMode': 'bridge'},
                       'NetworkSettings': {'Networks': {}}, 'Mounts': []}
                      for name, label, image, command in [('a', 'glyph-api', 'node:22-alpine', 'node server.js'),
                          ('b', 'glyph-cache', 'redis:7-alpine', 'redis-server'),
                          ('c', 'glyph-db', 'postgres:17-alpine', 'postgres')]]
        if path == '/_ping':
            value = b'OK'
        elif path == '/version':
            value = {'Version': '27.0.0', 'ApiVersion': '1.47', 'MinAPIVersion': '1.24', 'Os': 'linux', 'Arch': 'amd64'}
        elif path == '/info':
            value = {'Containers': 3, 'ContainersRunning': 3, 'Images': 3, 'Name': 'local-capture-fixture', 'ServerVersion': '27.0.0'}
        elif path == '/events':
            # Docker streams individual event objects, never an array. Keep the local stream idle.
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.flush()
            import time
            time.sleep(30)
            return
        elif path == '/containers/json':
            value = containers
        elif path == '/images/json':
            value = [{'Id': row['ImageID'], 'RepoTags': [row['Image']], 'Created': 1767268800, 'Size': 104857600,
                      'SharedSize': 0, 'VirtualSize': 104857600, 'Labels': {}, 'Containers': 1} for row in containers]
        elif path.endswith('/json') and path.startswith('/containers/'):
            row = containers[0]
            value = {'Id': row['Id'], 'Name': row['Names'][0], 'Created': '2026-01-01T12:00:00Z',
                     'Path': 'node', 'Args': ['server.js'], 'State': {'Status': 'running', 'Running': True,
                     'Pid': 100, 'StartedAt': '2026-01-01T12:00:00Z', 'FinishedAt': '0001-01-01T00:00:00Z'},
                     'Config': {'Image': row['Image'], 'Cmd': ['node', 'server.js'], 'Labels': {}, 'Env': []},
                     'HostConfig': {'NetworkMode': 'bridge'}, 'NetworkSettings': {'Networks': {}, 'Ports': {}}, 'Mounts': []}
        elif path.endswith('/stats'):
            value = {'read': '2026-01-01T12:00:00Z', 'cpu_stats': {'cpu_usage': {'total_usage': 1000000, 'percpu_usage': [1000000]},
                     'system_cpu_usage': 100000000, 'online_cpus': 1}, 'precpu_stats': {'cpu_usage': {'total_usage': 900000},
                     'system_cpu_usage': 90000000}, 'memory_stats': {'usage': 33554432, 'limit': 1073741824, 'stats': {}},
                     'networks': {}, 'blkio_stats': {'io_service_bytes_recursive': []}, 'pids_stats': {'current': 8}}
        elif path == '/volumes':
            value = {'Volumes': [], 'Warnings': []}
        elif path == '/system/df':
            value = {'LayersSize': 314572800, 'Images': [], 'Containers': [], 'Volumes': [], 'BuildCache': []}
        elif path.endswith('/top'):
            value = {'Titles': ['PID', 'USER', 'COMMAND'], 'Processes': [['100', 'node', 'node server.js']]}
        elif path.endswith('/logs'):
            value = b''
        else:
            value = []
        data = value if isinstance(value, bytes) else json.dumps(value).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('API-Version', '1.47')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        if self.command != 'HEAD':
            try:
                self.wfile.write(data)
            except BrokenPipeError:
                pass


def prepare(c):
    global server
    c.copy(f'themes/{c.slug}.yml', '.config/lazydocker/config.yml')
    server = ThreadingHTTPServer(('127.0.0.1', 0), DockerFixture)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    c.env['DOCKER_HOST'] = f'tcp://127.0.0.1:{server.server_port}'
    c.env['DOCKER_API_VERSION'] = '1.47'
    c.env['CONFIG_DIR'] = str(c.home / '.config/lazydocker')
    return ['lazydocker']


def drive(c):
    c.wait_text(r'Containers|glyph-api')
    if 'report' in c.text().lower() or 'Welcome' in c.text():
        c.key('esc')
    c.wait_text('glyph-api')


def cleanup(c):
    if server:
        server.shutdown()
        server.server_close()
