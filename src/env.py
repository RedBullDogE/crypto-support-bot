class Env:
    def __new__(cls, init: bool = False):
        """This makes class a Singleton"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(Env, cls).__new__(cls)
        return cls.instance

    def __init__(self, init: bool = False):
        if not init:
            return
        # dict with user chat ids keys and current_menu values
        self.current_menu: dict = {}
