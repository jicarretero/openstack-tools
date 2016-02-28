#!/usr/bin/python

from wsgiref.simple_server import make_server, demo_app

# A relistic response body from FIWARELab Keystone
body='{"versions": {"values": [{"status": "stable", "updated": "2013-03-06T00:00:00Z", "media-types": [{"base": "application/json", "type": "application/vnd.openstack.identity-v3+json"}, {"base": "application/xml", "type": "application/vnd.openstack.identity-v3+xml"}], "id": "v3.0", "links": [{"href": "http://localhost:4730/v3/", "rel": "self"}]}, {"status": "stable", "updated": "2014-04-17T00:00:00Z", "media-types": [{"base": "application/json", "type": "application/vnd.openstack.identity-v2.0+json"}, {"base": "application/xml", "type": "application/vnd.openstack.identity-v2.0+xml"}], "id": "v2.0", "links": [{"href": "http://localhost:4730/v2.0/", "rel": "self"}, {"href": "http://docs.openstack.org/", "type": "text/html", "rel": "describedby"}]}]}}'


# Responses the script returns. Each response is retuirned every other request
# I know '200 Multiple Choices is not an HTTP usual response, but it is 
# useful for testing purposes.
status=["300 Multiple Choices", "200 Multiple Choices"]


class KeystoneSimulation:
    def __init__(self):
        self.i=0;
        httpd = make_server('0.0.0.0', 4728, self.application)
        httpd.serve_forever()

    def application(self, environ, start_response):
        headers = [
            ("Vary", "X-Auth-Token"),
            ("Content-Length", str(len(body))),
            ("Content-Type", "application/json"),
        ]
        # Send the headers:
        start_response(status[self.i], headers)
        self.i=(self.i+1)%len(status)
        # Now send the body:
        return [body]

if __name__ == "__main__":
    demo=KeystoneSimulation()
