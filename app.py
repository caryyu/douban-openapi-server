from flask import Flask
from flask import request
from index import *

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def api_search():
    headers = {'content-type': 'application/json'}
    keyword = request.args.get("q")
    app.logger.info('the parameter is given: %s', keyword)
    result = func_delegate_try_except_driver(func_keyword_search, str(keyword))
    if result:
        return result, 200, headers
    return f'Results Not Found: {keyword}', 404, headers

if __name__ == "__main__":
    app.run()

