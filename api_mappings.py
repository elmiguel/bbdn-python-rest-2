from docopt import docopt
import sys
from bbdn.core.Auth import AuthToken
from bbdn.core.LearnObject0 import LearnObject
import json

usage = """Bb REST API CLI

Usage:
    bbrestapi courses [COURSE-ID CHILD-COURSE-ID] [options]
    bbrestapi contents COURSE-ID [CONTENT-ID] [options]
    bbrestapi groups COURSE-ID [CONTENT-ID GROUP-ID USER-ID] [options]
    bbrestapi memberships COURSE-ID [USER-ID] [options]
    bbrestapi grades COURSE-ID [COLUMN-ID ATTEMPTS-ID USER-ID] [options]
    bbrestapi users [USER-ID] [options]
    bbrestapi datasources [DATA-SOURCE-ID] [options]
    bbrestapi terms [TERM-ID] [options]
    bbrestapi system

Commands:
    courses:     Targets courses and it's chidlren.
    contents:    Targets contents of a course.
    groups:      Targets grouped assignments within a course.
    memberships: Targets users within a course.
    grades:      Targets grades within a course.
    users:       Targets users.
    datasources: Targets data sources.
    terms:       Targets terms.
    system:      Returns the Bb Learn system information.

Inputs:
    COURSE-ID       The target COURSE-ID. [default: None]
    CHILD-COURSE-ID Target Child courses. ALL for all children or specific ID. [default: None]
    CONTENT-ID      Target Content with in a Course. ALL for all contents or specific ID. [default: None]
    GROUP-ID        Target Group Assignments with in a Course. ALL for all contents or specific ID. [default: None]
    USER-ID         Target a specific User. ALL for all contents or specific ID. [default: None]
    COLUMN-ID       Target a specific Column in a gradebook. ALL for all columns or specific ID. [default: None]
    ATTEMPTS-ID     Target a specific Attempt. ALL for all attempts or specific ID. [default: None]
    DATA-SOURCE-ID  Target a specific Data Source. [default: None]
    TERM-ID         Target a specific Term. [default: None]

Options:
    -h, --help                      Show this screen.
    -v, --verbose                   Verbose mode.
    -e, --enrollments               If set, then return the memberships for a specific user. Only used with: get users.
    -t <type>..., --type <type>...  Set the type for the Id. primaryId, externalId, userName. Can be comma delimited
                                    to accept multiple targets.
                                    Note: types are assigned to in order given to the order of the IDs in a API target.
                                    Example:
                                        URL: /learn/api/public/v1/courses/{courseId}/gradebook/columns/{columnId}/attempts/{attemptId}

                                        args: -t externalId,primaryId,primaryId

                                        Result:
                                        /learn/api/public/v1/courses/externalId:<id>/gradebook/columns/primaryId:<id>/attempts/primaryId:<id>
                                    [default: primaryId]
    -m <method>, --method <method>  If set, controls the HTTP method of interaction to the API and Target.
                                    Methods: get, post, put, patch, delete. [default: get].
    -d <data>, --data <data>        Data used in post, put, patch methods. [default: None]
    -f <file>..., --file <file>...  Data used in post, put, patch methods, but using a file or a list of files. [default: None]
"""

base_path = '/learn/api/public/v1/'
token = base_path + 'oauth2/token'


def api():
    v = opts['--verbose']
    method = opts['--method'] if opts['--method'] in ['get',
                                                      'post', 'put', 'patch', 'delete'] else None
    if not method:
        print('Unsupported method', opts['--method'] + '.',
              'Please see help for supported methods.')
        sys.exit(1)

    auth = AuthToken(v)
    auth.set_token()

    res = None
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

if __name__ == '__main__':
    opts = docopt(usage, version='Bb REST API CLI v0.0.1')
    api()
