import os
import ga_demo
import unittest
import tempfile
import sqlite3
class GATestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, ga_demo.app.config['DATABASE'] = tempfile.mkstemp()
        self.db_name = ga_demo.app.config['DATABASE']
        ga_demo.app.config['TESTING'] = True
        self.app = ga_demo.app.test_client()
        with ga_demo.app.app_context():
            ga_demo.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(ga_demo.app.config['DATABASE'])

    def execute_query(self, query):
        db = sqlite3.connect(self.db_name)
        cur = db.execute(query)
        cur.row_factory = sqlite3.Row
        rv = cur.fetchall()
        db.close()
        return rv

    def test_empty(self):
        rv = self.app.get('/')
        assert "Add New Archer" in rv.data
        assert "Update Archer Details" in rv.data

    def test_add_archer_post(self):
        rv = self.app.post('/add_archer', data=dict(
        firstname='John',
        lastname='Smith',
        byear='2000',
        gender='Male'
    ), follow_redirects=True)
        assert "New archer was successfully added" in rv.data
        # new archer should appear in drop down
        assert "John Smith" in rv.data

        query = """select id,
                            firstname,
                            lastname,
                            byear,
                            gender
                            day
                            from members"""
        entries = self.execute_query(query)
        assert len(entries) == 1
        assert entries[0][0] == 1
        assert entries[0][1] == "John", entries[0][1]
        assert entries[0][2] == "Smith", entries[0][2]
        assert entries[0][3] == 2000, entries[0][3]
        assert entries[0][4] == "Male", entries[0][4]

def test_add_archer_post(self):
    rv = self.app.get('/edit_details)
    # new archer should appear in drop down
    assert "John Smith" in rv.data

    query = """select id,
                      firstname,
                      lastname,
                      byear,
                      gender
                      day
                    from members"""
    entries = self.execute_query(query)
    assert len(entries) == 1
    assert entries[0][0] == 1
    assert entries[0][1] == "John", entries[0][1]
    assert entries[0][2] == "Smith", entries[0][2]
    assert entries[0][3] == 2000, entries[0][3]
    assert entries[0][4] == "Male", entries[0][4]

if __name__ == '__main__':
    unittest.main()
