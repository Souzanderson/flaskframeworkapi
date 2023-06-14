class Middleware:
    def __init__(self, request):
        self.request = request;
    
    @property
    def token(self):
        try:
            auth = self.request.headers.get("Authorization")
            token = str(auth.split(" ")[1].strip())
            return token
        except Exception as e:
            print(f'[ERROR] => Middleware => getAuthorizationToken{e}')
            return ""
    