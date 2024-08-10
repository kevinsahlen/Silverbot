import discord
import mysql.connector
import logging
from os import getenv

logger = logging.getLogger(__name__)

# creates database connection
def db():
    return mysql.connector.connect(
        port=getenv('DB_PORT'),
        host=getenv('DB_HOST'),
        user=getenv('DB_USER'),
        password=getenv('DB_PW'),
        database=getenv('DB_NAME'))

# retrieves timezone for user from database
def getTimezone(user: discord.User):
    with db() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT timezone FROM users WHERE discordID = %s', (user.id,))
            result = cursor.fetchone()
            if result is None:
                return 'Europe/Stockholm'
            return result[0]

# Inserts or updates timezone for user in database
def setTimezone(user: discord.User, userinput: str):
    try:
        with db() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT timezone FROM users WHERE discordID = %s', (user.id,))
                result = cursor.fetchone()
                if result is None:
                    cursor.execute('INSERT INTO users (discordID, discordName, timezone) VALUES (%s, %s, %s)', (user.id, user.name, userinput))
                else:
                    cursor.execute('UPDATE users SET timezone = %s WHERE discordID = %s', (userinput, user.id))
                conn.commit()
                return True, userinput
    except mysql.connector.Error as e:
        logger.error(f'Failed to set country code for user {user.id}: {e}')
        raise