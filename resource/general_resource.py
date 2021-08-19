# Anything that's unrelated to the media resources can be put here
import traceback
from resource.base_resource import BaseResource
from flasgger import swag_from

class PhotoList(BaseResource):
    @swag_from('../docs/photo-list.yml')
    def get(self, sid):
        headers = {'content-type': 'application/json'}
        self.logger.info('the parameter is given: %s', sid)
        result = ""
        try:
            result = self.provider.fetch_wallpaper(str(sid))
            return result, 200, headers
        except:
            traceback.print_exc()
        return f'Results Not Found: {sid}', 404, headers

