#!/usr/bin/env python

# provides a reverse proxy that only allows requests coming from the same
# user it's running as
#
# grant access based on the presence of a _ood_token_<session_id>=<password>
# cookie, where:
#  <session_id> is the OnDemand Session id
#  <password> is the password defined in the template/before.sh script

from twisted.internet import reactor, endpoints
from twisted.web import proxy, server
from twisted.web.resource import Resource
from twisted.web.resource import ForbiddenResource

import argparse
import getpass
import sys, os

#
# ReverseProxy Resource that checks cookie before forwarding requests
#
class TokenResource(Resource):

    def __init__(self, host, port, path):
            Resource.__init__(self)
            self.host = host
            self.port = port
            self.path = path

    def getChild(self, path, request):


        # check if the request comes from the right user (note: can be forged)
        # unshare is booted by "root" (what you think is root anyhow)
        # if user == getpass.getuser():

        # get ood token cookie
        # - cookie name depends on the ood interactive session id ($PWD)
        ood_session_id = os.path.basename(os.getcwd())
        cookie_name = str.encode('_ood_token_' + ood_session_id)
        cookie_bytes = request.getCookie(cookie_name)

        # getCookie doesn't throw key error but could be None
        if cookie_bytes != None:
            cookie = cookie_bytes.decode()
        else:
            cookie = None

        # get token from environment
        # - $_ood_token_<session_id> is set in template/before.sh script
        try:
            ood_token = os.environ.get("_ood_token_" +
                                        ood_session_id.replace("-", "_"))
        except:
            ood_token = None

        # check that cookie matches the local token
        if cookie == ood_token and cookie != None:
            return proxy.ReverseProxyResource(self.host,
                                                self.port,
                                                b'/' + path)

        # no cheese for you
        request.setResponseCode(403)
        return ForbiddenResource()


#
# parse arguments
#
def parse_args(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Token Revproxy')
    parser.add_argument('--app-port', dest='app_port', type = int,
                        required = True, help='application port, to forward requests to')
    parser.add_argument('--proxy-port', dest='proxy_port', type = int,
                        required = True, help='proxy port, to listen for requests on')
    parser.add_argument('--bind-host', dest='bind_host', type = str,
                required = False, help='the host to bind on', default="127.0.0.1")

    args = parser.parse_args(argv)
    return args

#
# entry point
#
def main(argv=sys.argv[1:]):
    args = parse_args(argv)
    print('authrevproxy is starting on port {} -> {}'.format(args.proxy_port,
                                                             args.app_port) )
    dest = TokenResource(args.bind_host, args.app_port, b'')
    site = server.Site(dest)

    endpoint = endpoints.TCP4ServerEndpoint(reactor, args.proxy_port)
    endpoint.listen(site)
    reactor.run()


if __name__ == '__main__':
    main()
