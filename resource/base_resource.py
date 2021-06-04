from flask_restful import Resource

class BaseResource(Resource):
    provider = None
    logger = None

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.provider = kwargs.get('provider')
        self.logger = kwargs.get('logger')

