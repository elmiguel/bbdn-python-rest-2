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
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from settings import config as settings
from datetime import datetime, timedelta
from time import sleep

requests.packages.urllib3.disable_warnings()

# Tls1Adapter allows for connection to sites with non-CA/self-signed
# certificates e.g.: Learn Dev VM


class Tls1Adapter(HTTPAdapter):

    def __init__(self):
        self.poolmanager = None
        super().__init__()

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        # Old code had: ssl.PROTOCOL_TLSv1 but there is no upstream to _ssl where the variable actually lives
        # Copied the code straight from _ssl for clarity.
        # PROTOCOL_SSLv2 = 0
        # PROTOCOL_SSLv23 = 2
        # PROTOCOL_SSLv3 = 1
        # PROTOCOL_TLSv1 = 3
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize, block=block, ssl_version=3)


class AuthToken:

    def __init__(self, verbose=False):
        self.verbose = verbose

    @staticmethod
    def get_key():
        return settings['key']

    @staticmethod
    def get_secret():
        return settings['secret']

    def date_handler(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError

    def set_token(self):
        oauth_url = 'https://' + settings['target_url'] + settings['api']['set_token']['path']
        parsed_json = None
        if settings["token"] is None:
            session = requests.session()

            # remove for production
            session.mount('https://', Tls1Adapter())

            # Authenticate
            if self.verbose:
                print("[auth:setToken] POST Request URL: " + oauth_url)
                print("[auth:setToken] JSON Payload: \n%s" % json.dumps(settings['payload'],
                                                                        indent=settings[
                                                                            'json_options']['indent'],
                                                                        separators=settings[
                                                                            'json_options']['separators'],
                                                                        default=self.date_handler))

            r = session.post(oauth_url, data=settings['payload'],
                             auth=(settings['key'], settings['secret']), verify=False)

            if self.verbose:
                print("[auth:setToken()] STATUS CODE: %d" % r.status_code)
            # strip quotes from result for better dumps
            res = json.loads(r.text)

            if self.verbose:
                print("[auth:setToken()] RESPONSE: \n%s" % json.dumps(res, indent=settings['json_options']['indent'],
                                                                      separators=settings[
                                                                          'json_options']['separators'],
                                                                      default=self.date_handler))

            if r.status_code == 200:
                parsed_json = json.loads(r.text)

            settings['payload']['token'] = parsed_json['access_token']
            expires = parsed_json['expires_in']
            m, s = divmod(expires, 60)
            # h, m = divmod(m, 60)
            # print "%d:%02d:%02d" % (h, m, s)
            now = datetime.now()
            settings['payload']['expires_at'] = now + timedelta(seconds=s, minutes=m)

            if self.verbose:
                print("[auth:setToken()] Token Expires at " +
                      settings['payload']['expires_at'].strftime("%H:%M:%S"))
                print("[auth:setToken()] TOKEN: %s" % settings['payload']['token'])

            # there is the possibility the required token may expire
            # before we are done so perform expiration sanity check...
            if self.is_expired(settings['payload']['expires_at']):
                self.set_token()

            # else:
            #     print("[auth:setToken()] ERROR")
        else:
            print("[auth:setToken()] TOKEN set")

    def get_token(self):
        # if token time is less than a one second then
        # print that we are pausing to clear
        # re-auth and return the new token
        if self.is_expired(settings['payload']['expires_at']):
            self.set_token()

        return settings['payload']['token']

    def revoke_token(self):
        revoke_url = 'https://' + settings['target_url'] + settings['api']['revoke_token']['path']

        if self.verbose:
            print("[auth:revokeToken()] KEY: %s" % settings['key'])
            print("[auth:revokeToken()] SECRET: %s" % settings['secret'])
        try:
            t = "[auth:revokeToken()] TOKEN: %s" % settings['payload']['token']

            if self.verbose:
                print(t)
        except TypeError as te:
            print("[auth:revokeToken()] is None or invalid", te)

        if self.verbose:
            print("[auth:revokeToken()] revoke_url: %s" % revoke_url)

        settings['payload']['token'] = settings['token']

        if settings['payload']['token'] != '' or settings['payload']['token']:
            if self.verbose:
                print("[auth:revokeToken()] TOKEN not empty...able to revoke")
                print("[auth:revokeToken()] POST PAYLOAD: ")

            for keys, values in settings['payload'].items():
                if values is None:
                    values = "None"

                if isinstance(values, datetime):
                    values = values.strftime("%H:%M:%S")

                if self.verbose:
                    print("\t\t\t", keys, values)

            session = requests.session()
            # remove for production
            session.mount('https://', Tls1Adapter())

            # revoke token
            if self.verbose:
                print("[auth:revokeToken] Request URL: %s" % revoke_url)
                print("[auth:revokeToken] JSON Payload: \n%s" %
                      json.dumps(settings['payload'], indent=settings['json_options']['indent'],
                                 separators=settings['json_options']['separators'],
                                 default=self.date_handler))

            r = session.post(revoke_url, data=settings['payload'],
                             auth=(settings['key'], settings['secret']), verify=False)

            if self.verbose:
                print("[auth:revokeToken()] STATUS CODE: %d" % r.status_code)
                print("[auth:revokeToken()] RESPONSE: %s" % r.text)

            if r.status_code == 200:
                print("[auth:revokeToken()] Token Revoked")
            else:
                print("[auth] ERROR on token revoke")
        else:
            print("[auth:revokeToken()] Must have set a token to revoke a token...")

    def is_expired(self, expiration_datetime):
        try:
            if self.verbose:
                print("[auth.is_expired()] Token Expires at " +
                      expiration_datetime.strftime("%H:%M:%S"))

            time_left = (expiration_datetime - datetime.now()).total_seconds()

            if self.verbose:
                print("[auth.is_expired()] Time Left on Token (in seconds): " + str(time_left))

            if time_left < 1:
                if self.verbose:
                    print("[auth.is_expired()] Token almost expired retrieving new token in two seconds.")

                sleep(1)
                return True

        except AttributeError as ae:
            print("[Auth.is_expired()] Expiration Datetime is invalid:", ae)
            return False
