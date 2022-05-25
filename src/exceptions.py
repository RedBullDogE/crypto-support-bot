class NoAdmins(Exception):
    def __init__(self):
        super().__init__("There are no admins registered in the system")
