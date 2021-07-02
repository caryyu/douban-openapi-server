import traceback
from resource.base_resource import BaseResource
from flasgger import swag_from

class Celebrity(BaseResource):
    @swag_from('../docs/celebrity.yml')
    def get(self, cid):
        headers = {'content-type': 'application/json'}
        self.logger.info('the parameter is given: %s', cid)
        result = ""
        try:
            result = self.provider.fetch_celebrity_detail(str(cid))
        except:
            traceback.print_exc()
        if result:
            return result, 200, headers
        return f'Results Not Found: {cid}', 404, headers

