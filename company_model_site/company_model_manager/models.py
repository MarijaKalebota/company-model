import functools
import json

from django.db import IntegrityError, models, transaction


class Node(models.Model):
    root = models.ForeignKey(
        "Node", on_delete=models.DO_NOTHING, blank=True, null=True, related_name="+"
    )
    parent = models.ForeignKey(
        "Node", on_delete=models.DO_NOTHING, blank=True, null=True, related_name="+"
    )
    height = models.BigIntegerField()

    @classmethod
    def insert(cls, parent_id=None):
        """
        Create a node in the tree. If the parent is not passed (None), then
        the nodei s considered the root node. There can only be one root node,
        and an exception will be raised (ValuError) if this is not true.
        """
        if parent_id == None:
            created, node = cls.insert_root()
        else:
            created, node = cls.insert_node(parent_id)

        return created, node

    @classmethod
    def insert_root(cls):
        """
        Inserts the root node if possible. Returns a tuple (created, root),
        where created is a bool flag indiciated has the root node been created.
        """
        if cls.objects.exists():
            return False, None

        root = cls(root=None, parent=None, height=0,)
        try:
            with transaction.atomic():
                root.save()
                root.root = root
                root.save()
                return True, root
        except IntegrityError:
            return False, None

    @classmethod
    def insert_node(cls, parent_id):
        """
        Insert a non root node and attach it to the parent node. If this 
        method is called while there is no root node or the parent node id
        does not exist, it will not insert the node.

        The method returns a tuple (created, node) - where created is a bool
        flag indicated has the node been created, and the node is a refernece
        to the node if it has been created, otherwise it is None.
        """
        parent = cls.objects.get(id=parent_id)
        if parent is None:
            return False, None

        node = cls(root=cls.get_root(), parent=parent, height=parent.height + 1,)
        node.save()
        return True, node

    @classmethod
    @functools.lru_cache()
    def get_root(cls):
        """
        Returns the root node if it exists, otherwise returns None.
        """
        if not cls.objects.exists():
            return None

        # TODO Check if the root actually exists
        return cls.objects.get(parent=None)

    @classmethod
    def is_node_among_descendants(cls, top_node, node_to_find):
        """
        Checks whether a node is among descendants of a given top node.
        """
        if not cls.objects.filter(parent=top_node):
            return False
        else:
            nodes_to_check = [top_node]

            while len(nodes_to_check) != 0:
                node = nodes_to_check.pop(0)
                children = cls.objects.filter(parent=node)
                for child in children:
                    if child.id == node_to_find.id:
                        return True
                    else:
                        nodes_to_check.append(child)
            return False

    def set_parent(self, parent_id):
        """
        Set a new parent if possible and return flag indicating
        if the new parent has been set.
        """
        new_parent = Node.objects.get(id=parent_id)
        if self.is_node_among_descendants(self, new_parent):
            return False

        self.parent = new_parent
        self.save()
        return True

    def get_descendants(self):
        """
        Run BFS to get all descendant nodes.
        """
        # TODO request?
        # TODO arguments into docstring
        # TODO invalid node id
        descendants = []
        nodes_to_check = [self]

        while len(nodes_to_check) != 0:
            node = nodes_to_check.pop(0)
            children = Node.objects.filter(parent=node)
            for child in children:
                nodes_to_check.append(child)
                descendants.append(child)

        return descendants

    def to_dict(self):
        return {
            "id": str(self.id),
            "parent": str(self.parent.id) if self.parent else str(None),
            "root": str(self.root.id),
            "height": str(self.height),
        }
