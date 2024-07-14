import discord
import mysql.connector

class Database:
    @staticmethod
    def db():
        return mysql.connector.connect(
            host=getenv('DB_HOST'),
            port=getenv('DB_PORT'),
            user=getenv('DB_USER'),
            password=getenv('DB_PW'),
            database=getenv('DB_NAME'))
    
    @staticmethod
    def getCountryCode(user):
        db = Database.db()
        cursor = db.cursor()
        cursor.execute("SELECT country FROM users WHERE discordID = %s", (user.id,))
        result = cursor.fetchone()
        db.close()
        if result is None:
            return None
        return result
    
    def setCountryCode(user, code):
        db = Database.db()
        cursor = db.cursor()
        cursor.execute("SELECT country FROM users WHERE discordID = %s", (user.id,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO users (discordID, discordName, country) VALUES (%s, %s, %s)", (user.id, user.name, code))
        else:
            cursor.execute("UPDATE users SET country = %s WHERE discordID = %s", (code, user.id))
        db.commit()
        cursor.close()
        db.close()