from flask import Flask, g, request
from proxypool.storages.redis import RedisClient
from proxypool.setting import API_HOST, API_PORT, API_THREADED, PROXY_SCORE_MAX, PROXY_SCORE_MIN


__all__ = ['app']

app = Flask(__name__)


def get_conn():
    """
    get redis client object
    :return:
    """
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    """
    get home page, you can define your own templates
    :return:
    """
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    """
    get a random proxy
    :return: get a random proxy
    """
    conn = get_conn()
    return conn.random().string()


@app.route('/delete')
def delete_proxy():
    """
    delete a proxy
    :return:
    """
    proxy = request.args.get("proxy", None)
    if not proxy:
        return {'code': 'nullProxy'}
    conn = get_conn()
    if not conn.delete(proxy):
        return {'code': 'notExistsProxy'}
    return {'code': 'SUCCESS'}


@app.route('/all')
def get_proxy_all():
    """
    get a random proxy
    :return: get a random proxy
    """
    conn = get_conn()
    proxies = conn.all()
    proxies_string = ''
    for proxy in proxies:
        proxies_string += str(proxy) + '\n'

    return proxies_string


@app.route('/count')
def get_count():
    """
    get the count of proxies
    :return: count, int
    """
    min = request.args.get("min", PROXY_SCORE_MIN)
    max = request.args.get("max", PROXY_SCORE_MAX)
    conn = get_conn()
    return str(conn.count(min, max))


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)
