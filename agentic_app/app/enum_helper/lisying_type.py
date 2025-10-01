listing_type = {
    "None": 0,
    "OpenActivities": 3,
    "ClosedActivities": 4,
    "RelatedNotes": 5,
    "RelatedHistory": 6,
    "RelatedIssues": 7,
    "RelatedRequirements": 8,
    "RelatedProducts": 9,
    "RelatedLeads": 14,
    "OpenOpportunities": 19,
    "ClosedOpportunities": 20,
    "RelatedContact": 28,
    "RealtedContract": 29,
    "RelatedAssets": 30,
    "OpenCases": 31,
    "ClosedCases": 32,
    "RelatedAttachments": 33,
    "RelatedPartners": 34,
    "RelatedCompetitors": 35,
    "RelatedSolutions": 36,
    "RelatedResponses": 37,
    "RelatedOffer": 38,
    "RelatedCases": 40,
}


def get_listing_type(name: str) -> int:
    return listing_type.get(name, -1)
