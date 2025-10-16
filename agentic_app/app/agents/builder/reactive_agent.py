from typing import Dict, Any, List, Optional, TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from agents.llm_factory import LLMFactory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

QueryType = Literal["greeting", "get", "filter", "groupby", "aggregate", "sort", "top", "bottom", "count", "ambiguous"]
EntityType = Literal["lead", "case", "account", "opportunity"]

class CRMQueryResult(TypedDict):
    entity_type: EntityType
    action: QueryType
    fields: List[str]
    conditions: Optional[Dict[str, Any]]
    result: Optional[List[Dict[str, Any]]]
    welcome_message: str
    end_message: str
    clarification_needed: bool
    clarification_message: Optional[str]
    error: Optional[str]

class ReActiveAgentState(TypedDict):
    query: str
    context: List[Dict[str, Any]]
    entity_type: Optional[EntityType]
    action: Optional[QueryType]
    fields: List[str]
    conditions: Dict[str, Any]
    result: Optional[List[Dict[str, Any]]]
    clarification_needed: bool
    clarification_message: Optional[str]
    output: Optional[CRMQueryResult]
    error: Optional[str]

class ReActiveAgent:
    def __init__(self, context: List[Dict[str, Any]]):
        self.context = context
        self.llm = LLMFactory.open_ai()
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        workflow = StateGraph(ReActiveAgentState)
        
        # Add nodes
        workflow.add_node("classify_query", self.classify_query)
        workflow.add_node("extract_fields", self.extract_fields)
        workflow.add_node("handle_ambiguity", self.handle_ambiguity)
        workflow.add_node("process_query", self.process_query)
        workflow.add_node("finalize_output", self.finalize_output)
        
        # Add edges with conditional routing
        workflow.add_edge(START, "classify_query")
        workflow.add_conditional_edges(
            "classify_query",
            self.route_after_classification
        )
        workflow.add_edge("handle_ambiguity", "finalize_output")
        workflow.add_edge("extract_fields", "process_query")
        workflow.add_edge("process_query", "finalize_output")
        workflow.add_edge("finalize_output", END)
        
        return workflow.compile()

    def classify_query(self, state: ReActiveAgentState) -> ReActiveAgentState:
        """Classify the query type and extract key information"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            Analyze this CRM query and extract key information. Follow these rules:

            1. Identify the main action type:
               - get: Simple data retrieval
               - filter: Data with conditions
               - groupby: Group data by field
               - aggregate: Sum/Count/Average etc.
               - sort: Order data
               - top/bottom: Limit results
               - count: Count records

            2. Identify the entity type:
               - lead
               - case
               - account
               - opportunity

            3. Check for ambiguity:
               - Multiple possible entities
               - Unclear conditions
               - Missing required info

            4. Extract mentioned fields and conditions.

            Respond in JSON format:
            {
                "action": "get|filter|groupby|aggregate|sort|top|bottom|count",
                "entity_type": "lead|case|account|opportunity",
                "fields": ["field1", "field2"],
                "conditions": {"field": "value"},
                "ambiguous": true/false,
                "clarification": "question if ambiguous"
            }

            Query: {query}
            """)
        ])
        
        chain = prompt | self.llm | JsonOutputParser()
        result = chain.invoke({"query": state["query"]})
        
        state["action"] = result.get("action")
        state["entity_type"] = result.get("entity_type")
        state["fields"] = result.get("fields", [])
        state["conditions"] = result.get("conditions", {})
        state["clarification_needed"] = result.get("ambiguous", False)
        state["clarification_message"] = result.get("clarification")
        
        return state

    def route_after_classification(self, state: ReActiveAgentState) -> str:
        """Determine next step based on classification"""
        if state["clarification_needed"]:
            return "handle_ambiguity"
        return "extract_fields"

    def extract_fields(self, state: ReActiveAgentState) -> ReActiveAgentState:
        """Extract and validate fields from context"""
        available_fields = set()
        relevant_items = []
        
        # Find items matching the entity type
        for item in self.context:
            if item.get("entity_type") == state["entity_type"]:
                relevant_items.append(item)
                available_fields.update(item.get("data_fields", []))
        
        # If no fields specified, use all available fields
        if not state["fields"]:
            state["fields"] = list(available_fields)
        else:
            # Validate and filter fields
            state["fields"] = [f for f in state["fields"] if f in available_fields]
        
        # Update context to only relevant items
        state["context"] = relevant_items
        
        return state

    def handle_ambiguity(self, state: ReActiveAgentState) -> ReActiveAgentState:
        """Handle ambiguous queries that need clarification"""
        output = CRMQueryResult(
            entity_type=state.get("entity_type"),
            action=state.get("action"),
            fields=[],
            conditions=None,
            result=None,
            welcome_message="I need some clarification:",
            end_message="Please provide more details so I can help you better.",
            clarification_needed=True,
            clarification_message=state["clarification_message"],
            error=None
        )
        state["output"] = output
        return state

    def process_query(self, state: ReActiveAgentState) -> ReActiveAgentState:
        """Process the query based on action type"""
        try:
            results = []
            action = state["action"]
            fields = state["fields"]
            conditions = state["conditions"]
            
            # Filter relevant items
            filtered_items = []
            for item in state["context"]:
                matches_conditions = all(
                    item.get(k) == v for k, v in conditions.items()
                )
                if matches_conditions:
                    result = {f: item.get(f) for f in fields if f in item}
                    if result:
                        filtered_items.append(result)
            
            # Apply action-specific processing
            if action == "get":
                results = filtered_items
            elif action == "filter":
                results = filtered_items
            elif action == "sort":
                if fields:
                    results = sorted(filtered_items, key=lambda x: x.get(fields[0], 0))
            elif action == "top":
                limit = conditions.get("limit", 10)
                results = sorted(filtered_items, key=lambda x: x.get(fields[0], 0), reverse=True)[:limit]
            elif action == "bottom":
                limit = conditions.get("limit", 10)
                results = sorted(filtered_items, key=lambda x: x.get(fields[0], 0))[:limit]
            elif action == "count":
                results = [{"count": len(filtered_items)}]
            elif action == "groupby":
                # Group items by the first field
                grouped = {}
                for item in filtered_items:
                    key = item.get(fields[0])
                    if key not in grouped:
                        grouped[key] = []
                    grouped[key].append(item)
                results = [{"group": k, "items": v} for k, v in grouped.items()]
            
            state["result"] = results
            
        except Exception as e:
            state["error"] = f"Error processing query: {str(e)}"
            state["result"] = []
            
        return state

    def finalize_output(self, state: ReActiveAgentState) -> ReActiveAgentState:
        """Create the final structured output"""
        entity_type = state.get("entity_type", "record")
        action = state.get("action", "get")
        
        # Create welcome message based on action and entity
        welcome_messages = {
            "get": f"Here are your {entity_type} details:",
            "filter": f"Here are the filtered {entity_type} results:",
            "sort": f"Here are your {entity_type}s sorted by {state['fields'][0] if state['fields'] else 'default'}:",
            "top": f"Here are the top {entity_type}s:",
            "bottom": f"Here are the bottom {entity_type}s:",
            "count": f"Here's the count of {entity_type}s:",
            "groupby": f"Here are your {entity_type}s grouped by {state['fields'][0] if state['fields'] else 'default'}:",
        }
        
        output = CRMQueryResult(
            entity_type=state["entity_type"],
            action=state["action"],
            fields=state["fields"],
            conditions=state["conditions"],
            result=state["result"],
            welcome_message=welcome_messages.get(action, f"Here are your {entity_type} results:"),
            end_message="Is there anything specific about these results you'd like to know? You can ask for specific fields, sorting, or filtering.",
            clarification_needed=state["clarification_needed"],
            clarification_message=state["clarification_message"],
            error=state.get("error")
        )
        
        state["output"] = output
        return state

    def invoke(self, query: str) -> CRMQueryResult:
        """Execute the reactive agent workflow"""
        try:
            initial_state = ReActiveAgentState(
                query=query,
                context=self.context,
                entity_type=None,
                action=None,
                fields=[],
                conditions={},
                result=None,
                clarification_needed=False,
                clarification_message=None,
                output=None,
                error=None
            )
            
            result = self.workflow.invoke(initial_state)
            return result["output"]
            
        except Exception as e:
            return CRMQueryResult(
                entity_type=None,
                action=None,
                fields=[],
                conditions=None,
                result=None,
                welcome_message="Sorry, I encountered an error.",
                end_message="Please try rephrasing your query.",
                clarification_needed=False,
                clarification_message=None,
                error=f"Workflow execution failed: {str(e)}"
            )

# Example usage
if __name__ == "__main__":
    # Example context
    context = [
        {
            "entity_type": "lead",
            "data_fields": ["id", "name", "status", "amount"],
            "id": "L001",
            "name": "Acme Corp",
            "status": "open",
            "amount": 50000
        },
        {
            "entity_type": "lead",
            "data_fields": ["id", "name", "status", "amount"],
            "id": "L002",
            "name": "TechStart",
            "status": "closed",
            "amount": 75000
        }
    ]
    
    agent = ReActiveAgent(context)
    
    # Test queries
    test_queries = [
        "show my leads",
        "get case 12345",
        "show top 10 leads by amount",
        "show me all leads and accounts",
        "show my open leads"
    ]
    
    for query in test_queries:
        print(f"\nTesting query: {query}")
        result = agent.invoke(query)
        print("Result:", result)