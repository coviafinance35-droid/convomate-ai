from typing import TypedDict, Any
import os, json, re
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langgraph.graph import StateGraph, END
except Exception:
    ChatOpenAI = None
from backend.app.prompts.system import REPLY_SYSTEM, TOPIC_SYSTEM, ADVICE_SYSTEM

class ConversationState(TypedDict, total=False):
    intent: str; context: dict; input: str; output: dict

def fallback(intent, context, text):
    tone=context.get('tone') or 'Natural'; latest=context.get('latest') or ''
    if intent=='advice':
        q=text.lower();
        if 'gift' in q: return {'answer':'A gift can be thoughtful when it matches the stage of the relationship and the person’s preferences. Keep it low-pressure and easy to receive rather than using it to solve uncertainty.','practical_options':['A small item tied to something they mentioned','A simple shared experience','A note that makes clear there is no expectation'],'relevant_caveats':['Consider whether gifts are already normal between you','Avoid anything expensive or overly intimate if the relationship is new'],'optional_next_action':'If you want, I can help you write a low-pressure note to go with it.'}
        return {'answer':'Start with the clearest, kindest version of what you mean. Give the other person room to respond, and treat their response as information rather than a verdict on your worth.','practical_options':['Say what you want directly','Ask one specific open question','Match their pace and leave space'],'relevant_caveats':['You cannot control the other person’s reaction','If they ask for space, respect it'],'optional_next_action':'I can help you turn this into a message if you share the situation.'}
    if intent=='topic': return {'suggested_message':f"That sounds like a good thread to keep exploring — what part of it has been most interesting for you lately?",'rationale':'It follows the current conversation instead of switching topics abruptly, and it invites a specific answer.','follow_up_question':'What detail did they mention that you could naturally pick up?','alternative_topic':'Ask about a small plan they are looking forward to this week.'}
    primary = f"I hear you. I’d keep it {tone.lower()} and simple: {text.strip().rstrip('.')}. What feels most natural for you to say next?"
    return {'primary_reply':primary,'alternatives':[f"That makes sense — I’d say it plainly and give them room to respond.",f"I’m glad you told me. I’d love to hear more when you feel like sharing."],'tone':tone,'short_explanation':'A concise draft that keeps the user’s intention while leaving room for a natural reply.'}

def build_graph():
    def route(s): return s
    def generate(s):
        if not ChatOpenAI or not os.getenv('OPENAI_API_KEY'): s['output']=fallback(s['intent'],s['context'],s['input']); return s
        schema = '{"primary_reply":"...","alternatives":["..."],"tone":"...","short_explanation":"..."}' if s['intent'] in ('reply','message') else '{"suggested_message":"...","rationale":"...","follow_up_question":"...","alternative_topic":"..."}'
        system = REPLY_SYSTEM if s['intent'] in ('reply','message') else TOPIC_SYSTEM
        if s['intent']=='advice': system=ADVICE_SYSTEM
        prompt=ChatPromptTemplate.from_messages([('system',system+f" Return valid JSON matching this shape: {schema}"),('human','Context: {context}\nUser input: {input}')])
        model=ChatOpenAI(model=os.getenv('OPENAI_MODEL','gpt-4o-mini'),temperature=.7,timeout=25,max_tokens=500)
        try:
            raw=model.invoke(prompt.format_messages(context=json.dumps(s['context']),input=s['input'])).content
            raw=re.sub(r'^```json|```$','',raw.strip()).strip(); s['output']=json.loads(raw)
        except Exception: s['output']=fallback(s['intent'],s['context'],s['input'])
        return s
    g=StateGraph(ConversationState); g.add_node('route',route); g.add_node('generate',generate); g.set_entry_point('route'); g.add_edge('route','generate'); g.add_edge('generate',END); return g.compile()
GRAPH=build_graph()
