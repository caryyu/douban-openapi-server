from resource.base_resource import BaseResource

class Celebrity(BaseResource):
    def get(self, cid):
        headers = {'content-type': 'application/json'}
        self.logger.info('the parameter is given: %s', cid)
        result = ""
        try:
            result = self.provider.fetch_celebrity_detail(str(cid))
        except Exception as ex:
            print(ex)
        if result:
            return result, 200, headers
        return f'Results Not Found: {cid}', 404, headers

