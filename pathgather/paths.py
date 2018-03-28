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

import json

from .models.path import Path, UserPath
from .models.skill import Skill
from .models.user import User
from .utils import scrub


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
        :rtype: ``list`` of :class:`pathgather.models.path.Path`
        """
        params = {}

        if from_page is not None:
            params['from'] = from_page

        paths = self.client.get_paged('paths', params=params)
        results = []
        for page in paths:
            results.extend([self._to_path(i) for i in page['results']])
        return results

    def get(self, id):
        """
        Fetch a path by ID

        :param id: Path ID
        :type  id: ``str``

        :return: A path
        :rtype: :class:`pathgather.models.path.Path`
        """
        path = self.client.get('paths/{0}'.format(id))
        return self._to_path(path)

    def starts_and_completions(self, from_page=None, query=None):
        """
        Returns objects representing a user's interaction
        (starts and completions) with paths.
        User path items are returned sorted by start date,
        with the most recently started paths appearing first.

        :param from_page: Get from page
        :type  from_page: ``str``

        :param query: Extra query parameters
        :param query: ``str``

        :return: A list of path starts and completions
        :rtype: ``list`` of :class:`pathgather.models.content.UserPath`
        """
        params = {}

        if from_page is not None:
            params['from'] = from_page

        data = None
        if query is not None:
            data = json.dumps({'q': query})

        content = self.client.get_paged('user_paths', params=params, data=data)
        results = []
        for page in content:
            results.extend([self._to_user_path(i) for i in page['results']])
        return results

    def _to_user_path(self, data):
        scrub(data)
        data['user'] = User(**data['user'])
        data['path'] = Path(**data['path'])
        data['path'].user = User(**data['path'].user)
        return UserPath(**data)

    def _to_path(self, data):
        scrub(data)
        _skills = []
        for skill in data['skills']:
            _skills.append(Skill(**skill))
        data['skills'] = _skills
        data['user'] = User(**data['user'])
        return Path(**data)
