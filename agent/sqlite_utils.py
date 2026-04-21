import sqlite3
from datetime import datetime
from langgraph.checkpoint.sqlite import SqliteSaver
from logger_config import setup_logging
setup_logging()

import logging

logger = logging.getLogger(__name__)


def init_db():
    logger.info("Entering init_db")
    conn = sqlite3.connect("db\chats.db")
    cursor = conn.cursor()
    print(cursor)
    cursor.execute(
        """ 
            CREATE TABLE IF NOT EXISTS chats(
                thread_id TEXT PRIMARY KEY,
                user_id TEXT ,
                title TEXT,
                updated_at TIMESTAMP
            )
        """
    )

    conn.commit()
    logger.info("Table created succesully!")
    conn.close()


def init_checkpointer():
    conn = sqlite3.connect('db\checkpoints.db', check_same_thread=False)
    saver = SqliteSaver(conn=conn)
    saver.setup()
    return saver


def upsert_chat(thread_id,user_id,final_text):
    logger.info(f"Entering upsert_chat->thread_id: {thread_id}, user:id:{user_id}, title:{final_text}")
    conn = sqlite3.connect("db\\chats.db")
    cursor = conn.cursor()
    title = final_text[:40] 
    cursor.execute("""
            INSERT INTO chats (thread_id, user_id, title, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(thread_id) DO UPDATE SET
                updated_at=excluded.updated_at
        """, (thread_id, user_id, title, datetime.utcnow()))

    conn.commit()