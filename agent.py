from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    input: str
    recommendation: str

# 노드 함수들
def collector_node(state: State):
    return {"input": state["input"]}

def search_node(state: State):
    # 여기서 ChromaDB 검색 로직 추가 예정
    return {"recommendation": "수원 영통 화계 닭갈비 어때요?"}

# 그래프 구성
workflow = StateGraph(State)
workflow.add_node("collector", collector_node)
workflow.add_node("search", search_node)

workflow.set_entry_point("collector")
workflow.add_edge("collector", "search")
workflow.add_edge("search", END)

app = workflow.compile()