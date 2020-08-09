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
    node = models.Node.objects.get(id=node_id)
    if request.method == "GET":
        # return HttpResponse(serializers.serialize('json', [node]))
        return JsonResponse(node.to_dict())
    elif request.method == "POST":
        new_parent_id = request.POST.get("new_parent_id")
        node.set_parent(new_parent_id)
        # return HttpResponse(serializers.serialize('json', [node]))
        return JsonResponse(node.to_dict())
    else:
        return HttpResponse("Unsupported operation", status=400)


def node_gui(request, node_id):
    if request.method == "GET":
        node = models.Node.objects.get(id=node_id)
        template = loader.get_template("company_model_manager/nodes.html")
        context = {"node": node}
        return HttpResponse(template.render(context, request))
    elif request.method == "POST":
        new_parent_id = request.POST.get("new_parent_id")
        node.set_parent(new_parent_id)
        context = {"node": node}
        return HttpResponse(template.render(context, request))
    # TODO implement DELETE
    else:
        return HttpResponse("Unsupported operation", status=400)


def get_descendants_api(request, node_id):
    node = models.Node.objects.get(id=node_id)
    descendants = node.get_descendants()
    # return HttpResponse(serializers.serialize('json', descendants))
    return JsonResponse(
        {"descendants": [descendant.to_dict() for descendant in descendants]},
    )


def get_descendants_gui(request, node_id):
    node = models.Node.objects.get(id=node_id)
    descendants = node.get_descendants()

    template = loader.get_template("company_model_manager/descendants.html")
    context = {
        "descendants": descendants,
        "node_id": node_id,
    }
    return HttpResponse(template.render(context, request))


def set_parent(request, node_id, new_parent_id):
    # TODO cover edge cases - when trying to set parent of root, etc.
    # TODO requests
    node = models.Node.objects.get(id=node_id)
    old_parent_id = node.parent.id
    new_parent = models.Node.objects.get(id=new_parent_id)
    if models.Node.is_node_among_descendants(node, new_parent):
        return HttpResponse("Illegal operation")
    else:
        node.parent = new_parent
        node.save()
        response = f"Node with ID: {str(node_id)} parent set from {str(old_parent_id)} to {str(new_parent_id)}"
        return HttpResponse(response)
