# -*- coding: utf-8 -*-

from excerpt_html import excerpt_html as _excerpt_html
from excerpt_html import (
    DEFAULT_CUT_MARK,
    DEFAULT_MIN_WORDS,
    )
from lektor.pluginsystem import Plugin
from markupsafe import (
    escape,
    Markup,
    )


_marker = object()


class ExcerptHtmlPlugin(Plugin):
    name = "Excerpt HTML"
    description = u"Provides a jinja filter to compute excerpts of HTML text."

    def on_setup_env(self, **extra):
        self.env.jinja_env.filters.update({
            'excerpt_html': self.excerpt_html,
            })

    def excerpt_html(self, text, min_words=_marker, cut_mark=_marker):
        if min_words is _marker:
            min_words = self.get_config().get_int(
                "excerpt_html.min_words", DEFAULT_MIN_WORDS)
        if cut_mark is _marker:
            cut_mark = self.get_config().get(
                "excerpt_html.cut_mark", DEFAULT_CUT_MARK)

        html_text = escape(text)
        result = _excerpt_html(html_text, min_words, cut_mark)
        if result is None:
            return text         # no truncation point found
        return Markup(result)
