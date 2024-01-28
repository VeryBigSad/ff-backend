from typing import Any
from sqlalchemy import text

from src.database import fetch_all
from src.recommendations.utils import exclude_meme_ids_sql_filter


# "lr" - like rate
# I'm not sure about the naming, will change later
async def sorted_by_user_source_lr_meme_lr_meme_age(
    user_id: int,
    limit: int = 10,
    exclude_meme_ids: list[int] = [],
) -> list[dict[str, Any]]:
    query = f"""
        SELECT 
            M.id, M.type, M.telegram_file_id, M.caption,
            'sorted_by_user_source_lr_meme_lr_meme_age' as recommended_by
        FROM meme M 
        LEFT JOIN user_meme_reaction R 
            ON R.meme_id = M.id
            AND R.user_id = {user_id}
        INNER JOIN user_language L
            ON L.user_id = {user_id}
            AND L.language_code = M.language_code
			
		LEFT JOIN user_meme_source_stats UMSS 
            ON UMSS.user_id = {user_id}
            AND UMSS.meme_source_id = M.meme_source_id
        LEFT JOIN meme_stats MS
            ON MS.meme_id = M.id
			
        WHERE 1=1
            AND M.status = 'ok'
            AND R.meme_id IS NULL
            {exclude_meme_ids_sql_filter(exclude_meme_ids)}

        ORDER BY 1
            * COALESCE((UMSS.nlikes + 1) / (UMSS.ndislikes + 1), 0.5)
            * COALESCE((MS.nlikes + 1) / (MS.ndislikes + 1), 0.5)
            * COALESCE(MS.raw_impr_rank, 99999)
            * COALESCE(age_days * (-1), 0.1)
		
        LIMIT {limit}
    """
    res = await fetch_all(text(query))
    return res

