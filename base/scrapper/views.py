from rest_framework.decorators import api_view
from .utils.utils import scrap_items
from rest_framework.response import Response
import json


@api_view(["POST"])
def get_prods(request):
    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    prods = scrap_items(*body.values())
    return Response(prods)
