import re
import argparse
import sys
from markovchain import SqliteStorage
from markovchain.text import MarkovText, ReplyMode, RegExpScanner, Formatter

MALAYALAM_EXPR = re.compile(
    r'(?:(?P<end>[.!?]+)|(?P<word>(?:[\S]+|\w+)))'
)
MALAYALAM_REPLACE = [
    (r'\s+', r' '),
    (r'\s*([^\S]+)\s*', r'\1'),
    (r'([,.?!])(\w)', r'\1 \2'),
    (r'([\w,.?!])([[({<])', r'\1 \2'),
    (r'([])}>])(\w)', r'\1 \2'),
    (r'(\w)([-+*]+)(\w)', r'\1 \2 \3'),
]


class MalayalamMarkov:
    def __init__(self, input_db=None, output_db=None):
        malayalam_scanner = RegExpScanner(expr=MALAYALAM_EXPR)
        malayalam_formatter = Formatter(replace=MALAYALAM_REPLACE)
        if input_db:
            storage = SqliteStorage(db=input_db)
        elif output_db:
            storage = SqliteStorage(db=output_db)
        self.markov = MarkovText(
            scanner=malayalam_scanner, formatter=malayalam_formatter, storage=storage)

    def add_text(self, text):
        if text:
            self.markov.data(text)

    def predict(self, start, words, count):
        results=[]
        for i in range(count):
            results.append(self.markov(max_length=words,
                              reply_to=start, reply_mode=ReplyMode.END))
        return results
    def save(self):
        self.markov.save()

    def from_db(self, db_filename):
        storage = SqliteStorage(db=db_filename)
        self.markov = MarkovText.from_storage(storage)


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Malayalam Markov Chain"
    )
    parser.add_argument(
        "-i",
        "--infile",
        metavar="INPUT.txt",
        default=sys.stdin,
        help="Input text file containing words",
        nargs="?",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        metavar="OUTPUT.db",
        help="Output file for saving the model",
        default="malayalam.db",
        nargs="?",
    )
    parser.add_argument(
        "-d",
        "--database",
        metavar="malayalam.db",
        help="Database containing markov model",
        nargs="?",
    )
    parser.add_argument(
        "-s",
        "--start",
        help="Predict the next word(s) for this prompt",
        nargs="?",
    )
    parser.add_argument(
        '-w', '--words',
        type=int, default=8,
        help='Number of words in generated sentence (default: %(default)s)'
    )
    parser.add_argument(
        '-c', '--count',
        type=int, default=1,
        help='Number of generated texts (default: %(default)s)'
    )
    return parser.parse_args(args)


def main(args=None):
    options = parse_args(args)
    mlmarkov = MalayalamMarkov(input_db=options.database, output_db=options.outfile)
    if options.start:
        results = mlmarkov.predict(options.start, options.words, options.count)
        print(results)
    else:
        with options.infile as fp:
            mlmarkov.add_text(fp.read())
        mlmarkov.save()


if __name__ == "__main__":
    sys.exit(main())
