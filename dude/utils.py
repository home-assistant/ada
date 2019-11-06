"""Utils for Dude."""


def divide_chunks(array, chunk_size):
    for i in range(0, len(array) / chunk_size + 1):
        yield array[i : i + chunk_size]

