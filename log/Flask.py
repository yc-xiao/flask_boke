1.flask的路由机制?
    @app.route('/', **kw)
    def helloc:
        pass
    ==>
    app.add_url_rule('/', view_func=helloc, **kw)
    ---------------------------------------------
    url, endpoint, views ==> endpoint默认为函数名称
    self.url_map = {'/': 'helloc'}
    self.view_functions = {'helloc': helloc}

2.
