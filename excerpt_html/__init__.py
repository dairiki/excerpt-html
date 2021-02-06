# -*- coding: utf-8 -*-
"""Extract a short summary from HTML text.

"""
from itertools import chain
import re

import bs4


DEFAULT_CUT_MARK = r'(?i)\s*more\b'
DEFAULT_MIN_WORDS = 50

# These are the elements at which we'll consider truncation.
# This is, roughly, a list of HTML block-level elements, though
# few block-level elements, particularly those which are components
# of another block-level element (e.g. dd, dt, li, figcaption, fieldset)
# have been omitted.
TRUNCATABLE_ELEMENTS = set(
    '''p div main article section nav aside header footer
    address aside blockquote details pre figure hgroup table
    h1 h2 h3 h4 h5 h6 dl ol ul form'''.split())


def excerpt_html(html_text,
                 min_words=DEFAULT_MIN_WORDS,
                 cut_mark=DEFAULT_CUT_MARK):
    """Extract a summary from html text.

    This function first looks for an HTML comment whose text matches the
    regular expression **cut_mark**.  If such a comment is found, all text
    after that comment is deleted, and the result is returned.
    The truncation is done in an HTML-aware manner.  The result should be
    a valid HTML fragment: it will not contain dangling tags, etc.

    If no cut mark is found, then the text is truncated at the first
    block element such that there are at least ``min_words`` words in
    the preserved (preceding) text.

    If no suitable truncation point can be found, ``None`` is
    returned.

    Args:
        html_text: The input text, a string.
        min_words: When finding a block-level truncation point, retain
            at least this many words of the original text.  Set to
            ``None`` to disable block-level truncation.
        cut_mark: A regular expression which is to be matched against
            the text of HTML comments in ``html_text`` to find a
            truncation point.  Pass ``None`` to disable.

    Returns:
        If an acceptable truncation point is found, returns the
        truncated HTML text, as a string.  If there is no acceptable
        truncation point, returns ``None``.

    """
    soup = bs4.BeautifulSoup(html_text, 'html5lib')
    # Many of the parsers add html/body to parse result.  Get rid of that.
    if soup.html:
        soup.html.unwrap()
    while soup.head:
        soup.head.decompose()
    if soup.body:
        soup.body.unwrap()

    cut_point = None
    if cut_mark:
        cut_mark_match = re.compile(cut_mark).match

        def is_cut_mark(elem):
            return isinstance(elem, bs4.Comment) and cut_mark_match(elem)
        cut_point = soup.find(text=is_cut_mark)

    if cut_point is None and min_words:
        cut_point = _find_truncation_point(soup, min_words)

    if cut_point is None:
        return None                     # no truncation point found

    # delete everything from cut_point onwards
    lineage = chain([cut_point], cut_point.parents)
    to_delete = [cut_point]
    for elem in lineage:
        to_delete.extend(elem.next_siblings)

    def is_blank(elem):
        return (
            isinstance(elem, bs4.Comment)
            or (isinstance(elem, bs4.NavigableString) and elem.strip() == ''))

    if all(is_blank(elem) for elem in to_delete):
        # No non-blank content to delete
        return None

    for elem in to_delete:
        if hasattr(elem, 'decompose'):
            elem.decompose()
        else:
            elem.extract()

    return soup.decode()


def _find_truncation_point(soup, min_words=DEFAULT_MIN_WORDS):
    word_count = 0
    at_word_break = True
    breakable = set([soup])
    for elem in soup.descendants:
        if isinstance(elem, bs4.Comment):
            continue
        elif isinstance(elem, bs4.NavigableString):
            s = elem
            if at_word_break:
                nwords = len(s.split())
            else:
                nwords = len(('x' + s).split()) - 1
            word_count += nwords
            at_word_break = s.rstrip() != s
        elif elem.name in TRUNCATABLE_ELEMENTS:
            # Only consider truncation if all parents are
            # truncatable elements
            if elem.parent in breakable:
                if word_count >= min_words:
                    return elem
                breakable.add(elem)
            at_word_break = True
