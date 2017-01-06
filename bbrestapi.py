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

from docopt import docopt
import sys
from bbdn.core.Auth import AuthToken
from bbdn.core.LearnObject import LearnObject
import json

LEARN_OBJECTS = ['user', 'course', 'term', 'membership', 'datasource', 'content', 'system', 'grade']

usage = """Bb REST API Demo

Usage:
    bbrestapi get -o <learn_object> [-i <id>...] [-t <type>...] [-v] [-D] [-P <params>] [--get-page <page>] [-a <path>]
    bbrestapi create -o <learn_object> -d <data> [-v] [-D]
    bbrestapi update -o <learn_object> -i <id>... -d <data> [-t <type>...] [-v] [-D]
    bbrestapi delete -o <learn_object> -i <id>... [-t <type>...] [-v] [-D]

Commands:
    get            Retrieve a given object or objects. Sends a GET request to API endpoint.
    create         Create an object. Sends a POST request to API endpoint.
    update         Updates an object or objects. Sends a PATCH request to API endpoint.
    delete         Deletes an object. Sends a DELETE request to API endpoint.

Inputs:
    learn_objects  The model class in which the data is used in transit. Singular form. Case Sensitive (lower case).
                       user: Will create a Learning Object as a User.
                       course: Will create a Learning Object as a Course.
                       term: Will create a Learning Object as a Term.
                       membership: Will create a Learning Object as a Membership.
                       datasource: Will create a Learning Object as a DataSource.
                       content: Will create a Learning Object as a Content item.
                       system: Will create a Learning Object as a System.
                       grade:  Will create a Learning Object as a Gradebook item. *(IMPLEMENTED...yet, but not Available)*


    id             If no id (<id>) specified, then will default to system get_all (200 pagination limit).
                   Required with --type options when not left to default. Always required with update, delete commands.
                   **Note: if more that one id is specified, then it is assumed that the first id is for the base rest
                            endpoint. The second is for the sub-item.

                        Example: /learn/api/public/v1/courses/{courseId}/contents/{contentId}

                        The {courseId} in this example will be replaced by the first id based on the settings in the
                        main settings.py file.

    data           Data to be sent to the REST API. JSON string data. Required for: create, update, and delete commands.
    types          Methods in which the API will use in the type of request.
                       primaryId: Default (nothing provided): Uses the pk1 id (_<id>_1)
                       externalId: Uses the batch_uid (external_person_key)
                       userName: Uses the user_id (the username instead of an id)

                   **Note: if more that one type is specified, then it is assumed that the first type is for the base
                           rest endpoint. The second is for the sub-item.

                        Example: /learn/api/public/v1/courses/{courseId}/contents/{contentId}

                        The {courseId} in this example will be replaced by the first type based on the settings in
                        the main settings.py file. The second type will be applied on the {contentId}. If only one
                        type is supplied, then the same type will be applied to both ids.

    params         Accepts a JSON String of key: value pairs that will be added to the RET API request.

                       offset: The number of rows to skip before beginning to return rows. An offset of 0 is the same as
                               omitting the offset parameter.

                       limit: The maximum number of results to be returned. There may be less if the query returned less
                              than the maximum.

                       fields: A comma-delimited list of fields to include in the response. If not specified, all fields
                               will be returned.

                   **Note: The params are built into the settings for defaults, if provided, then
                           the defaults will be overwritten.

Options:
    -h, --help                                       Show this screen.
    -v, --verbose                                    Verbose mode.
    -o <learn_object>, --learn-object <learn_object> Refer to Inputs: learn_objects.
    -i <id>..., --id <id>...                         Refer to Inputs: id.
    -d <data>, --data <data>                         Refer to Inputs: data.
    -t <type>.., --type <type>...                    Refer to Inputs: types. [default: primaryId]
    -D, --debug                                      If set, this will enable debugging mode
    -P <params>, --params <params>                   Refer to Inputs: params.
    --get-page <page>                                Accepts the pagination value returned from a previous request.
                                                     If set, then all ids, types, params are ignored. As they are
                                                     already included in the paginated value.
    -a <path>, --append <path>                       Append a suffix to the url: /users
"""


def api(opts):
    v = opts['--verbose']
    debug = opts['--debug']
    auth = AuthToken(v)
    auth.set_token()
    c = {key: value for key, value in opts.items() if key in ['get', 'create', 'update', 'delete']}
    command = list(filter(c.get, c))[0]

    res = None
    if opts['--learn-object'] not in LEARN_OBJECTS:
        print("Invalid Learning Object type: please refer to the Input: learn_objects in the help")
        sys.exit(1)
    else:
        learn_object = LearnObject(opts['--learn-object'].title(), v, debug)

    if v:
        print(opts)

    if command == 'get':
        if v:
            print(command)
        res = learn_object.get(obj_id=opts['--id'], id_type=opts['--type'], params=opts['--params'],
                               page=opts['--get-page'], append=opts['--append'])
    elif command == 'create':
        if v:
            print(command)
        res = learn_object.create(data=opts['--data'])
    elif command == 'update':
        if v:
            print(command)
        res = learn_object.update(obj_id=opts['--id'], id_type=opts['--type'], data=opts['--data'],
                                  params=opts['--params'])
    elif command == 'delete':
        if v:
            print(command)
        res = learn_object.delete(obj_id=opts['--id'], id_type=opts['--type'])

    print(json.dumps(res))


def test():
    print("Running Test")


if __name__ == '__main__':
    args = docopt(usage, version='Bb REST API Demo v0.0.1')
    api(args)
