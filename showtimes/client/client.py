import grpc
import showtimes_pb2
import showtimes_pb2_grpc


def get_showtimes(stub):
    showtimes = stub.GetShowtimes(showtimes_pb2.Empty)
    return showtimes


def run():
    with grpc.insecure_channel('localhost:5000') as channel:
        stub = showtimes_pb2_grpc.ShowtimesStub(channel)

        print("-------------- GetShowtimes --------------")
        showtimes = get_showtimes(stub)
        print(showtimes)


if __name__ == '__main__':
    run()