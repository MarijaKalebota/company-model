from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError, transaction

import functools

from . import models

def index(request):
    return HttpResponse("Hello, world. You're at the index.")

def insert_root(request):
    # query DB. If result set is empty, create root
    #if len(models.Node.objects.all()) == 0:
    if not models.Node.objects.exists():
        root = models.Node(
            root = None,
            parent = None,
            height = 0,
        )
        try:
            with transaction.atomic():
                print("Entered transaction")
                root.save()
                print("Saved")
                root.root = root
                root.save()
                return HttpResponse("Root created.", status=201)
        except IntegrityError:
            return HttpResponse("Transaction unsuccessful, please try again.", status=400)
    else:
        return HttpResponse("Root already exists.", status=400)

@functools.lru_cache()
def get_root():
    if models.Node.objects.exists():
        try:
            return models.Node.objects.get(parent=None)
        #except Entry.DoesNotExist:
        except:
            # TODO 
            return None
    else:
        # TODO
        return None
    
def insert_node(request, parent_id):
    # query DB to check if given parent exists
    parent = models.Node.objects.get(id=parent_id)
    if parent is not None:
        parent_height = parent.height
        new_node = models.Node(
            root = get_root(),
            parent = parent,
            height = parent_height + 1,
        )
        new_node.save()
        return HttpResponse("Node inserted.")
    else:
        return HttpResponse("Node with provided ID does not exist.")

def get_descendant_nodes(node_id):
    '''
    Run BFS to get all descendants.
    '''
    # TODO request?
    # TODO arguments into docstring
    # TODO invalid node id
    descendants = []
    node = models.Node.objects.get(id=node_id)
    nodes_to_check = [node]

    while len(nodes_to_check) != 0:
        node = nodes_to_check.pop(0)
        children = models.Node.objects.filter(parent=node)
        for child in children:
            nodes_to_check.append(child)
            descendants.append(child)
    
    return descendants

def get_descendants(request, node_id):
    descendant_nodes = get_descendant_nodes(node_id)
    descendants = []

    for descendant_node in descendant_nodes:
        descendant = {
            'id': str(descendant_node.id),
            'parent': str(descendant_node.parent.id),
            'root': str(descendant_node.root.id),
            'height': str(descendant_node.height),
        }
        descendants.append(descendant)
    
    response_data = {
        'descendants': descendants,
    }

    return JsonResponse(response_data)

def is_node_among_descendants(top_node, node_to_find):
    if not models.Node.objects.filter(parent=top_node):
        return False
    else:
        nodes_to_check = [top_node]

        while len(nodes_to_check) != 0:
            node = nodes_to_check.pop(0)
            children = models.Node.objects.filter(parent=node)
            for child in children:
                if child.id == node_to_find.id:
                    return True
                else:
                    nodes_to_check.append(child)
        return False

def set_parent(request, node_id, new_parent_id):
    # TODO cover edge cases
    # TODO requests
    node = models.Node.objects.get(id=node_id)
    old_parent_id = node.parent.id
    new_parent = models.Node.objects.get(id=new_parent_id)
    if is_node_among_descendants(node, new_parent):
        return HttpResponse("Illegal operation")
    else:
        node.parent = new_parent
        node.save()
        return HttpResponse("Node with ID: " + str(node_id) + " parent set from " + str(old_parent_id) + " to " + str(new_parent_id))
