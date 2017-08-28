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

import requests

from pathgather.exceptions import PathgatherApiException
from .users import UsersClient
from .content import ContentClient
from .paths import PathsClient


class PathgatherClient(object):
    """
    The main API client
    """
    def __init__(self, host, api_key):
        """
        Instantiate a new API client

        :param host: The host name, e.g. mycompany.pathgather.com
        :type  host: ``str``

        :param api_key: The API token (from the admin console)
        :type  api_key: ``str``
        """
        self._api_key = api_key

        self.base_url = 'https://{0}/v1'.format(host)

        self.session = requests.Session()
        self.session.proxies = {'https': 'https://localhost:8888/'}
        self.session.verify = False
        self.session.headers.update(
            {'Accept': 'application/json',
             'Content-Type': 'application/json',
             'Authorization': "Bearer {0}".format(api_key)})

        self.users = UsersClient(self)
        self.content = ContentClient(self)
        self.paths = PathsClient(self)

    def get(self, uri, params=None):
        try:
            result = self.session.get("{0}/{1}".format(self.base_url, uri),
                                      params=params)
            result.raise_for_status()

            return result.json()
        except requests.HTTPError as e:
            raise PathgatherApiException(e.response.text, uri)

    def post(self, uri, data=None):
        try:
            result = self.session.post("{0}/{1}".format(self.base_url, uri),
                                       json=data)
            result.raise_for_status()

            return result.json()
        except requests.HTTPError as e:
            raise PathgatherApiException(e.response.text)

    def put(self, uri, data=None):
        try:
            result = self.session.put("{0}/{1}".format(self.base_url, uri),
                                      json=data)
            result.raise_for_status()
        except requests.HTTPError as e:
            raise PathgatherApiException(e.response.text)

    def delete(self, uri):
        try:
            result = self.session.delete("{0}/{1}".format(self.base_url, uri))
            result.raise_for_status()
        except requests.HTTPError as e:
            raise PathgatherApiException(e.response.text)
