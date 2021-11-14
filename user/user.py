from flask import Flask, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound
import grpc

import movie_pb2
import movie_pb2_grpc
import booking_pb2
import booking_pb2_grpc

app = Flask(__name__, template_folder='../templates')

PORT = 3000
HOST = '127.0.0.1'
localhost = '172.17.0.1'
URLS = {
    "booking": "localhost:3002",
    "movie": "localhost:3001",
}

with open('{}/database/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Users service!</h1>", 200)

# return an array containing user’s bookings
def user_bookings(user_id):
    with grpc.insecure_channel(URLS["booking"]) as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        bookings = stub.GetBookingsByUserID(booking_pb2.UserID(id=user_id))
        
        ans = []
        
        for booking in bookings.dates:
            movies = [] 
            
            for id in booking.movies:
                movies.append({"id": id, "title": movie_title(id)})
            
            ans.append({"date": booking.date, "movies": movies})
            
        return ans

def movie_title(movie_id):
    with grpc.insecure_channel(URLS["movie"]) as channel:
        stub = movie_pb2_grpc.MovieStub(channel)
        movie = stub.GetMovieByID(movie_pb2.MovieID(id=movie_id))
        return movie.title

# get the complete json file
@app.route("/users", methods=['GET'])
def get_users():
    users_with_bookings = []
    
    for user in users:
        user["bookings"] = user_bookings(user["id"])
            
        users_with_bookings.append(user)
    
    return make_response(jsonify(users), 200)

# return an user specified by his id
@app.route("/users/<userid>", methods=['GET'])
def get_user_by_id(userid):
    matching_users = [user for user in users if user["id"] == userid]
    if len(matching_users) == 0:
        return make_response(jsonify({"error": "user ID not found"}), 400)
    else:
        return matching_users[0]

# add a new user
@app.route("/users/<userid>", methods=["POST"])
def create_user(userid):
    req = request.get_json()
    req["id"] = userid

    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify({"error": "user ID already exists"}), 409)

    users.append(req)
    return make_response(jsonify(req), 200)

# delete an user
@app.route("/users/<userid>", methods=["DELETE"])
def del_movie(userid):
    try:
        user = next(user for user in users if user['id'] == userid)
    except StopIteration:
        return make_response(jsonify({"error": "user ID not found"}), 400)
    else:
        users.remove(user)
        return make_response(jsonify(user), 200)

# change an user last active
@app.route("/users/<userid>/<lastactive>", methods=["PUT"])
def update_user_last_active(userid, lastactive):
    try:
        user = next(user for user in users if user['id'] == userid)
    except StopIteration:
        return make_response(jsonify({"error": "user ID not found"}), 201)
    else:
        user["lastactive"] = int(lastactive)
        return make_response(jsonify(user), 200) 

if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    localhost = '127.0.0.1'
    app.run(host=HOST, port=PORT)
