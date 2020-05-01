import logging

class Logger:
    def __init__(self, destination_ids=[]):
        logging.basicConfig(
            filename="bot.log",
            level=logging.INFO,
            format="%(asctime)s|%(levelname)s:%(message)s"
            )

        self._destination_ids = tuple(destination_ids)

    ##### TODO  # Needs tying to the client and handlers creating for logging
