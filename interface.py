class SearchInterface():
    def __init__(self, mode, engine, query):
        """
        Default constructor
        :param mode: The mode
        :param engine: A pointer to SearchEngine
        :param query: The query that the user inputes
        """
        self.mode = mode
        self.engine = engine
        self.query = query

    def listen(self):
        """
        Listin is called at the start of the program and is the main way a user interacts with the program
        :return: None
        """
        if self.mode == 'c':
            self.engine.handle_query(self.query)
        elif self.mode == 'i':
            print("----------------------------------")
            print("|         UTK EECS SEARCH        |")
            print("__________________________________")
            while 1:
                print('> ', end='')
                var = input()
                self.handle_input(var)

    def handle_input(self, var):
        """
        Handles inputes from listen()
        :param var: Command
        :return: None
        """
        if var == ':exit':
            self.engine.exit()
        elif var == ':train':
            self.engine.train()
        elif var == ':delete':
            self.engine.delete()
        else:
            self.engine.handle_query(var)