from flask_restful import Resource, reqparse

class Movies(Resource):
    provider = None
    logger = None

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.provider = kwargs.get('provider')
        self.logger = kwargs.get('logger')

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str)
        parser.add_argument('q', type=str, required=True)
        params = parser.parse_args()
        print(params)
        if params['type'] == 'full':
            return self.__api_full_search(params)
        else:
            return self.__api_partial_search(params)

    def __api_full_search(self, params):
        headers = {'content-type': 'application/json'}
        keyword = params['q']
        self.logger.info('the parameter is given: %s', keyword)
        result = ""
        try:
            result = self.provider.search_full_list(str(keyword))
        except Exception as ex:
            print(ex)
        if result:
            return result, 200, headers
        return f'Results Not Found: {keyword}', 404, headers

    def __api_partial_search(self, params):
        headers = {'content-type': 'application/json'}
        keyword = params["q"]
        self.logger.info('the parameter is given: %s', keyword)
        result = ""
        try:
            result = self.provider.search_partial_list(str(keyword))
        except Exception as ex:
            print(ex)
        if result:
            return result, 200, headers
        return f'Results Not Found: {keyword}', 404, headers
