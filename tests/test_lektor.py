# -*- coding: utf-8 -*-

from lektor.environment import Expression
from lektor.project import Project
import pytest


@pytest.fixture
def lektor_project(tmp_path):
    site_dir = tmp_path
    project_file = site_dir / 'Test Site.lektorproject'
    project_file.write_text(
        "[project]\n"
        "name = Test Site\n"
    )
    config_file = site_dir / 'configs' / 'excerpt-html.ini'
    config_file.parent.mkdir()
    config_file.write_text("[excerpt-html]\n")
    return Project.from_path(str(site_dir))
    
    
@pytest.fixture
def lektor_env(lektor_project):
    return lektor_project.make_env(load_plugins=True)


@pytest.fixture
def eval_j2_expr(lektor_env):
    def eval(expr, **kwargs):
        return Expression(lektor_env, expr).evaluate(values=kwargs)
    return eval


def test_jinja_filter(eval_j2_expr):
    text = u"<p>Word1 <!-- more --> word2.</p>"
    assert eval_js_expr("text|excerpt_html", text=text) \
        == u"<p>Word1</p>"
