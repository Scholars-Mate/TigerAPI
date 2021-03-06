import pandas as pd
import sqlalchemy as s
import numpy as np
import json

class THApi(object):
    """Uses TigerHacks database to return JSON data"""

    def __init__(self, dbstr):
        """
        Connect to database

        :param dbstr: The [database string](http://docs.sqlalchemy.org/en/latest/core/engines.html) to connect to the database
        """
        self.DB_STR = dbstr
        self.db = s.create_engine(dbstr, poolclass=s.pool.NullPool)
        #If doesn't work, run a test with a SQL command

    def test(self):
        data = {}
        data['test'] = 'success'
        return json.dumps(data)

    def addParticipant(self, data):
        message = {}
        if len(data) == 0:
            message['error'] = 'add error'
            return json.dumps(message)

        fields = ['school', 'grade', 'age', 'major', 'current_location', 'working_place', 'title', 'skills', 'food_allergies', 'gender', 'linkedin', 'github', 'shirt_size', 'transportation', 'lightning_interest', 'professional_interest']
        sql_string = "INSERT INTO Participants ("
        for field in fields:
            sql_string += field + ", "
        sql_string = sql_string[:-2] + ") VALUES ("
        for field in fields:
            if field in data:
                if field == "age" or field == "lightning_interest":
                    sql_string += data[field] + ", "
                else:
                    sql_string += "'" + data[field] + "', "
            else:
                sql_string += "NULL, "
        sql_string = sql_string[:-2] + ")"
        SQL = s.sql.text(sql_string)
        try:
            result = self.db.engine.execute(SQL)
            message['success'] = 'add success'
        except:
            message['error'] = 'add error'
        return json.dumps(message)

    def updateParticipant(self, id, data):
        message = {}
        if len(data) == 0:
            message['error'] = 'update error'
            return json.dumps(message)
        
        sql_string = "UPDATE Participants SET "
        for field in data:
            sql_string += field + "='" + data[field] + "', "
        sql_string = sql_string[:-2] + " WHERE id=" + str(id)
        print(sql_string)
        SQL = s.sql.text(sql_string)
        try:
            result = self.db.engine.execute(SQL)
            message['success'] = 'update success'
        except:
            message['error'] = 'update error'
        return json.dumps(message)

    def getParticipant(self, id):
        SQL = s.sql.text(" SELECT * FROM Participants WHERE id=" + str(id))
        df = pd.read_sql(SQL, self.db)
        if df.empty:
            message = {}
            message['error'] = 'Not found error'
            return json.dumps(message)
        return df.to_json(orient='records', lines=True)

    def getParticipants(self):
        SQL = s.sql.text(""" SELECT * FROM Participants """)
        df = pd.read_sql(SQL, self.db)
        return df.to_json(orient='records')

    def deleteParticipant(self, id):
        SQL = s.sql.text(" DELETE FROM Participants WHERE id=" + str(id))
        result = self.db.engine.execute(SQL)
        message = {}
        if result.rowcount:
            message['success'] = 'delete success'
        else:
            message['error'] = 'Not found error'
        return json.dumps(message)

    def createPrize(self, data):
        message = {}
        if len(data) == 0:
            message['error'] = 'add error'
            return json.dumps(message)
        sid = s.sql.text(" SELECT id FROM Sponsors WHERE company_name='" + data['sponsor_name'] + "'")
        df_id = pd.read_sql(sid, self.db)
        if df_id.empty:
            message = {}
            message['error'] = 'Sponsor not found error'
            return json.dumps(message)
        ids =  df_id.to_dict()
        for id in ids:
            for id1 in ids[id]:
                sponsor_id = ids[id][id1]
        fields = ['prize_description', 'description_to_win', 'number_of_prizes', 'sponsor_id']
        sql_string = "INSERT INTO Prizes ("
        for field in fields:
            sql_string += field + ", "
        sql_string = sql_string[:-2] + ") VALUES ("
        for field in fields:
            if field in data:
                if field == "number_of_prizes":
                    sql_string += data[field] + ", "
                else:
                    sql_string += "'" + data[field] + "', "
            elif field == "sponsor_id":
                print(sponsor_id)
                sql_string += str(sponsor_id) + ", "
            else:
                sql_string += "NULL, "
        sql_string = sql_string[:-2] + ")"
        SQL = s.sql.text(sql_string)
        try:
            result = self.db.engine.execute(SQL)
            message['success'] = 'add success'
        except:
            message['error'] = 'add error'
        return json.dumps(message)

    def getPrize(self, id):
        SQL = s.sql.text(" SELECT * FROM Prizes WHERE id=" + str(id))
        df = pd.read_sql(SQL, self.db)
        if df.empty:
            message = {}
            message['error'] = 'Not found error'
            return json.dumps(message)
        return df.to_json(orient='records', lines=True)

    def getPrizes(self):
        SQL = s.sql.text(""" SELECT * FROM Prizes """)
        df = pd.read_sql(SQL, self.db)
        return df.to_json(orient='records')

    def deletePrize(self, id):
        SQL = s.sql.text(" DELETE FROM Prizes WHERE id=" + str(id))
        result = self.db.engine.execute(SQL)
        message = {}
        if result.rowcount:
            message['success'] = 'delete success'
        else:
            message['error'] = 'Not found error'
        return json.dumps(message)
    
    def updatePrize(self, id, prizeDescription, descriptionToWin, numberOfPrizes, sponsorId):
        SQL_string = "UPDATE Prizes SET"
        if prizeDescription is not None:
            SQL_string.append("prize_description =" + str(prizeDescription))
        if descriptionToWin is not None:
            SQL_string.append(" description_to_win=" + str(descriptionToWin))
        if numberOfPrizes is not None:
            SQL_string.append(" number_of_prizes=" + str(numberOfPrizes))
        if sponsorId is not None:
            SQL_string.append(" sponsor_id=" + str(sponsorId))
        SQL = s.sql.text( SQL_string + " WHERE id =" + str(id))
        result = self.db.engine.execute(SQL)
        message = {}
        if result.rowcount:
            message['success'] = 'Update Success'
        else:
            message['error'] = result
        return json.dumps(message)
        
    
    
    
    
    

