import subprocess
import tempfile

class Client(object):
    
    def __init__(self, user, password, host, db, port=3306):
        self.user = user
        self.password = password
        self.host = host
        self.db = db
        self.port = str(port)
        self.args = ['mysql', '-u'+user, '-p'+password, '--database='+db, '--port='+str(port), '--host='+host, '--skip-column-names', '--skip-line-numbers', '-e']
    
    def query(self, sql):
        query_args = self.args + [sql]
        #mysql = Popen(query_args, stdout=PIPE)
        #results, err = mysql.communicate()
        #optimization from
        #http://stackoverflow.com/questions/13835055/python-subprocess-check-output-much-slower-then-call
        with tempfile.NamedTemporaryFile() as f:
            subprocess.check_call(query_args, stdout=f, stderr=subprocess.STDOUT)
            f.seek(0)
            results = f.read()

        rows = [tuple(row.split()) for row in results.split('\n')]
        return rows
