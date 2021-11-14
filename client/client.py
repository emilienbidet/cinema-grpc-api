import grpc

import movie_pb2
import movie_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc
import booking_pb2
import booking_pb2_grpc

def runMovie():
    with grpc.insecure_channel('localhost:3001') as channel:
        stub = movie_pb2_grpc.MovieStub(channel)
        
        print("—————————————— GetMovieByID ——————————————")
        movieid = movie_pb2.MovieID(id = "a8034f44-aee4-44cf-b32c-74cf452aaaae")
        get_movie_by_id(stub, movieid)
        
        print("—————————————— AddMovie ——————————————")
        new_movie_id = "a8034f44-aee4-44cf-b32c-74cf452abcde"
        new_movie = movie_pb2.MovieData(title="Ad Astra", rating=6.5, director="James Gray", id=new_movie_id)
        add_movie(stub, new_movie)
        
        print("—————————————— GetMovieByTitle ——————————————")
        title = movie_pb2.MovieTitle(title="Ad Astra")
        get_movie_by_title(stub, title)
        
        print("—————————————— PutMovieRateById ——————————————")
        rate = movie_pb2.MovieIDRate(id=new_movie_id, rate=5)
        put_movie_rate_by_id(stub, rate)
        
        print("—————————————— PatchMovieTitle ——————————————")
        title = movie_pb2.MovieIDTitle(id=new_movie_id, title="Astram ad")
        patch_movie_title(stub, title)
        
        print("—————————————— DeleteMovieById ——————————————")
        delete_movie(stub, movie_pb2.MovieID(id=new_movie_id))
        
        print("—————————————— GetListMovies ——————————————")
        get_list_movies(stub)
        
def runShowtime():
    with grpc.insecure_channel('localhost:3003') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)
        
        print("—————————————— GetSchedule ——————————————")
        get_schedule(stub)
        
        print("—————————————— GetMoviesByDate——————————————")
        get_movies_by_date(stub, showtime_pb2.MovieDate(date="20151130"))
    
def runBooking():
    with grpc.insecure_channel('localhost:3002') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        
        print("—————————————— GetBookings ——————————————")
        get_bookings(stub)

        print("—————————————— AddBookingByUserID ——————————————")
        userid = "michael_scott"
        new_booking = booking_pb2.SingleBooking(date="20151130" , userid=userid, movieid="a8034f44-aee4-44cf-b32c-74cf452aaaae")
        add_booking_by_user_id(stub, new_booking)
        
        print("—————————————— GetBookingsByUserID ——————————————")
        get_bookings_by_user_id(stub, booking_pb2.UserID(id=userid))

def get_movie_by_id(stub,id):
    movie = stub.GetMovieByID(id)
    print(movie)
    
def get_list_movies(stub):
    allmovies = stub.GetListMovies(movie_pb2.Empty())
    for movie in allmovies:
        print("Movie called %s" % (movie.title))
        
def get_movie_by_title(stub, title):
    movie = stub.GetMovieByTitle(title)
    print(movie)
    
def add_movie(stub, movie):
    added_movie = stub.AddMovie(movie)
    print("Added\n")
    
def delete_movie(stub, id):
    delete_movie = stub.DeleteMovieByID(id)
    print("Deleted\n")
    
def put_movie_rate_by_id(stub, rate):
    modified_movie = stub.PutMovieRateByID(rate)
    print(modified_movie)

def patch_movie_title(stub, title):
    modified_movie = stub.PatchMovieTitle(title)
    print(modified_movie)
    
def get_schedule(stub):
    schedule = stub.GetSchedule(showtime_pb2.EmptySchedule())
    
    for time in schedule:
        print(time.date)
        
        for movie in time.movies:
            print("- {}".format(movie))
        
        print('\n')

def get_movies_by_date(stub, date):
    time = stub.GetMoviesByDate(date)
    
    print(time.date)
    for movie in time.movies:
        print("- {}".format(movie))
    
    print('\n')

def get_bookings(stub):
    all_bookings = stub.GetBookings(booking_pb2.EmptyBooking())
    for booking in all_bookings:
        print(booking)    
    
def get_bookings_by_user_id(stub, userid):
    booking = stub.GetBookingsByUserID(userid)
    print(booking)

def add_booking_by_user_id(stub, booking):
    added_booking = stub.AddBookingByUserID(booking)
    print(added_booking)

if __name__ == '__main__':
    runMovie()
    runShowtime()
    runBooking()
