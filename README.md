# Excerpt HTML

[![PyPI version](https://img.shields.io/pypi/v/excerpt-html.svg)](https://pypi.org/project/excerpt-html/)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/excerpt-html.svg)](https://pypi.python.org/pypi/excerpt-html/)
[![GitHub license](https://img.shields.io/github/license/dairiki/excerpt-html)](https://github.com/dairiki/excerpt-html/blob/master/LICENSE)
[![GitHub Actions (Tests)](https://github.com/dairiki/excerpt-html/workflows/Tests/badge.svg)](https://github.com/dairiki/excerpt-html)

This distribution provides a single function, `excerpt_html` whose
purpose is to extract leading portions of HTML text.  This is useful,
for example, in order to be able to generate a summary of a blog post
from the post body.

**`excerpt_html(html_text, min_words=50, cut_mark=r'(?i)\s*more\b')`**

The `excerpt_html` function expects, as input, HTML text, and returns
a shortened version of that HTML text.  The truncation point is found
in one of two ways:

- If an explicit _cut-mark_ — an HTML comment whose text matches
    **cut_mark** — is found, the text will be truncated there.

- If no explicit cut-mark is found, an attempt will be made to find a
    suitable implicit truncation point.  Only points which
    are not within in-line markup are considered.  The text will be
    truncated at the first such location found which preserves at
    least **min_words** (by default, 50) words of text.

In either case, the returned excerpt will always be a syntactically
valid HTML fragment.

**Arguments**:

- `html_text`: The input text, a string containing an HTML fragment.

- `min_words`: When finding a block-level truncation point, retain at
    least this many words of the original text.  Pass `None` to
    disable block-level truncation.

- `cut_mark`: A regular expression which is to be matched against the
    text of HTML comments in `html_text` to find a truncation point.
    This is matched using `re.match()` against the contents of HTML
    comments.  This should be either a compiled regular expression or a
    string; or `None` to disable cut-mark recognition.

**Returns**:

If a truncation point was found, a string containing the excerpt, a semantically valid HTML fragment, is returned.

If no suitable truncation point was found, `None` is returned.


## Installation

The package is installable via _pip_.

```sh
pip install excerpt-html
```

## Example

Here are two paragraphs worth of HTML, with an explicit *cut-mark* in the middle
of the first paragraph.

```pycon
>>> from excerpt_html import excerpt_html

>>> post_body = '''
... <p>
... In a sense, the subject is interpolated into a neotextual
... narrative that includes culture as a paradox.
... <!-- more -->
... A number of deconceptualisms concerning substructural
... construction exist.
... </p>
... <p>
... However, the subject is contextualised into a postmaterial
... discourse that includes sexuality as a totality. Sontag uses
... the term ‘cultural narrative’ to denote not, in fact,
... deconstruction, but predeconstruction.
... </p>'''

```

By default, the text will be truncated at the cut mark:

```pycon
>>> summary = excerpt_html(post_body)
>>> print(summary)
<p>
In a sense, the subject is interpolated into a neotextual
narrative that includes culture as a paradox.
</p>

```

If we disable _cut_mark_ recognition, there is no suitable implicit
truncation point which will preserve at least 50 words (the default
value of _min_words_):

```pycon
>>> summary = excerpt_html(post_body, cut_mark=None)

>>> summary is None
True

```

If we a lower value for _min_words_, the break between paragraphs will be
selected as a truncation point:

```pycon
>>> summary = excerpt_html(post_body, min_words=10, cut_mark=None)

>>> print(summary)          # doctest: +NORMALIZE_WHITESPACE
<p>
In a sense, the subject is interpolated into a neotextual
narrative that includes culture as a paradox.
<!-- more -->
A number of deconceptualisms concerning substructural
construction exist.
</p>

```

## Links

Development takes place at [GitHub][].  Releases may be downloaded from [PyPI][].

[GitHub]: <https://github.com/dairiki/excerpt-html/>
[PyPI]: <https://pypi.org/projects/excerpt-html/>


## Author

Jeff Dairiki <dairiki@dairiki.org>
