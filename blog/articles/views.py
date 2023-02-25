from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

article = Blueprint('article', __name__, url_prefix='/articles',
                    static_folder='../static')

ARTICLES = {
    1: 'Biology',
    2: 'Anatomy',
    3: 'Astronomy',
}


@article.route('/')
def article_list():
    return render_template('articles/list.html', articles=ARTICLES)


@article.route('/<int:pk>')
def get_article(pk: int):
    try:
        article_name = ARTICLES[pk]
    except KeyError:
        raise NotFound(f'Статья c id {pk} не найдена')
    return render_template('articles/details.html', article_name=article_name)
