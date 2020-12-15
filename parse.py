#!/usr/bin/env python3
import sys
import json, argparse
import html
import wikipediaapi

from html.parser import HTMLParser

class WikiHTML(HTMLParser):
    rendered = ""
    skip = False

    RESET = '\x1B[23m'
    ITALIC = '\x1B[3m'
    BOLD = '\033[1m'

    def handle_starttag(self, tag, attrs):
        if self.skip:
            return

        if tag == "i":
            self.rendered += self.ITALIC

        # FIXME this is dumb and you should feel bad
        elif tag == "h1":
            self.rendered += "\n# "
        elif tag == "h2":
            self.rendered += "\n## "
        elif tag == "h3":
            self.rendered += "\n### "
        elif tag == "h4":
            self.rendered += "\n#### "

        if tag == "math":
            self.skip = True
            self.rendered += "$"
            for (key, val) in attrs:
                if key == 'alttext':
                    self.rendered += val
                    return

    def handle_endtag(self, tag):
        if tag == "math":
            self.rendered += "$"
            self.skip = False

        if tag == "i":
            self.rendered += self.RESET
        elif tag == "h1" or tag == "h2" or tag == "h3" or tag == "h4" or tag == "h4":
            self.rendered += "\n"

        if self.skip:
            return

    # handle any data (`test` in `<p>test</p>`)
    def handle_data(self, data):
        if self.skip:
            return
        # do not manipulate data
        self.rendered += data

    def get_rendered(self):
        return self.rendered

if __name__ == "__main__":
    # collect CLI args
    parser = argparse.ArgumentParser(description='Command line client for Wikipedia.')
    parser.add_argument('page', metavar='PAGE', type=str, nargs='+', help='Name of page')
    args = parser.parse_args()

    PAGE_NAME = ' '.join(map(str, args.page))

    # access through API
    PAGE_HTML = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.HTML
    ).page(PAGE_NAME).text

    # parse
    parser = WikiHTML()
    parser.feed(PAGE_HTML)

    print(parser.get_rendered())
