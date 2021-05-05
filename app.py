from flask import Flask
from flask import request
from index import *

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def api_search():
    return api_full_search()

@app.route('/fullsearch', methods=['GET'])
def api_full_search():
    headers = {'content-type': 'application/json'}
    keyword = request.args.get("q")
    app.logger.info('the parameter is given: %s', keyword)
    result = delegator_try_except_driver(service_keyword_full_search, str(keyword))
    if result:
        return result, 200, headers
    return f'Results Not Found: {keyword}', 404, headers

@app.route('/partialsearch', methods=['GET'])
def api_partial_search():
    headers = {'content-type': 'application/json'}
    keyword = request.args.get("q")
    app.logger.info('the parameter is given: %s', keyword)
    result = delegator_try_except_driver(service_keyword_partial_search, str(keyword))
    if result:
        return result, 200, headers
    return f'Results Not Found: {keyword}', 404, headers

@app.route('/fetchbysid', methods=['GET'])
def api_fetch_by_sid():
    headers = {'content-type': 'application/json'}
    sid = request.args.get("sid")
    app.logger.info('the parameter is given: %s', sid)
    result = delegator_try_except_driver(service_info_fetch_by_sid, str(sid))
    if result:
        return result, 200, headers
    return f'Results Not Found: {sid}', 404, headers

if __name__ == "__main__":
    app.run()

