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

    def migrate(self):
        try:
            with open("./schema.sql") as script_file:
                script = script_file.read()
                self.cr.executescript(script)
                self.db.commit()
            print("Done")
        except Exception as e:
            print(f"""
Error when migrate
Error: {e}
""")

    def create_server(self, server_id, server_name):
        try:
            self.cr.execute(
                f"""
    INSERT INTO Servers (ServerID, ServerName)
    VALUES (\"{server_id}\", \"{server_name}\");"""
            )
            print(f"server \"{server_name}\" registerd")
        except sqlite3.IntegrityError:
            pass
        self.db.commit()

    def delete_server(self, server_id):
        self.cr.execute(f"""DELETE FROM Servers WHERE ServerID={server_id}""")
        self.db.commit()

    def create_temp_voice_config(self, server_id, room_id, room_name, room_prefix):
        self.cr.execute(
            f"""
INSERT INTO temp_voice_config (ServerID, RoomId, RoomName, RoomPrefix)
VALUES (\"{server_id}\", \"{room_id}\", \"{room_name}\", \"{room_prefix}\");"""
        )
        self.db.commit()

    def create_temp_voice_config(self, room_id):
        self.cr.execute(f'DELETE FROM temp_voice_config WHERE RoomId="{room_id}"')
        self.db.commit()

    def create_temp_room(self, server_id, room_id, owner_id):
        self.cr.execute(
            f"""
INSERT INTO temp_room (ServerID, RoomId, OwnerId)
VALUES (\"{server_id}\", \"{room_id}\", \"{owner_id}\");"""
        )
        self.db.commit()

    def delete_temp_room(self, room_id):
        self.cr.execute(
            f"""
        DELETE FROM temp_room WHERE RoomId=\"{room_id}\""""
        )
        self.db.commit()

    def get_temp_room(self, room_id):
        room = [q for q in self.cr.execute(
            f"""
        SELECT * FROM temp_room WHERE RoomId=\"{room_id}\""""
        )][0]
        return room

    def get_temp_room_2(self, room_id=0, owner_id=0):
        room = [q for q in self.cr.execute(
            f"""
        SELECT * FROM temp_room WHERE RoomId=\"{room_id}\" AND OwnerId=\"{owner_id}\""""
        )][0]
        return room

    def update_temp_room_owner(self, room_id, new_owner_id):
        self.cr.execute(f"""
UPDATE temp_room SET OwnerId={new_owner_id} WHERE RoomId={room_id}
""")
        self.db.commit()

if __name__ == "__main__":
    DataBase().migrate()
