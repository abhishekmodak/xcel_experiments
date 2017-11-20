"""This script creates short form from Full Name"""

def abbrev():
    """To make abbreviation of the name."""

    entered_string = 'mahendra singh dhoni'
    splitted_name = entered_string.split()
    result = ''
    for item in splitted_name[:-1]:
        result += item[0] + ' '
    result += splitted_name[-1]

    result = result.title()
    result = result.replace(' ', '.')

    print result


abbrev()
