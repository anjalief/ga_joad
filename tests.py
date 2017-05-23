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
        self.reset_db()


    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(ga_demo.app.config['DATABASE'])

    # DB helpers
    def reset_db(self):
        with ga_demo.app.app_context():
            ga_demo.init_db()

    def execute_query(self, query):
        db = sqlite3.connect(self.db_name)
        cur = db.execute(query)
        cur.row_factory = sqlite3.Row
        rv = cur.fetchall()
        db.close()
        return rv

    def check_archer_details(self, expected_rows):
        query = """select id,
                        discipline,
                        owns_equipment,
                        draw_weight,
                        draw_length,
                        equipment_description,
                        distance,
                        joad_day
                        from member_details order by date desc"""
        entries = self.execute_query(query)
        assert len(entries) == len(expected_rows)
        for i in range(0, len(expected_rows)):
            for j in range(0, len(expected_rows[0])):
                assert entries[i][j] == expected_rows[i][j], entries[i][j]

    # util helpers
    def add_archer_helper(self,
                          firstname_='John',
                          lastname_='Smith',
                          byear_='2000',
                          gender_='Male',
                          follows_redirect_=True):
        return self.app.post('/add_archer', data=dict(
                            firstname=firstname_,
                            lastname=lastname_,
                            byear=byear_,
                            gender=gender_
                            ), follow_redirects=follows_redirect_)

    # Base tests
    def test_empty(self):
        rv = self.app.get('/')
        assert "Add New Archer" in rv.data
        assert "Update Archer Details" in rv.data

    def test_add_archer_post(self):
        self.reset_db()
        rv = self.add_archer_helper()
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

    def test_add_two_archers(self):
        self.reset_db()
        rv = self.add_archer_helper()
        assert "New archer was successfully added" in rv.data
        # both new archers should appear in drop down

        rv = self.add_archer_helper(firstname_='Alice')
        assert "John Smith" in rv.data
        assert "Alice Smith" in rv.data


    def test_get_edit_details(self):
        self.reset_db()
        rv = self.add_archer_helper()
        assert "John Smith" in rv.data

        rv = self.app.get('/edit_details?name_selecter=1')
        # prepopulating fields is done in javascript, can't test here
        # just sanity check that some fields exist
        assert "Primary Discipline:" in rv.data
        assert "Primary Day:" in rv.data
        assert "Saturday" in rv.data
        assert "Compound" in rv.data

    def test_get_edit_details(self):
        self.reset_db()
        rv = self.add_archer_helper()
        assert "John Smith" in rv.data

        rv = self.app.post('/edit_details', data=dict(
                            id="1",
                            discipline="Compound",
                            owns_equipment="",
                            draw_weight=10,
                            draw_length=25,
                            equipment_description="blah",
                            distance_selecter=10,
                            day_selecter="Saturday"
                            ), follow_redirects=True)
        assert 'New data was successfully added' in rv.data
        expected_row_1=[1, "Compound", 1, 10, 25, "blah", 10, "Saturday"]
        self.check_archer_details([expected_row_1])

        rv = self.app.post('/edit_details', data=dict(
                            id="1",
                            discipline="Recurve",
                            draw_weight=10,
                            draw_length=25,
                            equipment_description="blah",
                            distance_selecter=10,
                            day_selecter="Saturday"
                            ), follow_redirects=True)
        expected_row_2=[1, "Recurve", 0, 10, 25, "blah", 10, "Saturday"]
        self.check_archer_details([expected_row_1, expected_row_2])




if __name__ == '__main__':
    unittest.main()
