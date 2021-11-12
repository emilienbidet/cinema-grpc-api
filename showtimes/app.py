import json
import grpc
from concurrent import futures
import showtimes_pb2
import showtimes_pb2_grpc
from flask import jsonify


class ShowtimeServicer(showtimes_pb2_grpc.ShowtimesServicer):
    def __init__(self):
        with open('{}/databases/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    def GetShowtimes(self, request, context):
        for showtime in self.db:
            yield showtimes_pb2.ShowtimeData(date=showtime["date"], movies=showtime["movies"])

        


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtimes_pb2_grpc.add_ShowtimesServicer_to_server(ShowtimeServicer, server)
    server.add_insecure_port('[::]:5000')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
