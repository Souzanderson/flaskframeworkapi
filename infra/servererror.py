from .log import Log
import json

class ErrorServer(Exception):
    def __init__(self, text_error, status_code=500):
        super().__init__(text_error)
        self.text_error = str(text_error)
        self.status_code = status_code
        
    def get(self):
        Log(f"Error: {self.text_error} => Status Code: {self.status_code}")
    
    @property
    def error(self): return json.dumps({"error": self.text_error, "status": self.status_code}, ensure_ascii=False), self.status_code
    
    def __repr__(self):
        return self.text_error, self.status_code