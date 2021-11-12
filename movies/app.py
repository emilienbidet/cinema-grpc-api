import json
import grpc
from concurrent import futures
import movie_pb2
import movie_pb2_grpc
from flask import jsonify


class MovieServicer(movie_pb2_grpc.MovieServicer):
    def __init__(self):
        with open('{}/databases/movies.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["movies"]

    def GetMovieByID(self, request, context):
        for movie in self.db:
            if movie['id'] == request.id:
                print("Movie found!")
                return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'],
                                           id=movie['id'])
        return movie_pb2.MovieData(title="", rating="", director="", id="")

    def GetListMovies(self, request, context):
        for movie in self.db:
            yield movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'],
                                      id=movie['id'])

    def CreateMovie(self, request, context):
        if request:
            newMovie = {
                "title": request.title,
                "rating": request.rating,
                "director": request.director,
                "id": request.id
            }
            self.db.append(newMovie)
        return movie_pb2.Result(message="The film has been added.")

    def UpdateMovieRating(self, request, context):
        if request:
            for movie in self.db:
                if str(movie["id"]) == str(request.id):
                    movie["rating"] = float(request.rating)
                    return movie_pb2.Result(message="The rating has been modified.")
        return movie_pb2.Result(message="The film cannot be found.")

    def DeleteMovie(self, request, context):
        if request:
            for movie in self.db:
                if str(movie["id"]) == str(request.id):
                    self.db.remove(movie)
                    return movie_pb2.Result(message="The movie has been removed.")

        return movie_pb2.Result(message="The film cannot be found.")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    movie_pb2_grpc.add_MovieServicer_to_server(MovieServicer(), server)
    server.add_insecure_port('[::]:5000')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
