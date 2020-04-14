# -*- coding: utf-8 -*-

import pytest

from excerpt_html import excerpt_html


@pytest.mark.parametrize('html_text, kwargs, expected_excerpt', [
    # test cut mark
    ((u'<p>Howdy there<!--more--> you <em>pretty</em> thing!</p>'
      u'<p>Another paragraph</p>'),
     {},
     u'<p>Howdy there</p>'),
    # cut mark at end
    (u'<p>Howdy there<p><!--more--> ',
     {'min_words': 1},
     None),
    # excerpt blocks
    (u'<div><p>Howdy there</p><p>P2</p></div>',
     {'min_words': 1},
     u'<div><p>Howdy there</p></div>'),
    # excerpt blocks with heading
    (u'<h3>Head</h3><p>Howdy</p><p>there</p>',
     {'min_words': 2},
     u'<h3>Head</h3><p>Howdy</p>'),
    # Non-default cut mark
    (u'<p>A<!--cut-->b</p>',
     {'cut_mark': 'cut'},
     u'<p>A</p>'),
    # Unicode cut mark
    (u'<p>A<!-- cüt -->b</p>',
     {'cut_mark': u'.*ü'},
     u'<p>A</p>'),
    # No truncation point found
    (u'<p>A b</p>',
     {'min_words': 2},
     None),
    # Ignores comments
    (u'<!-- x y z  --><p>A b</p><p>C d</p>',
     {'min_words': 2},
     u'<!-- x y z  --><p>A b</p>'),
    # Continue word
    (u'<p>A<i>b</i></p><p>C</p><p>D</p>',
     {'min_words': 2},
     u'<p>A<i>b</i></p><p>C</p>'),
    # Should not break up a list
    (u'<ul><li>one two</li><li><p>three</p></li></ul>',
     {'min_words': 2},
     None),
    # Can break list with explicit break
    (u'<ul><li>one two</li><!-- more --><li><p>three</p></li></ul>',
     {},
     u'<ul><li>one two</li></ul>'),
    # Probably should not allow explict break to create empty elements,
    # but for now... well, you get what you ask for.
    pytest.param(
        u'<ul><li>one two</li><li><p><!-- more -->three</p></li></ul>',
        {},
        u'<ul><li>one two</li></ul>',
        marks=pytest.mark.xfail),
    ])
def test_excerpt_html(html_text, kwargs, expected_excerpt):
    result = excerpt_html(html_text, **kwargs)
    assert result == expected_excerpt
