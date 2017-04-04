# BBDN-REST-Python
This project contains sample code for demonstrating the Blackboard Learn REST APIs in Python.
This sample code was built with Python 3.5.0.

###Project at a glance:
- Target: Blackboard Learn SaaS Release 2015.11.0-ci.23+a9a4758 minimum
- Source Release: v1.0
- Release Date  2016-02-24
- Refactored Date  2016-08-31
- Original Author: moneil
- Code Refactoring: Michael Bechtel
- Tested on Blackboard Learn SaaS Release 2015.11.0-ci.23+a9a4758
- Tested on Blackboard Learn 9.1  Release 3100.0.0-rel.107+401e22b

###Requirements:
- Python  3.5.0
- Python Modules: docopt and schema
```
$ pip install docopt schema
```

- Developer account - register at https://developer.blackboard.com
- Test instance


### Setting Up Your Development Environment
#### Python development tools
You will first need to install Python 3.5.0 (or higher). You can use tools like brew or ports to install, or run the installation manually.

You may also install Python tools for your IDE or use a text editor and terminal to run the python code.


### Below is currently for the original code, will be updated soon
---
---
### Included Files

    bbdn (package)
        core (package)
            __init__.py
            Auth.py            Main authencation class.
            LearnObject.py     Class Object to get/maniplate Learn Object data.
            Validator.py       Class to validate data prior to sending to Learn.
        __init__.py

    test_data
        course_create.json     Test data to create a course.
        course_update.json     Test data to update a course.
        grade_create.json      Test data to create a grade.
        membership_create.json Test data to create a a membership.
        membership_update.json Test data to update a a membership.
        term_create.json       Test data to create a term.
        term_update.json       Test data to update a term.
        user_create.json       Test data to create a user.
        user_update.json       Test data to update a term.

    bbrestapi.py               Main CLI to communicate to the Learn API.
    settings.py                Settings that are used in CLI.
    setup.py                   Simple setup to install this as a libary.


### What it does
The rest demo script demonstrates authenticating a REST application, management and use of the authorization token, and creating, updating, discovering, and deleting supported Learn objects.

<i><b>NOTE:</b> Before running the example code you must register a developer account and application as described on the Developer Community <a href="https://community.blackboard.com/docs/DOC-1579">What is the Developer Portal: Developer Registration and Application Management</a> and <a href="https://community.blackboard.com/docs/DOC-1580">Managing REST Integrations in Learn: The REST Integrations Tool for System Administrators</a> pages. You must also configure the script as outlined in the below Configure the Script section.</i>


<b>TODO:</b>
- [ ] Create a task to run through all test data

Create, Read, and Update a Data Source<br/>
Create, Read, and Update a Term<br/>
Create, Read, and Update a Course<br/>
Create, Read, and Update a User<br/>
Create, Read, and Update a Membership<br/>
Delete created objects in reverse order of create - membership, user, course, term, datasource.

When run with a specific command on an object only that operation will be run - you are responsible for system cleanup.

All generated output is sent to the terminal (or IDE output window).

Usage:
```
Bb REST API CLI

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

```

<br/><br/>

## Running the Demo!
### Setup Your Test Server
To run the demo if you have not already done so you must as outlined above register the application via the Developer Portal and add the application to your test environment using the REST API Integration tool.


### Configuring the Script
Before executing the script to run against your test server you must configure it with your registered application's Key and Secret in the settings.py file.

Once you have setup your test server and edited the settings.py to reflect your application's key and secret you may run the command line tools as outlined above or via your IDE.


### Conclusion
For a thorough walkthrough of this code, visit the corresponding Blackboard Developer Community <a href="https://github.com/elmiguel/bbdn-python-rest-2">REST Demo Using Python</a>.
