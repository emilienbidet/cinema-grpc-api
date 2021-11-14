import json
import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc


class BookingServicer(booking_pb2_grpc.BookingServicer):
    def __init__(self):
        with open('{}/database/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetBookings(self, request, context):
        for booking in self.db:
            yield booking_pb2.BookingObject(userid=booking['userid'], dates=booking['dates'])

    def GetBookingsByUserID(self, request, context):
        try:
            booking = next(booking for booking in self.db if booking['userid'] == request.id)
        except StopIteration:
            print("User not found!")
            return booking_pb2.BookingObject(userid="", dates=[])
        else:
            print("User found!")
            return booking_pb2.BookingObject(userid=booking['userid'], dates=booking['dates'])

    def AddBookingByUserID(self, request, context):
        with grpc.insecure_channel('localhost:3003') as channel :
            stub = showtime_pb2_grpc.ShowtimeStub(channel)
            showtime = stub.GetMoviesByDate(showtime_pb2.MovieDate(date=request.date))
            
            try:
                movie = next(movie for movie in showtime.movies if request.movieid == movie)
            except StopIteration:
                print("Movie does not exist in the showtime")
                return booking_pb2.BookingObject(userid="", dates=[])
            else:
                print("Movie exists in the showtime")
                try:
                    selected_booking = next(booking for booking in self.db if booking['userid'] == request.userid)
                except StopIteration:
                    selected_booking = {"userid": request.userid, "dates": []}
                    self.db.append(selected_booking)
                
                try:
                    selected_time = next(time for time in selected_booking['dates'] if time['date'] == request.date)
                except StopIteration:
                    selected_time = {"date": request.date, "movies": []}
                    selected_booking["dates"].append(selected_time)
                finally:
                    # Let assume that an user can book the same movie several time a day
                    selected_time["movies"].append(request.movieid)
                    print("Booking added")
            
                answer = booking_pb2.BookingObject(userid=selected_booking["userid"])
                for time in selected_booking["dates"]:
                    answer.dates.append(booking_pb2.BookingObject.BookingDate(date=time["date"], movies=time["movies"]))
                return answer


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
