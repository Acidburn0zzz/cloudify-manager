#########
# Copyright (c) 2015 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.
#

from nose.plugins.attrib import attr

from manager_rest.test.base_list_test import BaseListTest


@attr(client_min_version=1, client_max_version=1)
class TestResourceListV1(BaseListTest):
    """
    REST list operations have changed in v2. This test class assures v1
    backwards compatibility has been preserved.
    """

    def setUp(self):
        super(TestResourceListV1, self).setUp()
        (self.first_blueprint_id,
         self.first_deployment_id,
         self.sec_blueprint_id,
         self.sec_deployment_id) = self._put_two_test_deployments()

    def test_blueprints_list_no_params(self):
        response = self.get('/blueprints', query_params=None).json
        self.assertEqual(2, len(response), 'expecting 2 blueprint result,'
                                           ' got {0}'.format(len(response)))
        for blueprint in response:
            self.assertIn(blueprint['id'],
                          (self.first_blueprint_id, self.sec_blueprint_id))
            self.assertIsNotNone(blueprint['plan'])

    def test_blueprints_list_with_params(self):
        response = self.get('/blueprints', query_params=None).json
        self.assertEqual(2, len(response), 'expecting 2 blueprint result,'
                                           ' got {0}'.format(len(response)))
        for blueprint in response:
            self.assertIn(response[0]['id'],
                          (self.first_blueprint_id, self.sec_blueprint_id))
            self.assertIsNotNone(blueprint['plan'])

    def test_deployments_list_no_params(self):
        response = self.get('/deployments', query_params=None).json
        self.assertEqual(2, len(response), 'expecting 2 deployment results, '
                                           'got {0}'.format(len(response)))

        if response[0]['id'] != self.first_deployment_id:
            response[0], response[1] = response[1], response[0]

        self.assertEquals(self.first_blueprint_id,
                          response[0]['blueprint_id'])
        self.assertEquals(self.sec_blueprint_id,
                          response[1]['blueprint_id'])

    def test_deployments_list_with_filters(self):
        filter_fields = {'id': self.first_deployment_id,
                         'blueprint_id': self.first_blueprint_id}
        response = self.get('/deployments', query_params=filter_fields).json

        self.assertEqual(2, len(response), 'filter should not be applied, '
                                           'expecting 2 results, got {0}'
                         .format(len(response)))

    def test_nodes_list_no_params(self):
        response = self.get('/nodes', query_params=None).json
        self.assertEqual(4, len(response), 'expecting 4 node results, '
                                           'got {0}'.format(len(response)))
        for node in response:
            self.assertIn(node['deployment_id'],
                          (self.first_deployment_id, self.sec_deployment_id))
            self.assertIn(node['blueprint_id'],
                          (self.first_blueprint_id, self.sec_blueprint_id))

    def test_nodes_list_with_params(self):
        params = {'deployment_id': self.first_deployment_id}
        response = self.get('/nodes', query_params=params).json
        self.assertEqual(2, len(response), 'expecting 1 node result, '
                                           'got {0}'.format(len(response)))
        for node in response:
            self.assertEquals(node['deployment_id'], self.first_deployment_id)
            self.assertEquals(node['blueprint_id'], self.first_blueprint_id)

    def test_executions_list_no_params(self):
        response = self.get('/executions', query_params=None).json
        self.assertEqual(2, len(response), 'expecting 2 executions results, '
                                           'got {0}'.format(len(response)))
        for execution in response:
            self.assertIn(execution['deployment_id'],
                          (self.first_deployment_id, self.sec_deployment_id))
            self.assertIn(execution['blueprint_id'],
                          (self.first_blueprint_id, self.sec_blueprint_id))
            self.assertEquals(execution['status'], 'terminated')

    def test_executions_list_with_params(self):
        params = {'deployment_id': self.first_deployment_id}
        response = self.get('/executions', query_params=params).json
        self.assertEqual(1, len(response), 'expecting 1 executions result, '
                                           'got {0}'.format(len(response)))
        for execution in response:
            self.assertIn(execution['deployment_id'],
                          (self.first_deployment_id, self.sec_deployment_id))
            self.assertIn(execution['blueprint_id'],
                          (self.first_blueprint_id, self.sec_blueprint_id))
            self.assertEquals(execution['status'], 'terminated')

    def test_node_instances_list_no_params(self):
        response = self.get('/node-instances', query_params=None).json
        self.assertEqual(4, len(response), 'expecting 4 node instance results,'
                                           ' got {0}'.format(len(response)))
        for node_instance in response:
            self.assertIn(node_instance['deployment_id'],
                          (self.first_deployment_id, self.sec_deployment_id))
            self.assertEquals(node_instance['state'], 'uninitialized')

    def test_node_instances_list_with_params(self):
        params = {'deployment_id': self.first_deployment_id}
        response = self.get('/node-instances', query_params=params).json
        self.assertEqual(2, len(response), 'expecting 2 node instance results,'
                                           ' got {0}'.format(len(response)))
        for instance in response:
            self.assertEquals(instance['deployment_id'],
                              self.first_deployment_id)

    # special parameter 'node_name' is converted to 'node_id' on the server
    def test_node_instances_list_with_node_name_filter(self):
        filter_params = {'node_name': 'http_web_server'}
        response = self.get('/node-instances', query_params=filter_params).json
        self.assertEqual(2, len(response), 'expecting 1 node instance result,'
                                           ' got {0}'.format(len(response)))
        for node_instance in response:
            self.assertIn(node_instance['deployment_id'],
                          (self.first_deployment_id, self.sec_deployment_id))
            self.assertEquals(node_instance['state'], 'uninitialized')

    def test_deployment_modifications_list_no_params(self):
        self._put_two_deployment_modifications()
        response = self.get('/deployment-modifications',
                            query_params=None).json
        self.assertEqual(2, len(response), 'expecting 2 deployment mod '
                                           'results, got {0}'
                         .format(len(response)))
        for modification in response:
            self.assertIn(modification['deployment_id'],
                          (self.first_deployment_id, self.sec_deployment_id))
            self.assertIn(modification['status'], ('finished', 'started'))

    def test_deployment_modifications_list_with_params(self):
        params = {'deployment_id': self.first_deployment_id}
        self._put_two_deployment_modifications()
        response = self.get('/deployment-modifications',
                            query_params=params).json
        self.assertEqual(1, len(response), 'expecting 1 deployment mod '
                                           'results, got {0}'
                         .format(len(response)))
        for modification in response:
            self.assertEquals(modification['deployment_id'],
                              self.first_deployment_id)
            self.assertIn(modification['status'], ('finished', 'started'))
