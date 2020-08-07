from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError, transaction

import functools

from . import models

def index(request):
    return HttpResponse("Hello, world. You're at the index.")

def insert_root():
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
                root.save()
                root.root = root.id
                root.save()
                return HttpResponse("Root created.", status=201)
        except IntegrityError:
            return HttpResponse("Transaction unsuccessful, please try again.", status=400)
    else:
        return HttpResponse("Root already exists.", status=400)

@functools.lru_cache()
def get_root_id():
    if models.Node.objects.exists():
        try:
            return models.Node.objects.get(id=root)
        except Entry.DoesNotExist:
            # TODO 
            return None
    else:
        # TODO
        return None
    
def insert_node(parent_id):
    # query DB to check if given parent exists
    parent = models.Node.objects.get(id=parent_id)
    if parent is not None:
        parent_height = parent.height
        new_node = models.Node(
            root = get_root_id(),
            parent = parent_id,
            height = parent_height + 1,
        )
    return

def get_descendants(request, node_id, descendants):
    '''
    Run BFS to get all descendants.
    '''
    # TODO request?
    # TODO arguments into docstring
    descendants = []
    node = models.Node.objects.get(id=node_id)
    nodes_to_check = [node]

    while len(nodes_to_check) != 0:
        node = nodes_to_check.pop(0)
        children = node.parent_set.objects.all()
        for child in children:
            nodes_to_check.append(child)
            descendants.append(child)
    
    return descendants

def is_node_among_descendants(top_node, node_to_find):
    if not top_node.parent_set.objects.exists():
        return False
    else:
        nodes_to_check = [top_node]

        while len(nodes_to_check) != 0:
            node = nodes_to_check.pop(0)
            children = node.parent_set.objects.all()
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
    new_parent = models.Node.objects.get(id=new_parent_id)
    if is_node_among_descendants(node, new_parent):
        return "Illegal operation"
    else:
        node.parent = new_parent
        return
