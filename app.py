import json

from flask import Flask
from flask import request
from flask_caching import Cache

from provider.httprequest_provider import HttpRequestProvider

provider = HttpRequestProvider()
app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app, config={'CACHE_TYPE': 'simple'})

@app.route('/search', methods=['GET'])
# @cache.cached(timeout=30, query_string=True)
def api_search():
    return api_full_search()

@app.route('/fullsearch', methods=['GET'])
# @cache.cached(timeout=30, query_string=True)
def api_full_search():
    headers = {'content-type': 'application/json'}
    keyword = request.args.get("q")
    app.logger.info('the parameter is given: %s', keyword)
    result = ""
    try:
        obj = provider.search_full_list(str(keyword))
        result = json.dumps(obj, ensure_ascii=False)
    except Exception as ex:
        print(ex)
    if result:
        return result, 200, headers
    return f'Results Not Found: {keyword}', 404, headers

@app.route('/partialsearch', methods=['GET'])
# @cache.cached(timeout=30, query_string=True)
def api_partial_search():
    headers = {'content-type': 'application/json'}
    keyword = request.args.get("q")
    app.logger.info('the parameter is given: %s', keyword)
    result = ""
    try:
        obj = provider.search_partial_list(str(keyword))
        result = json.dumps(obj, ensure_ascii=False)
    except Exception as ex:
        print(ex)
    if result:
        return result, 200, headers
    return f'Results Not Found: {keyword}', 404, headers

@app.route('/fetchbysid', methods=['GET'])
# @cache.cached(timeout=30, query_string=True)
def api_fetch_by_sid():
    headers = {'content-type': 'application/json'}
    sid = request.args.get("sid")
    app.logger.info('the parameter is given: %s', sid)
    result = ""
    try:
        obj = provider.fetch_detail_info(str(sid))
        result = json.dumps(obj, ensure_ascii=False)
    except Exception as ex:
        print(ex)
    if result:
        return result, 200, headers
    return f'Results Not Found: {sid}', 404, headers

@app.route('/fetchceleritiesbysid', methods=['GET'])
# @cache.cached(timeout=30, query_string=True)
def api_fetch_celerities_by_sid():
    headers = {'content-type': 'application/json'}
    sid = request.args.get("sid")
    app.logger.info('the parameter is given: %s', sid)
    result = ""
    try:
        obj = provider.fetch_celebrities(str(sid))
        result = json.dumps(obj, ensure_ascii=False)
    except Exception as ex:
        print(ex)
    if result:
        return result, 200, headers
    return f'Results Not Found: {sid}', 404, headers

if __name__ == "__main__":
    app.run()

