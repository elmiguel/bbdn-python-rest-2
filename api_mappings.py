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
    -p <params>, --params <params>  Accepts a JSON String of key: value pairs that will be added to the RET API request.
                                       offset: The number of rows to skip before beginning to return rows. An offset of 0 is the same as
                                               omitting the offset parameter.

                                       limit: The maximum number of results to be returned. There may be less if the query returned less
                                              than the maximum.

                                       fields: A comma-delimited list of fields to include in the response. If not specified, all fields
                                               will be returned.

                                    **Note: The params are built into the settings for defaults, if provided, then
                                            the defaults will be overwritten.
                                    [default: None]
    -f <file>..., --file <file>...  Data used in post, put, patch methods, but using a file or a list of files. Overrides --data. [default: None]
    -D, --debug                     Turn on debug mode. [default: False]
    -P <page>, --get-page <page>    Accepts the pagination value returned from a previous request.
                                    If set, then all ids, types, params are ignored. As they are
                                    already included in the paginated value.

"""


def api():
    if opts['--verbose']:
        print(opts)

    auth = AuthToken(opts['--verbose'])
    auth.set_token()

    learn_object = LearnObject(opts)
    if opts['--method'] == 'get':
        learn_object.get()
    elif opts['--method'] == 'post':
        learn_object.create()
    elif opts['--method'] == 'put':
        learn_object.update()
    elif opts['--method'] == 'delete':
        learn_object.delete()

if __name__ == '__main__':
    opts = docopt(usage, version='Bb REST API CLI v0.0.1')
    api()
