import traceback
from resource.base_resource import BaseResource
from flask_restful import Resource, reqparse
from flasgger import swag_from

class MovieList(BaseResource):

    @swag_from('../docs/movie-list.yml')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str)
        parser.add_argument('s', type=str)
        parser.add_argument('q', type=str, required=True)
        params = parser.parse_args()
        if params['type'] == 'full':
            return self.__api_full_search(params)
        else:
            return self.__api_partial_search(params)

    def __api_full_search(self, params):
        headers = {'content-type': 'application/json'}
        keyword = params['q']
        image_size = params['s']
        self.logger.info('the parameter is given: %s', keyword)
        result = ""
        try:
            result = self.provider.search_full_list(str(keyword), str(image_size))
        except:
            traceback.print_exc()
        if result:
            return result, 200, headers
        return f'Results Not Found: {keyword}', 404, headers

    def __api_partial_search(self, params):
        headers = {'content-type': 'application/json'}
        keyword = params["q"]
        image_size = params['s']
        self.logger.info('the parameter is given: %s', keyword)
        result = ""
        try:
            result = self.provider.search_partial_list(str(keyword), str(image_size))
        except:
            traceback.print_exc()
        if result:
            return result, 200, headers
        return f'Results Not Found: {keyword}', 404, headers

class Movie(BaseResource):
    @swag_from('../docs/movie.yml')
    def get(self, sid):
        parser = reqparse.RequestParser()
        parser.add_argument('s', type=str)
        params = parser.parse_args()
        return self.__api_fetch_by_sid(sid, params)

    def __api_fetch_by_sid(self, sid, params):
        headers = {'content-type': 'application/json'}
        image_size = params['s']
        self.logger.info('the parameter is given: %s', sid)
        result = ""
        try:
            result = self.provider.fetch_detail_info(str(sid), str(image_size))
        except:
            traceback.print_exc()
        if result:
            return result, 200, headers
        return f'Results Not Found: {sid}', 404, headers

class MovieCelebrityList(BaseResource):
    @swag_from('../docs/movie-celebrity-list.yml')
    def get(self, sid):
        return self.__api_fetch_celerities_by_sid(sid)

    def __api_fetch_celerities_by_sid(self, sid):
        headers = {'content-type': 'application/json'}
        self.logger.info('the parameter is given: %s', sid)
        result = ""
        try:
            result = self.provider.fetch_celebrities(str(sid))
        except:
            traceback.print_exc()
        if result:
            return result, 200, headers
        return f'Results Not Found: {sid}', 404, headers
