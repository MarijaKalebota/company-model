from company_model_manager import models
from django.test import Client, TestCase


def populate_db_with_nodes():
    _, root = models.Node.insert()
    _, node1a = models.Node.insert(root.id)
    _, node1b = models.Node.insert(root.id)
    _, node2a = models.Node.insert(node1b.id)

    return root, node1a, node1b, node2a


class NodeModelTests(TestCase):
    def test_get_descendant_of_root(self):
        root, node1a, node1b, node2a = populate_db_with_nodes()

        descendants = root.get_descendants()
        descendant_node_ids = [descendant.id for descendant in descendants]

        assert len(descendants) == 3

        assert node1a.id in descendant_node_ids
        assert node1b.id in descendant_node_ids
        assert node2a.id in descendant_node_ids

    def test_root_hight(self):
        root, node1a, node1b, node2a = populate_db_with_nodes()

        assert root.height == 0

    def test_level_1_hegith(self):
        root, node1a, node1b, node2a = populate_db_with_nodes()

        assert node1a.height == 1

    def test_get_descendant_nodes_one_level(self):
        root, node1a, node1b, node2a = populate_db_with_nodes()

        assert len(node2a.get_descendants()) == 0

    def test_insert_root_node(self):
        assert len(models.Node.objects.all()) == 0

        created, root = models.Node.insert()

        assert created is True
        assert len(models.Node.objects.all()) == 1
        assert root.parent is None
        assert root.height == 0

    def test_to_node_dict(self):
        _, root = models.Node.insert()

        true_root = {
            "id": str(1),
            "parent": str(None),
            "root": str(1),
            "height": str(0),
        }

        assert true_root == root.to_dict()

    def test_insert_non_root_node(self):
        _, root = models.Node.insert()
        created, node1 = models.Node.insert(root.id)

        assert len(models.Node.objects.all()) == 2
        assert created is True

        assert node1.parent == root

    def test_insert_invalid_non_root_node(self):
        _, root = models.Node.insert()
        created, node1 = models.Node.insert()

        assert len(models.Node.objects.all()) == 1
        assert created is False
