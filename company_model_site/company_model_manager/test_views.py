from company_model_manager import models
from django.test import Client, TestCase


class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_nodes_without_specifing_id(self):
        response = self.client.get("/company_model_manager/api/v1/nodes/")
        assert response.status_code == 404

    def test_node_api_get(self):
        created, root = models.Node.insert()
        assert created is True

        response = self.client.get(f"/company_model_manager/api/v1/nodes/{root.id}/")
        assert response.status_code == 200

        true_root = {
            "id": str(1),
            "parent": str(None),
            "root": str(1),
            "height": str(0),
        }
        assert response.json() == true_root

    def test_node_gui_get(self):
        created, root = models.Node.insert()
        assert created is True

        response = self.client.get(f"/company_model_manager/nodes/{root.id}/")
        assert response.status_code == 200

        response_content = response.content.decode("utf-8")
        assert f"/company_model_manager/nodes/{root.id}/" in response_content
        assert f"Node {root.id}" in response_content

    def test_empty_descendants_api_get(self):
        created, root = models.Node.insert()
        assert created is True

        response = self.client.get(
            f"/company_model_manager/api/v1/nodes/{root.id}/descendants/"
        )
        assert response.status_code == 200

        descendants = response.json()["descendants"]
        assert len(descendants) == 0

    def test_multiple_descendants_api_get(self):
        _, root = models.Node.insert()
        _, node1a = models.Node.insert(root.id)
        _, node2a = models.Node.insert(node1a.id)

        response = self.client.get(
            f"/company_model_manager/api/v1/nodes/{root.id}/descendants/"
        )
        assert response.status_code == 200

        descendants = response.json()["descendants"]
        assert len(descendants) == 2
