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
        term_create.json       Test data to create a term.
        term_update.json       Test data to uodate a term.
        user_create.json       Test data to create a user.
        user_update.json       Test data to update a term.
        
    bbrestapi.py               Main CLI to communicate to the Learn API.
    settings.py                Settings that are used in CLI.
    setup.py                   Simple setup to install this as a libary.
    

### What it does
The rest demo script demonstrates authenticating a REST application, management and use of the authorization token, and creating, updating, discovering, and deleting supported Learn objects.

<i><b>NOTE:</b> Before running the example code you must register a developer account and application as described on the Developer Community <a href="https://community.blackboard.com/docs/DOC-1579">What is the Developer Portal: Developer Registration and Application Management</a> and <a href="https://community.blackboard.com/docs/DOC-1580">Managing REST Integrations in Learn: The REST Integrations Tool for System Administrators</a> pages. You must also configure the script as outlined in the below Configure the Script section.</i>

When run with only a target URL the script will in the following order
Authenticate<br/>
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
Bb REST API Demo

Usage:
    bbrestapi get -o <learn_object> [-i <id>...] [-t <type>...] [-v] [-D] [-P <params>] [--get-page <page>]
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
                       grade:  Will create a Learning Object as a Gradebook item. *(NOT IMPLEMENTED...yet)*

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
```

<br/><br/>

## Running the Demo!
### Setup Your Test Server
To run the demo if you have not already done so you must as outlined above register the application via the Developer Portal and add the application to your test environment using the REST API Integration tool.


### Configuring the Script
Before executing the script to run against your test server you must configure it with your registered application's Key and Secret in the settings.py file.

Once you have setup your test server and edited the settings.py to reflect your application's key and secret you may run the command line tools as outlined above or via your IDE.


### Conclusion
For a thorough walkthrough of this code, visit the corresponding Blackboard Developer Community <a href="#">REST Demo Using Python</a>.
