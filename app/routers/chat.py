from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from db.db import get_conn

router = APIRouter()


@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Placeholder — RAG pipeline will be wired here in Phase 2."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            # get or create session
            cur.execute(
                """
                INSERT INTO Chat_Session (user_id, course_id)
                VALUES (%s, %s)
                RETURNING session_id
                """,
                (req.user_id, req.course_id),
            )
            session_id = cur.fetchone()[0]

            # log user message
            cur.execute(
                """
                INSERT INTO Chat_Log (session_id, role, content)
                VALUES (%s, 'user', %s)
                RETURNING chat_id
                """,
                (session_id, req.question),
            )
            user_chat_id = cur.fetchone()[0]

            # placeholder answer
            answer = "RAG engine not yet connected. (Phase 2)"
            cur.execute(
                """
                INSERT INTO Chat_Log (session_id, role, content)
                VALUES (%s, 'assistant', %s)
                RETURNING chat_id
                """,
                (session_id, answer),
            )
            chat_id = cur.fetchone()[0]
        conn.commit()

    return ChatResponse(session_id=session_id, chat_id=chat_id, answer=answer)


@router.get("/{session_id}")
def get_chat_history(session_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT chat_id, role, content, sources, created_at
                FROM Chat_Log
                WHERE session_id = %s
                ORDER BY created_at
                """,
                (session_id,),
            )
            rows = cur.fetchall()
    return [
        {"chat_id": r[0], "role": r[1], "content": r[2],
         "sources": r[3], "created_at": str(r[4])}
        for r in rows
    ]
