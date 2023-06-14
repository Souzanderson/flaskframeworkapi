from middlewares.middleware import Middleware
from infra.servererror import ErrorServer

class MiddlewareAuth(Middleware):
    
    def authenticate(self):
        try:
            res =  True
            if not self.user.get("authenticate"):
                raise(Exception("Usuário não identificado!"))
        except Exception as e:
            print(e)
            raise(ErrorServer(f"Erro de Autorização => {str(e)}", 401))
        
    def authenticate_master(self):
        try:
            
            if not self.user.get("master"):
                raise(Exception("Usuário sem permissão suficiente!"))
        except Exception as e:
            print(e)
            raise(ErrorServer(f"Erro de Autorização => {str(e)}", 401))
        
    @property
    def user(self):
        try:
            res =  {"user": "user", "hash": self.token, "authenticate": True, "master": True}
            return res
        except Exception as e:
            print(e)
            raise(ErrorServer(f"Erro de Autorização ao selecionar User => {str(e)}", 401))