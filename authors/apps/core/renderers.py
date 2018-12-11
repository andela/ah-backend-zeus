import json
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework.renderers import JSONRenderer


class AuthorsJSONRenderer(JSONRenderer):
    """
    Renderer class for Authors
    """

    charset = 'utf-8'
    object_label = 'object'
    object_label_plural = 'objects'

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, ReturnList):
            _data = json.loads(
                super(AuthorsJSONRenderer, self).render(data).decode('utf-8')
            )

            return json.dumps({
                self.object_label_plural: _data
            })
        else:
            # If the view throws an error (such as the user can't be authenticated)
            # `data` will contain an `errors` key. We want
            # the default JSONRenderer to handle rendering errors, so we need to
            # check for this case.
            return json.dumps({
                self.object_label: data
            })
