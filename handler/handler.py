from flask import jsonify, request, send_file, render_template
from infra.servererror import ErrorServer


class Handler:

    def __init__(self, endpoint: str = None):
        self.request = request
        self.method = request.method
        self.endpoint = endpoint

    def handler(self):
        try:
            if self.GET:
                return self.get()
            elif self.POST:
                return self.post()
            elif self.PUT:
                return self.put()
            elif self.DELETE:
                return self.delete()
            else: raise(ErrorServer("Error Method!", 500))
        except ErrorServer as e:
            print(e)
            e.get()
            return e.error

    def get(self):
        raise(ErrorServer("Error Method!", 500))

    def post(self):
        raise(ErrorServer("Error Method!", 500))

    def put(self):
        raise(ErrorServer("Error Method!", 500))

    def delete(self):
        raise(ErrorServer("Error Method!", 500))

    @property
    def GET(self):
        return self.method == "GET"

    @property
    def POST(self):
        return self.method == "POST"

    @property
    def PUT(self):
        return self.method == "PUT"

    @property
    def DELETE(self):
        return self.method == "DELETE"

    @property
    def JSON(self):
        return self.request.get_json()

    @property
    def ARGS(self):
        return self.request.args or {}
    
    def getFormData(self, key):
        return self.request.form.get(key)
    
    def getFormFile(self, key):
        return self.request.files.get(key)

    def sendExcelFile(self, file_data, name="file.xls"):
        return self.sendFile(file_data, name, "application/vnd.ms-excel")

    def sendFile(self, file_data, file_name):
        return send_file(file_data,
                         as_attachment=True,
                         attachment_filename=file_name)

    def template(self, template_name, data):
        return render_template(template_name, data=data)

    def toJson(self, values: dict):
        return jsonify(values)
    
    
