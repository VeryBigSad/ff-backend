from typing import Any
from datetime import datetime
from sqlalchemy import select, nulls_first, text
from sqlalchemy.dialects.postgresql import insert

from src.database import (
    language,
    meme,
    meme_source,
    meme_raw_telegram,
    meme_raw_vk,
    execute, fetch_one, fetch_all,
)


async def calculate_user_meme_source_stats() -> None:
    # TODO: update only recently active users
    insert_query = f"""
        INSERT INTO user_meme_source_stats (
            user_id, 
            meme_source_id,
            nlikes, 
            ndislikes,
            updated_at
        )
        SELECT 
            R.user_id,
            M.meme_source_id,	
            COUNT(*) FILTER (WHERE reaction_id = 1) nlikes,
            COUNT(*) FILTER (WHERE reaction_id = 2) ndislikes,
            NOW() AS updated_at
        FROM user_meme_reaction R
        INNER JOIN meme M
            ON M.id = R.meme_id
        GROUP BY 1,2
        ON CONFLICT (user_id, meme_source_id) DO 
        UPDATE SET
            nlikes = EXCLUDED.nlikes,
            ndislikes = EXCLUDED.ndislikes,
            updated_at = EXCLUDED.updated_at
    """
    await execute(text(insert_query))
