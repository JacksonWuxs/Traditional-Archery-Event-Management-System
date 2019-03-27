from sqlite3 import connect
from time import localtime
from warnings import warn


class database:
    def __init__(self, addr):
        self._conn = connect(addr)
        self._cur = self._conn.cursor()
    
    def _execute(self, command):
        try:
            self._cur.execute(command.decode('utf-8'))
        except Exception, e:
            warn('FAILED TO: %s BECAUSE: %s' % (command, e), stacklevel=3)
            return False
        else:
            self._conn.commit()
            return True

    def _execute2(self, command):
        try:
            self._cur.execute(command)
        except Exception, e:
            warn('FAILED TO: %s BECAUSE: %s' % (command, e), stacklevel=3)
            return False
        else:
            return self._cur.fetchall()
        
    def _get_date(self):
        t = map(str, localtime())
        return t[0] + t[1].zfill(2) + t[2].zfill(2)

    def create_user_table(self):
        self._execute('CREATE TABLE users (ID INTEGER PRIMARY KEY AUTOINCREMENT, Name Char(30), Psd Char(30), Email Char(50), Date Int(8), Money real)')
        self.add_user(1, 'admin', '123', 'test@163.com')

    def add_user(self, id, user, psd, email, confirm_code=''):
        date = self._get_date()
        command = 'INSERT INTO users (ID, Name, Psd, Email, Date, Money) VALUES ' + \
                  '(%s, "%s", "%s", "%s", %s, %s)' % (id, user, psd, email, date, 0)
        return self._execute(command)

    def select(self, condition=None, order=None, limit=None):
        command = 'SELECT * FROM users' 
        if condition:
            command += ' WHERE %s' % condition
        if order:
            command += ' ORDER BY %s' % order
        if limit:
            command += ' LIMIT %d' % limit
        return self._execute2(command)

    def exit(self):
        self._conn.close()
