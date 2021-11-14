import json
import grpc
from concurrent import futures
import movie_pb2
import movie_pb2_grpc

class MovieServicer(movie_pb2_grpc.MovieServicer):
    def __init__(self):
        with open('{}/database/movies.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["movies"]
            
    def GetMovieByID(self, request, context):
        try:
            movie = next(movie for movie in self.db if movie['id'] == request.id)
        except StopIteration:
            return movie_pb2.MovieData(title="", rating=0.0, director="", id="")
        else:
            print("Movie found!")
            return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
    
    def GetMovieByTitle(self, request, context):
        try:
            movie = next(movie for movie in self.db if movie['title'] == request.title)
        except StopIteration:
            return movie_pb2.MovieData(title="", rating=0.0, director="", id="")
        else:
            print("Movie found!")
            return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
    
    def GetListMovies(self, request, context):
        for movie in self.db:
            yield movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
    
    def AddMovie(self, request, context):
        """ Renvoie l’élément ajouté """
        id = request.id
        title = request.title
        rating = request.rating
        director = request.director

        try:
            movie = next(movie for movie in self.db if movie['id'] == id)
        except StopIteration:
            newMovie = {"id": id, "title": title, "director": director, "rating": rating}
            self.db.append(newMovie)
            return movie_pb2.MovieData(title=title, rating=rating, director=director, id=id)
        else:
            return movie_pb2.MovieData(title="", rating=0.0, director="", id="")        

    def DeleteMovieByID(self, request, context):
        """ On renvoie l’élément supprimé. """
        try:
            movie = next(movie for movie in self.db if movie['id'] == request.id)
        except StopIteration:
            return movie_pb2.MovieData(title="", rating=0, director="", id="")
        else:
            self.db.remove(movie)
            return movie_pb2.MovieData(title=movie["title"], rating=movie["rating"], director=movie["director"], id=movie["id"])        
    
    def PutMovieRateByID(self, request, context):
        """ On renvoie l'élément modifié. """
        try:
            movie = next(movie for movie in self.db if movie['id'] == request.id)
        except StopIteration:
            return movie_pb2.MovieData(title="", rating=0, director="", id="")
        else:
            movie["rating"] = request.rate   
            return movie_pb2.MovieData(title=movie["title"], rating=movie["rating"], director=movie["director"], id=movie["id"])
    
    def PatchMovieTitle(self, request, context):
        """ On renvoie l'élément modifié. """
        try:
            movie = next(movie for movie in self.db if movie['id'] == request.id)
        except StopIteration:
            return movie_pb2.MovieData(title="", rating=0, director="", id="")
        else:
            movie["title"] = request.title
            return movie_pb2.MovieData(title=movie["title"], rating=movie["rating"], director=movie["director"], id=movie["id"])
        
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    movie_pb2_grpc.add_MovieServicer_to_server(MovieServicer(), server)
    server.add_insecure_port('[::]:3001')
    server.start()
    server.wait_for_termination()
    
if __name__ == '__main__':
    serve()
