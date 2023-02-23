"""persistence module"""
import datetime
import sqlite3
from utils.model.image import Image


class Persistence:
    """persistence class"""

    def __init__(self, path):
        self.path = path
        self.con = sqlite3.connect(self.path)
        self.con.row_factory = self.row_to_dict
        self.cur = self.con.cursor()

    def row_to_dict(self, cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
        """row_to_dict"""
        data = {}
        for idx, col in enumerate(cursor.description):
            data[col[0]] = row[idx]
        return data

    def init(self):
        """init"""
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS image
            (
                id VARCHAR(700) PRIMARY KEY, 
                namespace VARCHAR(100), 
                resource VARCHAR(300), 
                image VARCHAR(200),
                tag VARCHAR(100), 
                tag_digest VARCHAR(500), 
                last_check_date DATETIME
            )
            """
        )
        self.con.commit()

    def get_image_by_id(self, image_id):
        """get_image_by_id"""
        result = self.cur.execute(f"SELECT * FROM image WHERE id='{image_id}'")
        return result.fetchone()

    def add_new_image(self, data: Image):
        """add_new_image"""

        self.cur.execute(
            f"""INSERT INTO image (id, namespace,resource, image, tag, tag_digest, last_check_date)
                VALUES (
                        '{data.image_id}',
                        '{data.namespace}',
                        '{data.resource}',
                        '{data.image}',
                        '{data.tag}',
                        '{data.tag_digest}',
                        '{get_date_time()}');"""
        )
        self.con.commit()

    def update_image_digest(self, image_id, new_tag_digest):
        """update_image_digest"""
        self.cur.execute(
            f"""
            UPDATE image SET tag_digest='{new_tag_digest}' WHERE id='{image_id}'
            """
        )
        self.con.commit()

    def update_image_last_check_data(self, image_id):
        """update_image_last_check_data"""
        self.cur.execute(
            f"""
            UPDATE image SET last_check_date='{get_date_time()}' WHERE id='{image_id}'
            """
        )

        self.con.commit()


def get_date_time():
    """get_date_time"""
    now = datetime.datetime.utcnow()
    return now.strftime("%Y-%m-%d %H:%M:%S")
