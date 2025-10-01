object_list = {
    1: "Task",
    2: "Event",  # Event is used as Appointment
    3: "Survey",
    4: "Note",
    5: "Contact",
    6: "Lead",
    7: "Account",
    8: "Opportunity",
    9: "Case",
    19: "Issue",  # Used by Mailing List
    34: "Product",
    43: "Activity",  # Common for Tasks and Events Views
    56: "Contract",
}

def get_object_name(item_type: int) -> str:
    return object_list.get(item_type, "Unknown")