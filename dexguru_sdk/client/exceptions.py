class RequestException(Exception):
    def __init__(self, e):
        try:
            self.msg = f"Check field {e['detail'][0]['loc'][1]}: {e['detail'][0]['msg']}"
        except (IndexError, TypeError, KeyError):
            self.msg = e.get('detail', e.get('message', e))

    def __str__(self):
        return self.msg
