from flask import Flask,g

from Myobject.proxypool.db import Reids_Client

__all__=['app']
app = Flask(__name__)
def get_conn():
    if not hasattr(g,'reids_client'):
        g.redis_client = Reids_Client()
    return g.redis_client

@app.route('/')
def index():
    return '<h1>欢迎来到代理池系统！</h1>'
@app.route('/get')
def get():
    conn = get_conn()
    proxy = conn.pop()
    if isinstance(proxy,bytes):
        return proxy.decode('utf-8')
    return proxy
@app.route('/count')
def count():
    return str(get_conn().queue_len)