from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError, transaction

from . import models

# Create your views here.



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
        #TODO return 404
        return HttpResponse("Root already exists.", status=400)

def insert_node(parent_id):
    # query DB to check if given parent exists
    parent = models.Node.objects.get(id=parent_id)
    if parent is not None:
        parent_height = parent.height
        new_node = models.Node(
            root = GLOBAL_ROOT,
            parent = parent_id,
            height = parent_height + 1,
        )
    return

def get_descendants(request, node_id):
    # TODO implement
    return

def set_parent(request, node_id, new_parent_id):
    # TODO implement
    # check if new_parent.height <= node.height. If not, abort
    return
