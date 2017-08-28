# -*- coding: utf-8 -*-
# Licensed to Anthony Shaw (anthonyshaw@apache.org) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class PathsClient(object):
    """ Path API. """

    def __init__(self, client):
        self.client = client

    def all(self, from_page=None):
        """
        Get all paths.

        Paths are returned sorted by creation date,
        with the most recently created path appearing first.

        :param from_page: Get from page (when paginated)
        :type  from_page: ``int``

        :return: A list of paths
        :rtype: ``list`` of ``dict``
        """
        params = {}

        if from_page is not None:
            params['from'] = from_page

        paths = self.client.get('paths', params=params)
        return [self._to_path(i) for i in paths['results']]

    def get(self, id):
        """
        Fetch a path by ID

        :param id: Path ID
        :type  id: ``str``

        :return: A path
        :rtype: ``dict``
        """
        path = self.client.get('paths/{0}'.format(id))
        return self._to_path(path)

    def _to_path(self, data):
        # TODO : Reflect into class model
        return data
