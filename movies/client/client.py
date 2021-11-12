import grpc
import movie_pb2
import movie_pb2_grpc


def get_movie_by_id(stub, id):
    movie = stub.GetMovieByID(id)
    print(movie)


def get_list_movies(stub):
    allmovies = stub.GetListMovies(movie_pb2.Empty())
    for movie in allmovies:
        print("Movie called %s" % (movie.title))


def create_movie(stub, movie):
    res = stub.CreateMovie(movie)
    print(res)

def update_movie_rating(stub, movie):
    res = stub.UpdateMovieRating(movie)
    print(res)

def delete_movie(stub,movie):
    res = stub.DeleteMovie(movie)
    print(res)


def run():
    with grpc.insecure_channel('localhost:5000') as channel:
        stub = movie_pb2_grpc.MovieStub(channel)

        print("-------------- GetMovieByID --------------")
        movieid = movie_pb2.MovieID(id="a8034f44-aee4-44cf-b32c-74cf452aaaae")
        get_movie_by_id(stub, movieid)
        print("-------------- GetListMovies --------------")
        get_list_movies(stub)

        print("-------------- CreateMovie --------------")
        movie = movie_pb2.MovieData(title="titre", rating=0, director="Mot", id="test")
        create_movie(stub, movie)

        print("-------------- Update movie rating --------------")
        movieRating = movie_pb2.MovieRating(id="720d006c-3a57-4b6a-b18f-9b713b073f3c", rating=0.0)
        update_movie_rating(stub,movieRating)

        print("-------------- Remove Movie --------------")
        movieId = movie_pb2.MovieID(id="720d006c-3a57-4b6a-b18f-9b713b073f3c")
        delete_movie(stub, movieId)


if __name__ == '__main__':
    run()
