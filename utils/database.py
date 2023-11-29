import sqlite3, os


class DataBase:
    def __init__(self):
        self.db, self.cr = self.init_db()

    def init_db(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_directory)
        database_path = os.path.join(parent_directory, "database.sqlite3")
        db = sqlite3.connect(database_path)
        cr = db.cursor()
        return db, cr

    def delete_server(self, server_id):
        self.cr.execute(f"""DELETE FROM Servers WHERE ServerID={server_id}""")
        self.db.commit()

    def create_server(self, server_id, server_name):
        self.cr.execute(
            f"""
INSERT INTO Servers (ServerID, ServerName)
VALUES (\"{server_id}\", \"{server_name}\");"""
        )
        self.db.commit()

    def create_db(self):
        with open("./schema.sql") as script_file:
            script = script_file.read()
            self.cr.executescript(script)
            self.db.commit()


if __name__ == "__main__":
    DataBase().create_db()
