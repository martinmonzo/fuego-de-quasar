from rest_framework.exceptions import APIException


class BaseAction(object):

    def __init__(self, request, **kwargs):
        self.request = request
        try:
            self.validate(**kwargs)
            self.run()
        except Exception as ex:
            raise APIException(ex)

    def validate(self):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()