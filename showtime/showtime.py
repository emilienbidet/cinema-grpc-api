import json
import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc


class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):
    def __init__(self):
        with open('{}/database/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    def GetSchedule(self, request, context):
        for time in self.db:
            date = showtime_pb2.MovieDate(date=time['date'])
            movies = [id for id in time['movies']]
            
            yield showtime_pb2.ScheduleObject(date=date, movies=movies)

    def GetMoviesByDate(self, request, context):
        try:
            time = next(time for time in self.db if time['date'] == request.date)
        except StopIteration:
            print("Movies not found!")
            return showtime_pb2.ScheduleObject()
        else:
            print("Movies found!")
            date = showtime_pb2.MovieDate(date=time['date'])
            movies = [id for id in time['movies']]
            
            return showtime_pb2.ScheduleObject(date=date, movies=movies)        


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3003')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
