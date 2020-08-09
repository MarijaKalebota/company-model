import functools

from django.core import serializers
from django.db import IntegrityError, transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader

from . import models


def index(request):
    return HttpResponse("Hello, world. You're at the index.")

def node_api(request, node_id):
    try:
        node = models.Node.objects.get(id=node_id)
    except models.Node.DoesNotExist as e:
        return HttpResponse("Object does not exist", status=404)
    if request.method == "GET":
        return JsonResponse(node.to_dict())
    elif request.method == "POST":
        new_parent_id = request.POST.get("new_parent_id")
        try:
            node.set_parent(new_parent_id)
        except (models.Node.DoesNotExist, ValueError) as e:
            return HttpResponse(f"Updating parent was unsucessful. Error: {str(e)}", status=400)
        return JsonResponse(node.to_dict())
    else:
        return HttpResponse("Unsupported operation", status=400)


def node_gui(request, node_id):
    try:
        node = models.Node.objects.get(id=node_id)
    except models.Node.DoesNotExist as e:
        return HttpResponse("Object does not exist", status=404)

    if request.method == "GET":
        template = loader.get_template("company_model_manager/nodes.html")
        context = {"node": node}
        return HttpResponse(template.render(context, request))
    elif request.method == "POST":
        new_parent_id = request.POST.get("new_parent_id")
        try:
            node.set_parent(new_parent_id)
        except (models.Node.DoesNotExist, ValueError) as e:
            return HttpResponse(f"Updating parent was unsucessful. Error: {str(e)}", status=400)
        context = {"node": node}
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse("Unsupported operation", status=400)


def get_descendants_api(request, node_id):
    try:
        node = models.Node.objects.get(id=node_id)
    except models.Node.DoesNotExist as e:
        return HttpResponse("Object does not exist", status=404)
    descendants = node.get_descendants()
    return JsonResponse(
        {"descendants": [descendant.to_dict() for descendant in descendants]},
    )


def get_descendants_gui(request, node_id):
    try:
        node = models.Node.objects.get(id=node_id)
    except models.Node.DoesNotExist as e:
        return HttpResponse("Object does not exist", status=404)
    descendants = node.get_descendants()

    template = loader.get_template("company_model_manager/descendants.html")
    context = {
        "descendants": descendants,
        "node_id": node_id,
    }
    return HttpResponse(template.render(context, request))
