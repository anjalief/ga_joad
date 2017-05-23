import datetime

def get_joad_age_class(birth_year):
    current_year = datetime.datetime.now().year
    # age archer is turning this year
    effective_age = current_year - birth_year

    if effective_age > 20:
        return "Senior"
    elif effective_age > 17:
        return "Junior"
    elif effective_age > 14:
        return "Cadet"
    elif effective_age > 12:
        return "Cub"
    elif effective_age > 9:
        return "Bowman"
    return "Yeoman"

class archer_details:
    def __init__(self, sql_row):
        self.id = sql_row[0]
        self.firstname = sql_row[1]
        self.lastname = sql_row[2]
        self.byear = sql_row[3]
        self.gender = sql_row[4]

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
        self.joad_age_class = get_joad_age_class(self.byear)
