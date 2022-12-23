from rest_framework.response import Response
from rest_framework import status

class Resp:
    def __init__(self, data_=None, msg_="OK", status_=True, code_=status.HTTP_200_OK, pagination_=False, previous_link_=None, next_link_=None, count_=None):
        self.status = status_
        self.msg = msg_
        self.data = data_
        self.code = code_
        self.pagination = pagination_
        self.previous_link = previous_link_
        self.next_link = next_link_
        self.count = count_

    def send(self):

        if self.pagination == True:
            result = {
            'data': self.data,
            'previous': self.previous_link,
            'next': self.next_link,
            'message': self.msg,
            "status": self.status,
            "count": self.count,
        }
        else:
            result = {
                'data': self.data,
                'message': self.msg,
                "status": self.status,
            }
        return Response(result, status=self.code)

    def result(self):
        return {
            'data': self.data,
            'message': self.msg,
            "status": self.status,
        }
