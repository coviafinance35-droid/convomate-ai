from fastapi.testclient import TestClient
from backend.app.main import app
client=TestClient(app)
def test_session_and_message_flow():
    r=client.post('/api/v1/sessions',json={'summary':'We had a good first date and they said they are busy this week.','who':'Someone I am dating','tone':'Warm','goal':'Keep the conversation going'}); assert r.status_code==200; sid=r.json()['id']
    r=client.post('/api/v1/chat/reply',json={'session_id':sid,'incoming_message':'I had a really nice time too, this week is just packed.'}); assert r.status_code==200; assert r.json()['primary_reply']
def test_gift_is_advice():
    r=client.post('/api/v1/chat/ask',json={'question':'Can I send her a gift?'}); assert r.status_code==200; assert 'gift' in r.json()['answer'].lower()
