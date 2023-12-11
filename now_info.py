class User:
    Uid = None
    Uname = None

    def __init__(self, uid, uname):
        self.Uid = uid
        self.Uname = uname


class Contest:
    Cid = None

    def __init__(self):
        pass


class Problem:
    Pid = None

    def __init__(self):
        pass


nowUser = None
nowContest = None
Problem = None
