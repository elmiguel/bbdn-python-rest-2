"""

    Copyright (C) 2016, Blackboard Inc.
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:

        Redistributions of source code must retain the above copyright notice, this list of conditions and the following
        disclaimer.

        Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
        following disclaimer in the documentation and/or other materials provided with the distribution.

        Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products
        derived from this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
        BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
        DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
        EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
        LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
        IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
        OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
import json
import requests
from bbdn.core.Auth import Tls1Adapter
from bbdn.core.Validator import UserSchema, CourseSchema, ContentsSchema, DataSourceSchema, TermSchema, MembershipSchema
from settings import config as settings
from schema import SchemaError

validators = {
    'user': UserSchema,
    'course': CourseSchema,
    'content': ContentsSchema,
    'datasource': DataSourceSchema,
    'term': TermSchema,
    'membership': MembershipSchema
}


class LearnObject:
    def __init__(self, class_name, verbose=False, debug=False):
        self.auth = "Bearer %s" % settings['payload']['token']
        self.target_url = settings['target_url']
        self.api_type = class_name.lower()
        self.api_path = settings['api']["%ss" % self.api_type]['path']
        self.replacement = settings['api']["%ss" % self.api_type]['replace']
        # self.fields = settings['api']["%ss" % self.api_type]['fields']
        self.class_name = class_name
        self.verbose = verbose
        self.debug = debug
        self.validator = validators[self.api_type]
        self.params = settings['api']["%ss" % self.api_type]['params']
        self.res = None
        self.isPaginated = False

    @staticmethod
    def date_handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError

    def create(self, data=None):
        try:
            data = json.loads(data)
            if self.verbose:
                print("Data from create:", type(data), data)

            if self.validator.validate(data):
                if self.verbose:
                    print("[%s] create called" % self.class_name)

                self.do_rest('POST', "https://%s%s" % (self.target_url, self.api_path), 'create', data=data)

        except SchemaError as se:
            self.res = {"error": se}
        return self.res

    def update(self, obj_id=None, id_type=None, data=None, params=None):
        try:
            data = json.loads(data)
            if self.verbose:
                print(data)

            if self.validator.validate(data):
                if self.verbose:
                    print("[%s] update called" % self.class_name)

                params = self.params.update(params) if params else self.params

                self.do_rest('PATCH', self.prep_url(obj_id, id_type), 'update', data=data, params=params)

        except SchemaError as se:
            self.res = {"error": se}

        return self.res

    def delete(self, obj_id=None, id_type=None):
        if self.verbose:
            print("[%s] delete called" % self.class_name)

        self.do_rest('DELETE', self.prep_url(obj_id, id_type), 'delete')
        self.res = {"message": "Successfully deleted", "id": obj_id[0]}

        return self.res

    def get(self, obj_id=None, id_type=None, params=None, page=None):
        if self.verbose:
            print("[%s:get()] called" % self.class_name)

        params = self.params.update(params) if params else self.params

        if page:
            url = "https://%s%s" % (self.target_url, page)
            self.isPaginated = True
        else:
            url = self.prep_url(obj_id, id_type)

        self.do_rest('GET', url, 'get', params=params)

        return self.res

    def prep_url(self, obj_id=None, id_type=None):
        # TODO: need to map the two arrays to assign one-to-one or one-to-many as there are some routes with 3 ids.
        # Check to see if we are trying to update a sub-item
        if len(obj_id) > 1:

            # if id_type is not more than 1 (one), default it to a list with the same id_type
            if len(id_type) == 1:
                id_type = [id_type[0], id_type[0]]
                if self.verbose:
                    print("RESET id_type", id_type)

            url = "https://%s%s%s" % (
                self.target_url,
                self.api_path.replace(self.replacement, self.prep_id(obj_id[0], id_type[0])[1:]),
                self.prep_id(obj_id[1], id_type[1]))

            if self.verbose:
                print("URL TEST FRO SUB-ITEMS:\n", url)
        else:
            # if there was no id, then there is a request to get multiple resets
            if len(obj_id) == 0:
                url = "https://%s%s" % (self.target_url, self.api_path)
            else:
                url = "https://%s%s%s" % (self.target_url, self.api_path, self.prep_id(obj_id[0], id_type[0]))

        return url

    def prep_id(self, obj_id=None, id_type=None):
        if self.verbose:
            print("prep_id called:", obj_id, id_type)

        _id = "/%s" % obj_id if obj_id else ''

        if id_type and id_type != "primaryId":
            _id = "/%s:%s" % (id_type, obj_id)
        return _id

    def do_rest(self, method, url, _caller, data=None, params=None):
        data = json.dumps(data) if data else None
        session = requests.session()
        session.verify = False

        headers = {'Authorization': self.auth, 'Content-Type': 'application/json'}

        if self.isPaginated:
            params = None

        req = requests.Request(method, url, data=data, headers=headers, params=params)
        prepped = session.prepare_request(req)

        if self.verbose:
            print("[%s:do_rest()] Called" % self.class_name)
            print(
                "[%s:do_rest()] method=%s, url=%s, _caller=%s, data=%s" % (self.class_name, method, url, _caller, data))

            print("Prepared Request:", prepped.url)

        # Only set if debugging or in development
        if self.debug:
            session.mount('https://', Tls1Adapter())

        if self.verbose:
            print("[%s:%s()] %s Request URL: %s" % (self.class_name, _caller, method, url))

        r = session.send(prepped)

        if self.verbose:
            print("[%s:%s()] STATUS CODE: %d" % (self.class_name, _caller, r.status_code))
            print("[%s:%s()] RESPONSE:" % (self.class_name, _caller))

        if r.text:
            self.res = json.loads(r.text)

        if self.verbose:
            print(json.dumps(self.res, indent=settings['json_options']['indent'],
                             separators=settings['json_options']['separators'],
                             default=self.date_handler))
