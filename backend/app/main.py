import os, time
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.schemas import *
from backend.app import store
from backend.app.agents.graph import GRAPH
app=FastAPI(title='ConvoMate AI API',version='1.0.0')
origins=os.getenv('CORS_ORIGINS','http://localhost:5173,http://localhost:3000').split(',')
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
rate={}
@app.middleware('http')
async def limiter(request:Request, call_next):
    if request.url.path.startswith('/api/'):
        ip=request.client.host if request.client else 'unknown'; now=time.time(); hits=[t for t in rate.get(ip,[]) if now-t<60]
        if len(hits)>=60: raise HTTPException(429,'Too many requests; try again in a minute.')
        hits.append(now); rate[ip]=hits
    return await call_next(request)
@app.get('/health')
def health(): return {'status':'ok','service':'convomate-ai','model_configured':bool(os.getenv('OPENAI_API_KEY'))}
@app.post('/api/v1/sessions',response_model=SessionOut)
def create(payload:SessionCreate): return store.create_session(payload)
@app.get('/api/v1/sessions',response_model=list[SessionOut])
def sessions(): return store.list_sessions()
@app.get('/api/v1/sessions/{sid}',response_model=SessionOut)
def session(sid:str):
    item=store.get_session(sid)
    if not item: raise HTTPException(404,'Session not found')
    return item
@app.patch('/api/v1/sessions/{sid}',response_model=SessionOut)
def patch(sid:str,payload:SessionUpdate):
    item=store.update_session(sid,payload)
    if not item: raise HTTPException(404,'Session not found')
    return item
@app.delete('/api/v1/sessions/{sid}')
def remove(sid:str): store.delete_session(sid); return {'ok':True}
def run(intent,payload, text):
    s=store.get_session(payload.session_id)
    if not s: raise HTTPException(404,'Session not found')
    context={'summary':s['summary'],'who':s['who'],'relationship':s['relationship'],'tone':payload.tone or s['tone'],'goal':s['goal'],'latest':payload.incoming_message,'history':store.recent_messages(payload.session_id)}
    store.add_message(payload.session_id,'user',text,'input'); out=GRAPH.invoke({'intent':intent,'context':context,'input':text})['output']
    return out
@app.post('/api/v1/chat/reply',response_model=ReplyResult)
def reply(p:GenerationRequest):
    if not p.incoming_message: raise HTTPException(422,'incoming_message is required')
    out=run('reply',p,p.incoming_message); did=store.add_draft(p.session_id,out['primary_reply'],'reply',out.get('tone','Natural')); out['draft_id']=did; store.add_message(p.session_id,'assistant',out['primary_reply'],'draft'); return out
@app.post('/api/v1/chat/message',response_model=ReplyResult)
def message(p:GenerationRequest):
    if not p.intention: raise HTTPException(422,'intention is required')
    out=run('message',p,p.intention); did=store.add_draft(p.session_id,out['primary_reply'],'message',out.get('tone','Natural')); out['draft_id']=did; return out
@app.post('/api/v1/chat/next-topic',response_model=TopicResult)
def topic(p:GenerationRequest):
    out=run('topic',p,p.incoming_message or p.intention or 'Continue the conversation naturally'); did=store.add_draft(p.session_id,out['suggested_message'],'topic',p.tone or 'Natural'); out['draft_id']=did; return out
@app.post('/api/v1/chat/ask',response_model=AdviceResult)
def ask(p:AskRequest):
    context={}
    if p.session_id and store.get_session(p.session_id): context=store.get_session(p.session_id)
    out=GRAPH.invoke({'intent':'advice','context':context,'input':p.question})['output'];
    if p.session_id: store.add_message(p.session_id,'user',p.question,'advice'); store.add_message(p.session_id,'assistant',out['answer'],'advice')
    return out
@app.post('/api/v1/chat/revise',response_model=ReplyResult)
def revise(p:ReviseRequest):
    out=run('message',GenerationRequest(session_id=p.session_id,tone='Natural'),f'Revise this draft: {p.draft}\nUser instruction: {p.instruction}'); return out
@app.get('/api/v1/drafts')
def drafts(): return store.list_drafts()
# Serve the compiled React app when present; API and health stay above this mount.
dist=Path(__file__).resolve().parents[2]/'dist'
if dist.exists():
    app.mount('/assets',StaticFiles(directory=dist/'assets'),name='assets')
    @app.get('/{path:path}')
    def spa(path:str):
        if path=='manus-routes.json': return FileResponse(Path(__file__).resolve().parents[2]/'public/manus-routes.json')
        return FileResponse(dist/'index.html')
