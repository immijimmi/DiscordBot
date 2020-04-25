import logging

class Logger:
    def __init__(self, client, destination_ids=[]):
        self.destination_ids = tuple(destination_ids)

        self.client = client

    ##### TODO