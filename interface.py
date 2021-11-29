# Jacob Isber
# File:
# Desc:


class SearchInterface():
    def __init__(self, mode, engine, query):
        self.mode = mode
        self.engine = engine
        self.query = query

    def listen(self):
        if self.mode == 'c' and self.query != '':
            self.engine.handel_query(self.query)
        elif self.mode == 'i':
            print("----------------------------------")
            print("|         UTK EECS SEARCH        |")
            print("__________________________________")
            while 1:
                var = input()
                self.handle_input(var)

    def handle_input(self, var):
        if var == ':exit':
            self.engine.exit()
        elif var == ':train':
            self.engine.train()
        elif var == ':delete':
            self.engine.delete()
        else:
            self.engine.handle_query(var)