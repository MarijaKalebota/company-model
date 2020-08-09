from django.test import Client, TestCase

from .models import Node
from .views import insert_node, get_descendant_nodes

def insert_root():
    root = Node(
        root = None,
        parent = None,
        height = 0,
    )
    root.save()
    root.root = root
    root.save()
    return root

def get_root():
    return Node.objects.get(parent=None)


def populate_db_with_nodes():
    insert_root()
    root = get_root()
    test_node_2 = Node(
        root = root,
        parent = root,
        height = 1,
    )
    test_node_2.save()
    test_node_3 = Node(
        root = root,
        parent = root,
        height = 1,
    )
    test_node_3.save()
    test_node_4 = Node(
        root = root,
        parent = test_node_2,
        height = 2,
    )
    test_node_4.save()

class NodeModelTests(TestCase):

    def setUp(self):
        self.client = Client()
        populate_db_with_nodes()
    
    def test_get_descendant_nodes_empty(self):
        assert len(get_descendant_nodes(4)) == 0
    
    def test_get_descendant_nodes_one_level(self):
        assert len(get_descendant_nodes(3)) == 1

    def test_get_descendant_nodes_multiple_levels(self):
        root = Node.objects.get(id=1)
        descendant_nodes = get_descendant_nodes(root.id)
        descendant_node_ids = [descendant_node.id for descendant_node in descendant_nodes]
        assert len(descendant_node_ids) == 3 and 2 in descendant_node_ids and 3 in descendant_node_ids and 4 in descendant_node_ids
