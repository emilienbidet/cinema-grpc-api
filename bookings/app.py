import json
import grpc
from concurrent import futures
import bookings_pb2
import bookings_pb2_grpc
from flask import jsonify


class BookingServicer(bookings_pb2_grpc.BookingsServicer):
    def __init__(self):
        with open('{}/databases/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetBookings(self, request, context):
        test = []
        for booking in self.db:
            test += bookings_pb2.BookingObject(userid=booking["user"],
                                             dates=booking["dates"])
        return test

    def GetBookingByUserID(self, request, context):
        for booking in self.db:
            if booking["userid"] == request.userid:
                return bookings_pb2.BookingObject(userid=booking["userid"],dates=booking["dates"])
        return bookings_pb2.BookingObject(userid="", dates=[])

    def AddBookingByUserID(self, request, context):
        userid = request.userid
        date = request.date
        movieid = request.movieid
        


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bookings_pb2_grpc.add_BookingsServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:5000')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
