from company_model_manager import models
from django.test import Client, TestCase


def insert_root():
    root = models.Node(root=None, parent=None, height=0,)
    root.save()
    root.root = root
    root.save()
    return root


def get_root():
    return models.Node.objects.get(parent=None)


def populate_db_with_test_nodes():
    insert_root()
    root = get_root()

    test_node_2 = models.Node(root=root, parent=root, height=1,)
    test_node_2.save()

    test_node_3 = models.Node(root=root, parent=root, height=1,)
    test_node_3.save()

    test_node_4 = models.Node(root=root, parent=test_node_2, height=2,)
    test_node_4.save()

    return root, test_node_2, test_node_3, test_node_4


class NodeModelTests(TestCase):
    def test_get_descendant_of_root(self):
        root, test_node_2, test_node_3, test_node_4 = populate_db_with_test_nodes()

        descendants = root.get_descendants()
        descendant_node_ids = [descendant.id for descendant in descendants]

        assert len(descendants) == 3

        assert test_node_2.id in descendant_node_ids
        assert test_node_3.id in descendant_node_ids
        assert test_node_4.id in descendant_node_ids

    def test_root_height(self):
        root, test_node_2, test_node_3, test_node_4 = populate_db_with_test_nodes()

        assert root.height == 0

    def test_level_1_height(self):
        root, test_node_2, test_node_3, test_node_4 = populate_db_with_test_nodes()

        assert test_node_2.height == 1

    def test_get_descendant_nodes_one_level(self):
        root, test_node_2, test_node_3, test_node_4 = populate_db_with_test_nodes()

        assert len(test_node_4.get_descendants()) == 0

    def test_insert_root_node(self):
        assert len(models.Node.objects.all()) == 0

        created, root = models.Node.insert()

        assert created is True
        assert len(models.Node.objects.all()) == 1
        assert root.parent is None
        assert root.height == 0

    def test_node_to_dict(self):
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

    def test_modify_parent(self):
        root, test_node_2, test_node_3, test_node_4 = populate_db_with_test_nodes()
        assert test_node_4.parent == test_node_2
        test_node_4.set_parent(test_node_3.id)
        assert test_node_4.parent == test_node_3

    def test_modify_parent_and_update_self_and_descendants_heights(self):
        root, test_node_2, test_node_3, test_node_4 = populate_db_with_test_nodes()
        test_node_5 = models.Node(root=root, parent=test_node_4, height=3)
        test_node_5.save()

        test_node_6 = models.Node(root=root, parent=test_node_5, height=4)
        test_node_6.save()
        test_node_5.set_parent(root.id)
        assert test_node_5.height == 1
        test_node_6 = models.Node.objects.get(id=6)
        assert test_node_6.height == 2
