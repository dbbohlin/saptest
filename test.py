import traceback, collections, sys

COMMENT = '//'

def histogram_letters(phrase):
    '''
    This will work for all python versions for Python 2.7 or better it would simply be:
        ':return collections.Counter(phrase)
    :param phrase:
    :return:
    '''
    histogram = collections.defaultdict(int)
    for letter in phrase:
        histogram[letter] += 1
    return histogram

def print_historgram(phrase, histogram):
    '''
    Print the histogram with a '#' for the count
    :param phrase:
    :param histogram:
    :return:
    '''
    print(phrase)
    keylist = histogram.keys()
    keylist.sort()
    for key, value in reversed(sorted(histogram.iteritems(), key=lambda (k,v): (v,k))):
        marker = ''
        for idx in range(0, value):
            marker +='#'
        print ('  {0}: {1}'.format(key, marker))

def histogram(phrase):
    '''
    processes the phrase into a histgram and prints it out
    :param phrase:
    :return:
    '''
    print_historgram(phrase, histogram_letters(phrase))

def parse_last_names(last_names):
    '''
    Print out full names based on length of last name, then print out names alphabetical by first names
    :param last_names:
    :return:
    '''
    print('\nPrint by last name length then first name alphabetical')
    for key, value in sorted(last_names.iteritems(), key=lambda value: (len(value[1]))):
        print('{0} {1}'.format(key, value))
    print('\nNow first name alphabetical')
    for key in sorted(last_names.iterkeys()):
        print('{0} {1}'.format(key,last_names[key]))

def is_balanced(expression):
    '''
    Check if the bracketing is balanced for a given expresssion. This only checks for "[]" and "()"
    but could be used for any number of brackets including just a single bracket set.
    :param expression:
    :return:
    '''
    openexpr = '(['
    closeexpr = ')]'
    map = dict(('()', '[]'))
    queue = []

    for bracket in expression:
        if bracket in openexpr:
            queue.append(map[bracket])
        elif bracket in closeexpr:
            if not queue or bracket != queue.pop():
                return False
    return not queue

def strip_comments(expression):
    '''
    Stripping comments out of JSON is not a good idea. Comments are not part of the JSON directive.
    JSON is meant for data only and should not require comments for parsing. If comments are required
    Then it is possible to add a data element that would be ignored during the parsing phase and could
    be used as a means of conveying instructions.

    That being said.
    A C style comment always ends a line
    A C style comment never includes multiple lines
    A C style comment always begins with //
    // can also be used in a URL or a string but will always be enclosed with a " or '
    A C style comment cannot be inside of a string
    There can be legitimate data before a C style comment but will either be a string,
        a boolean, a numeric or a bracket

    This solution will work as long as there are no string delimeter in the comment itself
    :param expression:
    :return:
    '''
    new_expression = ''
    lines = expression.split('\n')
    for line in lines:
        if COMMENT in line:
            line = process_comment(line)
        new_expression += line +'\n'
    return new_expression

def process_comment(line, offset=0):
    '''
    Process the line that has a comment string in it
    :param line:
    :param offset:
    :return:
    '''
    index = line.rfind(COMMENT)
    if (0 == index):
        return ''
    while  index > 0:
        if not check_for_string(line[index:], line[:-index]):
            line = line[:index]
        else:
            return line
        offset = index - 1
        index = line.find(COMMENT, 0, offset)
    return line

def check_for_string(comment_line, before_line):
    '''
    Check for enclosing strings before line or after
    :param comment_line:
    :param before_line:
    :return:
    '''
    if '"' in comment_line and '"' in before_line:
        return True
    elif "'" in comment_line and "'" in before_line:
        return True
    return False

if __name__ == '__main__':
    try:
        if '-h' == sys.argv[1]:
            print('test.py histogram balance_expression\nUse this program by entering the histogram phrase to be parsed in double quotes " and the bracket expression to be evalutated in double qoutes as well')
            sys.exit(0)
        histogram(sys.argv[1])
        last_names = {
            'Mary': 'Li',
            'James': "O'Day",
            'Thomas': 'Miller',
            'William': 'Garcia',
            'Elizabeth': 'Davis',
        }
        parse_last_names(last_names)
        print('\nThe expresion is balanced: {0}\n\n'.format(is_balanced(sys.argv[2])))
        json_string = '// this is a comment\n{ // another comment\n   true, "foo", // 3rd comment\n   "http://www.ariba.com" // comment after URL\n}\n'
        processed_string = strip_comments(json_string)
        print('JSON String with comments:\n{0}\nJSON String without comments:\n{1}'.format(json_string, processed_string))
    except Exception as ex:
        print('Exception occurred: {0}\n{1}'.format(ex, traceback.format_exc()))
    finally:
        pass
