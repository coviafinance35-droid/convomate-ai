import json, sqlite3, uuid
from datetime import datetime, timezone
from pathlib import Path
DB = Path(__file__).resolve().parents[2] / 'convomate.db'

def now(): return datetime.now(timezone.utc).isoformat()
def conn():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    c.executescript('''create table if not exists sessions(id text primary key,title text not null,summary text not null,who text,relationship text,tone text,goal text,created_at text,updated_at text); create table if not exists messages(id text primary key,session_id text,role text,content text,message_type text,created_at text); create table if not exists drafts(id text primary key,session_id text,content text,draft_type text,tone text,created_at text);''')
    return c

def create_session(data):
    sid=str(uuid.uuid4()); t=now(); title=(data.summary[:48]+'…') if len(data.summary)>48 else data.summary
    with conn() as c: c.execute('insert into sessions values(?,?,?,?,?,?,?,?,?)',(sid,title,data.summary,data.who,data.relationship,data.tone,data.goal,t,t));
    return get_session(sid)
def get_session(sid):
    with conn() as c:
        row=c.execute('select * from sessions where id=?',(sid,)).fetchone()
        return dict(row) if row else None
def list_sessions():
    with conn() as c: return [dict(r) for r in c.execute('select * from sessions order by updated_at desc limit 20')]
def update_session(sid, data):
    old=get_session(sid)
    if not old: return None
    merged={k:(v if v is not None else old[k]) for k,v in data.model_dump().items()}
    t=now()
    with conn() as c: c.execute('update sessions set summary=?,who=?,relationship=?,tone=?,goal=?,updated_at=? where id=?',(merged['summary'],merged['who'],merged['relationship'],merged['tone'],merged['goal'],t,sid))
    return get_session(sid)
def delete_session(sid):
    with conn() as c: c.execute('delete from messages where session_id=?',(sid,)); c.execute('delete from drafts where session_id=?',(sid,)); c.execute('delete from sessions where id=?',(sid,))
def add_message(sid, role, content, message_type):
    with conn() as c: c.execute('insert into messages values(?,?,?,?,?,?)',(str(uuid.uuid4()),sid,role,content,message_type,now()))
def recent_messages(sid):
    with conn() as c: return [dict(r) for r in c.execute('select * from messages where session_id=? order by created_at desc limit 10',(sid,))][::-1]
def add_draft(sid, content, dtype, tone):
    did=str(uuid.uuid4())
    with conn() as c: c.execute('insert into drafts values(?,?,?,?,?,?)',(did,sid,content,dtype,tone,now()))
    return did
def list_drafts():
    with conn() as c: return [dict(r) for r in c.execute('select * from drafts order by created_at desc limit 30')]
