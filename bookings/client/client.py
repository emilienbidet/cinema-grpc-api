import grpc
import bookings_pb2
import bookings_pb2_grpc


def get_bookings(stub):
    bookings = stub.GetBookings(bookings_pb2.Empty())
    return bookings


def run():
    with grpc.insecure_channel('localhost:5000') as channel:
        stub = bookings_pb2_grpc.BookingsStub(channel)

        print("-------------- GetBookings --------------")
        bookings = get_bookings(stub)
        print(bookings)


if __name__ == '__main__':
    run()