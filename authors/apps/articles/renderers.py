from authors.apps.core.renderers import AuthorsJSONRenderer


class ArticleJSONRenderer(AuthorsJSONRenderer):
    """
    This class calls the renderers.py in the Core app 
    to fetch and format error data for 
    all articles or a single article
    """

    object_label = 'article'
    object_label_plural = 'articles'
