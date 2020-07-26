# -*- coding: utf-8 -*-
import flask
import requests
# from flask_cors import CORS

app = flask.Flask(__name__)
# CORS(app)

# method_requests_mapping = {
#     'GET': requests.get,
#     'HEAD': requests.head,
#     'POST': requests.post,
#     'PUT': requests.put,
#     'DELETE': requests.delete,
#     'PATCH': requests.patch,
#     'OPTIONS': requests.options,
# }


# example nodejs install link https://wuecampus2.uni-wuerzburg.de/moodle/mod/url/view.php?id=1351062
# tested like this fetch('http://127.0.0.1:5000/wuecampusViewPhp/1351062', {credentials: 'include'}).then((r) => console.log(r))
@app.route('/wuecampusViewPhp/<path:viewId>') #methods=method_requests_mapping.keys()
def urlResolver(viewId):
    wuecampus_base_url = "https://wuecampus2.uni-wuerzburg.de/moodle/mod/url/view.php?id="
    wuecampus_url = wuecampus_base_url + viewId


    print(flask.request.cookies)

    request_response = requests.request(
        method=flask.request.method,
        url=wuecampus_url,
        headers={key: value for (key, value) in flask.request.headers if key != 'Host'},
        data=flask.request.get_data(),
        cookies=flask.request.cookies,
        allow_redirects=True)
    # print(response.text)

    if request_response.history:
        print("Request was redirected")
        for resp in request_response.history:
            print(resp.status_code, resp.url)
        print("Final destination:")
        print(request_response.status_code, request_response.url)
    else:
        print("Request was not redirected")

    # print(resp.url)
    # return response.url
    flask_response = flask.Response(flask.stream_with_context(request_response.iter_content()),
                            content_type=request_response.headers['content-type'],
                            status=request_response.status_code)
    #TODO reactivate this
    flask_response.headers['Access-Control-Allow-Origin'] = 'https://wuecampus2.uni-wuerzburg.de'
    flask_response.headers['Origin'] = 'https://wuecampus2.uni-wuerzburg.de'
    # flask_response.headers['Access-Control-Allow-Origin'] = '*'
    flask_response.headers['Access-Control-Allow-Credentials'] = 'true'
    return flask_response


    # requests_function = method_requests_mapping[flask.request.method]
    # request = requests_function(wuecampus_url, stream=True, params=flask.request.args, cookies=flask.request.cookies)
    # print(request.text)
    # response = flask.Response(flask.stream_with_context(request.iter_content()),
    #                         content_type=request.headers['content-type'],
    #                         status=request.status_code)
    # response.headers['Access-Control-Allow-Origin'] = '*'
    # return response

if __name__ == '__main__':
    app.debug = True
    app.run()
