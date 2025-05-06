import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from views import (
    create_category,
    create_comment,
    create_tag,
    delete_category,
    delete_comment,
    delete_tag,
    get_all_categories,
    get_all_comments,
    get_all_tags,
    get_comments_by_user,
    get_comments_on_post,
    get_single_category,
    get_single_comment,
    get_single_tag,
    update_category,
    update_comment,
    update_tag,
)
from views.user import create_user, login_user


class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self):
        """Parse the url into the resource and id"""
        path_params = self.path.split("/")
        resource = path_params[1]
        if "?" in resource:
            param = resource.split("?")[1]
            resource = resource.split("?")[0]
            pair = param.split("=")
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            resource_id = None
            try:
                resource_id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, resource_id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()

    def do_GET(self):
        """Handle Get requests to the server"""
        self._set_headers(200)

        response = {}

        parsed = self.parse_url()

        if len(parsed) == 2:
            (resource, resource_id) = parsed

            if resource == "comments":
                if resource_id is not None:
                    response = get_single_comment(resource_id)
                else:
                    response = get_all_comments()
            elif resource == "categories":
                if resource_id is not None:
                    response = get_single_category(resource_id)
                else:
                    response = get_all_categories()
            elif resource == "tags":
                if resource_id is not None:
                    response = get_single_tag(resource_id)
                else:
                    response = get_all_tags()

        else:
            (resource, key, value) = parsed

            if resource == "comments":
                if key == "user_id":
                    response = get_comments_by_user(value)
                elif key == "post_id":
                    response = get_comments_on_post(value)

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get("content-length", 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = {}
        resource, _ = self.parse_url()

        if resource == "login":
            response = login_user(post_body)
        elif resource == "register":
            response = create_user(post_body)
        elif resource == "comments":
            response = create_comment(post_body)
        elif resource == "categories":
            response = create_category(post_body)
        elif resource == "tags":
            response = create_tag(post_body)

        self.wfile.write(json.dumps(response).encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, resource_id) = self.parse_url()

        response = {}

        if resource == "comments":
            response = update_comment(resource_id, post_body)
        elif resource == "categories":
            response = update_category(resource_id, post_body)
        elif resource == "tags":
            response = update_tag(resource_id, post_body)

        if "status" in response and response["status"] == 404:
            self._set_headers(404)
        else:
            self._set_headers(204)

        self.wfile.write(json.dumps(response).encode())

    def do_DELETE(self):
        """Handle DELETE Requests"""
        self._set_headers(204)

        (resource, resource_id) = self.parse_url()

        if resource == "comments":
            delete_comment(resource_id)
        elif resource == "categories":
            delete_category(resource_id)
        elif resource == "tags":
            delete_tag(resource_id)

        self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class"""
    host = ""
    port = 8088
    print("rare-server started!")
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
