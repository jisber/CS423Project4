import sys

import engine


def handle_command(command_line):
    '''
    This function handles the argument flags and takes in the function parameters in any order given
    :param command_line: list of arguments
    :return: returns the commands in the order they need to be
    '''

    # Temporary list
    temp_list = []

    # Pre-made list than can hold the 4 arguments
    commands = ['', '', '', '']

    for i in command_line:
        temp_list.append(i)

    if '-mode' not in temp_list:
        print("ERROR: Missing required arguments",file=sys.stderr)
        exit(1)
    elif '-root' not in temp_list:
        print("ERROR: Missing required arguments", file=sys.stderr)
        exit(1)

    for i, val in enumerate(temp_list):

        if val == '-root':
            commands[0] = temp_list[i + 1]
            if not parseLink(commands[0]):
                print("ERROR: Link '" + commands[0] + "' is in the incorrect format. The link must start with 'http' "
                                                      "or 'https'.", file=sys.stderr)
                exit(1)
        elif val == '-mode':
            commands[1] = temp_list[i + 1]
            commands[1] = commands[1].lower()
            if commands[1] != 'c' and commands[1] != 'i':
                print("ERROR: Mode: '" + commands[1].upper() + "' is not supported, please use 'C' or 'I'. ",
                      file=sys.stderr)
                exit(1)

        elif val == '-query':
            commands[2] = temp_list[i + 1]

        elif val == '-verbose':
            commands[3] = temp_list[i + 1]
            commands[3] = commands[3].lower()
            if commands[3] != 't' and commands[3] != 'f':
                print("ERROR: Mode: '" + commands[3].upper() + "' is not supported, please use 'T' or 'F'. ",
                      file=sys.stderr)
                exit(1)

    if commands[1] == 'c':
        if "-query" not in temp_list:
            print("ERROR: Missing query arguments", file=sys.stderr)
            exit(1)
    elif commands[1] == 'i':
        if "-verbose" not in temp_list:
            print("ERROR: Missing verbose arguments", file=sys.stderr)
            exit(1)

    return commands


def parseLink(link):
    """
    Parses the link provided to check if it is valid
    :param link: string
    :return: true if link is valid else return false
    """
    expected_string = link[:5]
    if "http" in expected_string:
        return True
    elif "https" in expected_string:
        return True
    else:
        return False


if __name__ == "__main__":
    commands = handle_command(sys.argv)

    root = commands[0]
    mode = commands[1]
    query = commands[2]
    verbose = commands[3]

    search_engine = engine.SearchEngine(root, mode, query, verbose, 0)
    search_engine.start()
