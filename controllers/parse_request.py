from flask import request


def get_request_data():
    """
    Get keys & values from request (Note that this method should parse requests with content type "application/x-www-form-urlencoded")
    """
    #if request.form:
    #data = request.form.to_dict()
    data = dict(request.form)
    return data
    #else:
        #return {}
