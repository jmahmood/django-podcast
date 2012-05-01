class baseDocumentOutput(object):
    def authorize(self):
        raise NotImplementedError( "Should have implemented this" )

    def get(self): # load articles
        raise NotImplementedError( "Should have implemented this" )

    # An empty function that you can define to filter messages or perform any transformations necessary before output is made.
    def prehook(self):
        pass
    
    # An empty function that you can define to filter messages or perform any transformations necessary before output is made.
    def posthook(self):
        pass
    
    def output_errors(self):
        raise NotImplementedError( "Should have implemented this" )
    
    def output_success(self):
        raise NotImplementedError( "Should have implemented this" )

    def __call__(self, request, *args, **kwargs):
        self.request = request
        if not self.authorize():
            return self.output_errors(request)
        
        self.args = args
        self.kwargs = kwargs
        
        self.statusCode = 0
        self.documents = False
        self.errors = []

        self.prehook()
        self.get()
        self.posthook()

        if self.statusCode == 1:
            return self.output_success()
        
        return self.output_errors()
