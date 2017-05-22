class archer_details:
    def __init__(self, sql_row):
        self.id = sql_row[0]
        self.firstname = sql_row[1]
        self.lastname = sql_row[2]
        self.gender = sql_row[3]
        self.byear = sql_row[4]

        self.date = ""
        self.discipline = ""
        self.owns_equipment = False
        self.draw_weight = ""
        self.draw_length = ""
        self.equipment_description = ""
        self.distance = ""
        self.joad_day = ""

    def set_details(self, sql_row):
        assert (self.id == sql_row[0])
        self.date = sql_row[1]
        self.discipline = sql_row[2]
        if sql_row[3] == 1:
            self.owns_equipment = True
        else:
            self.owns_equipment = False
        self.draw_weight = sql_row[4]
        self.draw_length = sql_row[5]
        self.equipment_description = sql_row[6]
        self.distance= sql_row[7]
        self.joad_day = sql_row[8]
