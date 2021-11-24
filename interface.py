# Jacob Isber
# File:
# Desc:


class SearchInterface():
    def __init__(self, mode, engine, query):
        self.mode = mode
        self.engine = engine
        self.query = query

    def listen(self):
        pass

    def handle_input(self):
        pass

    def test(self):
        self.engine.start(self)
