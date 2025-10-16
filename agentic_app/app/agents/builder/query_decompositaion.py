from agents.controllers.structured_output import AgentSchema
from langchain_core.prompts import ChatPromptTemplate
from agents.llm_factory import LLMFactory
from langchain_core.output_parsers import StrOutputParser


class QueryDecomposition:

    @classmethod
    def get_query_decompose_prompt(cls) -> ChatPromptTemplate:
        query_normalizer_prompt ="""
            You are a CRM query decomposer.

            ### Goal
            Take a normalized CRM query and break it into multiple smaller queries
            that can be used for retrieval or RAG context building.
            
            ### Context
            objectsName: Leads, Accounts, Contacts, Opportunities, Cases, Activities, Products, Quotes, Invoices, Solutions, Campaigns, Users, Teams
            objectPrimaryKeys: LeadId, AccountId, ContactId, OpportunityId, CaseId, ActivityId, ProductId, QuoteId, InvoiceId, SolutionId, CampaignId, UserId, TeamId
            objectForeignKeys: LeadIdActivityId, AccountIdContactId, AccountIdOpportunityId, AccountIdCaseId, ContactIdActivityId, OpportunityIdProductId, QuoteIdProductId, InvoiceIdProductId, CampaignIdLeadId
            ###

            Rules:
            1. Each query should be self-contained and clear.
            2. If there are multiple entities joined by 'and' or relational words, split them.
            3. If there is a relationship (like "leads and their activities"), express it as:
            - "show my activities where ActivityId == LeadIdActivityId"
            4. Return only a **Python-style list of strings**.
            5. Do NOT explain, just return the list.

            ### Examples

            Input: show my leads and cases
            Output:
            [
            "show my leads",
            "show my cases"
            ]

            Input: show my all leads and their activities
            Output:
            [
            "show my all leads",
            "show my activities where ActivityId == LeadIdActivityId"
            ]

            Input: show my 10 top leads and 5 accounts
            Output:
            [
            "show my top 10 leads",
            "show my top 5 accounts"
            ]
            
            Input: "show my accounts group by rating"
            Output:
            [
            "show my accounts group by rating"
            ]
            
            Input: "show my account which is related to leadid = 124545"
            Output:
            [
            "show my account where LeadIdAccountId == 124545"
            ]
            
            Input: "show my Cases and its related contacts"
            Output:
            [
            "show my Cases where CaseId == CasesIdContactId",
            "show my Contacts where ContactId == CasesIdContactId"
            ]
            
            Input: "show my open leads and their related activities"
            Output:
            [
            "show my open leads",
            "show my activities where ActivityId == LeadIdActivityId"
            ]

            Now, decompose this normalized query:
            "{normalized_query}"
            """
        return ChatPromptTemplate.from_messages([("system", query_normalizer_prompt)])

    @classmethod
    def invoke(cls, user_query: str) -> str:
        
        print("The original user query for decomposition is:", user_query)
        prompt = cls.get_query_decompose_prompt()
        chain = prompt |  LLMFactory.open_ai() | StrOutputParser()
        response = chain.invoke({"normalized_query": user_query})
        print("The decomposed query response is:", response)
        try:
            # Safely evaluate list-like string output
            result = eval(response.strip())
            if isinstance(result, list):
                return result
            return [response.strip()]
        except Exception:
            return [response.strip()]
