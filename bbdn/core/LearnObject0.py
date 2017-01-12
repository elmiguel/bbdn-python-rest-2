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
from bbdn.core.Validator import UserSchema, CourseSchema, ContentsSchema, DataSourceSchema, TermSchema, MembershipSchema, GradebookColumnSchema, SystemSchema
from settings import config as settings
from schema import SchemaError

validators = {
    'users': UserSchema,
    'courses': CourseSchema,
    'contents': ContentsSchema,
    'datasources': DataSourceSchema,
    'terms': TermSchema,
    'memberships': MembershipSchema,
    'system': SystemSchema,
    'grades': GradebookColumnSchema
}


class LearnObject:

    def __init__(self, options):
        base_path = '/learn/api/public/v1/'
        self.auth = "Bearer %s" % settings['payload']['token']
        self.target_url = settings['target_url']
        self.api_type = [k for k, v in validators.items() if options[k]][0]
        self.api_path = base_path + self.api_type
        self.class_name = self.api_type.title()[:-1]
        self.validator = validators[self.api_type]
        self.res = None
        self.isPaginated = False

        # Action controls
        self.data = options['--data']
        # if a file is provided, override self.data
        if options['--file']:
            with open(options['--file']) as f:
                self.data = json.dumps(json.loads(f.read()))

        self.debug = options['--debug']
        self.enrollments = options['--enrollments']

        self.help = options['--help']
        self.method = options['--method']
        self.page = options['--get-page']

        default_params = settings['api'][self.api_type]['params']

        try:
            override_params = json.loads(options['--params'])
            default_params.update(override_params) if options[
                '--params'] else default_params
            self.params = default_params.copy()
        except ValueError:
            self.params = default_params.copy()
        except json.decoder.JSONDecodeError:
            self.params = default_params.copy()

        self.type = options['--type'].split(',')
        self.verbose = options['--verbose']
        self.attempts_id = options['ATTEMPTS-ID']
        self.child_course_id = options['CHILD-COURSE-ID']
        self.column_id = options['COLUMN-ID']
        self.column_id = options['CONTENT-ID']
        self.course_id = options['COURSE-ID']
        self.data_source_id = options['DATA-SOURCE-ID']
        self.group_id = options['GROUP-ID']
        self.term_id = options['TERM-ID']
        self.user_id = options['USER-ID']

    @staticmethod
    def date_handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError

    def create(self):
        '''
        {"externalId": "test.python.user","dataSourceId": "_81_1","userName": "python_demo","password": "python61","availability": {"available": "Yes"},"name": {"given": "Python","family": "Demo"},"contact": {"email": "no.one@ereh.won"}}
        '''
        try:
            if self.verbose:
                print("Data from create:", type(self.data), self.data)

            # if self.validator.validate(self.data):
            if self.verbose:
                print("[%s] create called" % self.class_name)
            url = self.prep_url()
            print(url)
            self.do_rest(url)

        except SchemaError as se:
            self.res = {"error": se}

        print(self.res)

    def update(self, obj_id=None, id_type=None, data=None, params=None):
        # try:
        #     data = json.loads(data)
        #     if self.verbose:
        #         print(data)
        #
        #     if self.validator.validate(data):
        #         if self.verbose:
        #             print("[%s] update called" % self.class_name)
        #
        #         params = self.params.update(params) if params else self.params
        #
        #         self.do_rest('PATCH', self.prep_url(obj_id, id_type),
        #                      'update', data=data, params=params)
        #
        # except SchemaError as se:
        #     self.res = {"error": se}

        print('NEEDS TO BE REFACTORED!')
        return self.res

    def delete(self, obj_id=None, id_type=None):
        if self.verbose:
            print("[%s] delete called" % self.class_name)

        # self.do_rest('DELETE', self.prep_url(obj_id, id_type) +
        #              self.prep_id(obj_id[0], id_type[0]), 'delete')
        # self.res = {"message": "Successfully deleted", "id": obj_id[0]}

        print('NEEDS TO BE REFACTORED!')
        return self.res

    def get(self):
        if self.verbose:
            print("[%s:get()] called" % self.class_name)

        if self.page:
            url = "https://%s%s" % (self.target_url, self.page)
            self.isPaginated = True
        else:
            url = self.prep_url()

        self.do_rest(url)

    def prep_url(self):
        url = 'https://%s%s' % (self.target_url, self.api_path)

        # Requesting single obj?
        if self.api_type == 'users':
            if self.user_id:
                url += '/%s:%s' % (self.type[0], self.user_id)

                # check for enrollments?
                if self.enrollments:
                    url += '/courses'

        elif self.api_type == 'courses':
            if self.course_id:
                url += '/%s:%s' % (self.type[0], self.course_id)

                # child course(s)
                if self.child_course_id:
                    if self.child_course_id == 'ALL':
                        url += '/children'
                    else:
                        url += '/children/%s:%s' % (self.type[1]
                                                    or self.type[0], self.child_course_id)

        elif self.api_type == 'contents':
            # contents was pre-appended: replace with courses
            url = url.replace('contents', 'courses')
            url += '/%s:%s/contents' % (self.type[0], self.course_id)

            # child content(s)
            if self.content_id:
                if self.content_id == 'ALL':
                    url += '/%s:%s' % (self.type[1]
                                       or self.type[0], self.content_id)
                else:
                    url += '/%s/children/' % self.child_course_id

        elif self.api_type == 'groups':
            # groups was pre-appended: replace with courses
            url = url.replace('groups', 'courses')
            url += '/%s:%s/contents/%s:%s/groups' % (self.type[0],
                                                     self.type[1]
                                                     or self.type[0])
            if self.group_id:
                url += '/%s:%s' % (self.type[2]
                                   or self.type[1]
                                   or self.type[0], self.group_id)

        elif self.api_type == 'memberships':
            # memberships was pre-appended: replace with courses
            url = url.replace('memberships', 'courses')
            url += '/%s:%s/users' % (self.type[0], self.course_id)
            if self.user_id:
                url += '/%s:%s' % (self.type[1] or self.type[0], self.user_id)

        elif self.api_type == 'datasources':
            if self.data_source_id:
                url += '/%s:%s' % (self.type[0], self.data_source_id)

        elif self.api_type == 'system':
            url += '/version'

        elif self.api_type == 'terms':
            if self.term_id:
                url += '/%s:%s' % (self.type[0], self.term_id)

        return url

    def do_rest(self, url):
        if self.verbose:
            print(url)

        session = requests.session()
        session.verify = False

        headers = {'Authorization': self.auth, 'Content-Type': 'application/json'}

        if self.isPaginated:
            self.params = None

        req = requests.Request(self.method.upper(), url, data=self.data,
                               headers=headers, params=self.params)
        prepped = session.prepare_request(req)

        if self.verbose:
            print("[%s:do_rest()] Called" % self.class_name)
            print(
                "[%s:do_rest()] method=%s, url=%s, data=%s" % (self.class_name, self.method, url, self.data))

            print("Prepared Request:", prepped.url)

        # Only set if debugging or in development
        if self.debug:
            session.mount('https://', Tls1Adapter())

        if self.verbose:
            print("[%s:%s()] %s Request URL: %s" %
                  (self.class_name, self.method, self.method.upper(), url))

        r = session.send(prepped)

        if self.verbose:
            print("[%s:%s()] STATUS CODE: %d" % (self.class_name, self.method, r.status_code))
            print("[%s:%s()] RESPONSE:" % (self.class_name, self.method))

        if r.text:
            # if '<!doctype html>' not in r.text[:16]:
            self.res = json.loads(r.text)
            print(self.res)

        if self.verbose:
            print(json.dumps(self.res, indent=settings['json_options']['indent'],
                             separators=settings['json_options']['separators'],
                             default=self.date_handler))
