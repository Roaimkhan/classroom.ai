class GCRError(Exception):
    """Base class for all GCR errors"""
    pass

class GCRAuthError(GCRError):
    """Authentication/Authorization failed (401/403/invalid_grant)"""
    def __init__(self,msg):
        self.msg = msg
        super().__init__(self.msg)

class GCRConnectionError(GCRError):
    """Network-level errors (timeouts, connection issues)"""
    def __init__(self,msg):
        self.msg = msg
        super().__init__(self.msg)    

class GCRRateLimitError(GCRError):
    """Too many requests (429)"""
    def __init__(self,msg):
        self.msg = msg
        super().__init__(self.msg)

class GCRServerError(GCRError):
    """Server-side transient errors (500, 502, 503, 504)"""
    def __init__(self,msg):
        self.msg = msg
        super().__init__(self.msg)
    

class GCRClientError(GCRError):
    """Other client errors (400, 404, etc.)"""
    def __init__(self,msg):
        self.msg = msg
        super().__init__(self.msg)

class GCRBotError(GCRError):
    """Unknown/unexpected errors"""
    def __init__(self,msg):
        self.msg = msg
        super().__init__(self.msg)


def gc_error_mapper(error):
    if error in [500,502,503,504]:
        return GCRServerError
    
    elif error in [400,404,422,409]:
        return GCRClientError
    
    elif error in [401,403]:
        return GCRAuthError
    
    elif error in [401,403]:
        return GCRAuthError
    
    elif error == 429:
        return GCRRateLimitError
    
    elif error == 408:
        return GCRConnectionError
    
if __name__ == "__main__":
    print(gc_error_mapper(500) == GCRServerError)

    