from rag.patterns.output_json.get_output import create_intent_and_output_format

get_base_patterns = {
    # --- Basic & Self ---
    "Show my {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),
    "List all {ObjectPlural}": create_intent_and_output_format("GET", "LIST"),
    "Get all {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),
    "Fetch my {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} assigned to me": create_intent_and_output_format("GET", "TABLE"),
    "Send my {ObjectPlural} assigned to me": create_intent_and_output_format("GET", "TABLE"),
    "Send me {ObjectPlural} assigned to me": create_intent_and_output_format("GET", "TABLE"),

    # --- Date Based ---
    "Show {ObjectPlural} created today": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} created yesterday": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} created this week": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} created last week": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} created this month": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} created last month": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} created this year": create_intent_and_output_format("GET", "TABLE"),

    # --- Status / Priority ---
    "List {ObjectPlural} by status": create_intent_and_output_format("GET", "TABLE"),
    "Show my open {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),
    "Show my closed {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),
    "Show my active {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),
    "Show my overdue {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),
    "Show my pending {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),
    "Show my completed {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),
    "Show my high priority {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),
    "Show my low priority {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),

    # --- Limit / Top N ---
    "Show top {N} {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),
    "Show latest {N} {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),
    "Show recent {N} {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),
    "Show last {N} {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),
    "Show first {N} {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),
    "Show next {N} {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),
    "Show {N} random {ObjectPlural}": create_intent_and_output_format("GET", "TABLE"),

    # --- Filtering / Sorting ---
    "Show {ObjectPlural} sorted by {Field}": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} filtered by {Field} = {Value}": create_intent_and_output_format("GET", "TABLE"),
    "Find {ObjectPlural} by {Field}": create_intent_and_output_format("GET", "TABLE"),
    "Search {ObjectPlural} where {Field} = {Value}": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} where {Field} contains {Keyword}": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} where {Field} starts with {Keyword}": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} where {Field} ends with {Keyword}": create_intent_and_output_format("GET", "TABLE"),

    # --- Ownership ---
    "Show {ObjectPlural} owned by me": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} assigned to {UserName}": create_intent_and_output_format("GET", "TABLE"),
    "Find {ObjectPlural} created by {UserName}": create_intent_and_output_format("GET", "TABLE"),
    "Find {ObjectPlural} updated by {UserName}": create_intent_and_output_format("GET", "TABLE"),

    # --- Date Range ---
    "Show {ObjectPlural} created between {Date1} and {Date2}": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} updated after {Date}": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} updated before {Date}": create_intent_and_output_format("GET", "TABLE"),

    # --- Grouping ---
    "Show {ObjectPlural} grouped by {Field}": create_intent_and_output_format("GET", "TABLE"),
    "List {ObjectPlural} by {Field}": create_intent_and_output_format("GET", "TABLE"),

    # --- Related Object (newly added) ---
    "Show {ObjectPlural} related to {RelatedObject}": create_intent_and_output_format("GET", "TABLE"),
    "List {ObjectPlural} linked to {RelatedObject}": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} connected to {RelatedObject}": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} under {RelatedObject}": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} associated with {RelatedObject}": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} which are related to {RelatedObject}": create_intent_and_output_format("GET", "TABLE"),

    # --- One Object (Details) ---
    "Show one {Object}": create_intent_and_output_format("GET", "DETAILS"),
    "Get details of {Object}": create_intent_and_output_format("GET", "DETAILS"),
    "Fetch details of {Object}": create_intent_and_output_format("GET", "DETAILS"),
    "Show details of {Object}": create_intent_and_output_format("GET", "DETAILS"),
    "Show summary of {Object}": create_intent_and_output_format("GET", "DETAILS"),
    "Show overview of {Object}": create_intent_and_output_format("GET", "DETAILS"),
    "Show info of {Object}": create_intent_and_output_format("GET", "DETAILS"),
    "Show information of {Object}": create_intent_and_output_format("GET", "DETAILS"),
    "Get info of {Object}": create_intent_and_output_format("GET", "DETAILS"),
    "Get information of {Object}": create_intent_and_output_format("GET", "DETAILS"),
    "Fetch info of {Object}": create_intent_and_output_format("GET", "DETAILS"),
    "Fetch information of {Object}": create_intent_and_output_format("GET", "DETAILS"),
    "Show {Object} details": create_intent_and_output_format("GET", "DETAILS"),
    "Show {Object} info": create_intent_and_output_format("GET", "DETAILS"),
    "Show {Object} information": create_intent_and_output_format("GET", "DETAILS"),
    "Get {Object} details": create_intent_and_output_format("GET", "DETAILS"),
    "Get {Object} info": create_intent_and_output_format("GET", "DETAILS"),
    "Get {Object} information": create_intent_and_output_format("GET", "DETAILS"),
    "Fetch {Object} details": create_intent_and_output_format("GET", "DETAILS"),
    "Fetch {Object} info": create_intent_and_output_format("GET", "DETAILS"),
    "Fetch {Object} information": create_intent_and_output_format("GET", "DETAILS"),
    "Find {Object} by ID {Value}": create_intent_and_output_format("GET", "DETAILS"),
    "Get {Object} with ID {Value}": create_intent_and_output_format("GET", "DETAILS"),
    "Show {Object} number {Value}": create_intent_and_output_format("GET", "DETAILS"),
    "Get {Object} reference {Value}": create_intent_and_output_format("GET", "DETAILS"),
    "Fetch {Object} with reference {Value}": create_intent_and_output_format("GET", "DETAILS"),

    # By Name / Keyword
    "Find {Object} named {Keyword}": create_intent_and_output_format("GET", "DETAILS"),
    "Show {Object} with name {Keyword}": create_intent_and_output_format("GET", "DETAILS"),
    "Get {Object} called {Keyword}": create_intent_and_output_format("GET", "DETAILS"),
    "Search {ObjectPlural} by name {Keyword}": create_intent_and_output_format("GET", "DETAILS"),

    # By Contact Info
    "Find {Object} by phone {Value}": create_intent_and_output_format("GET", "DETAILS"),
    "Find {Object} by email {Value}": create_intent_and_output_format("GET", "DETAILS"),
    "Show {ObjectPlural} where email = {Value}": create_intent_and_output_format("GET", "TABLE"),

    # By Ownership
    "Show {ObjectPlural} owned by {UserName}": create_intent_and_output_format("GET", "TABLE"),
    "Get {ObjectPlural} managed by {UserName}": create_intent_and_output_format("GET", "TABLE"),
    "Show {ObjectPlural} handled by {TeamName}": create_intent_and_output_format("GET", "TABLE"),

    # Generic CRM Phrasing
    "Pull up {Object}": create_intent_and_output_format("GET", "DETAILS"),
    "Bring me details of {Object}": create_intent_and_output_format("GET", "DETAILS"),
    "Give me {Object} information": create_intent_and_output_format("GET", "DETAILS"),
    "Open {Object}": create_intent_and_output_format("GET", "DETAILS"),
    "Display {Object} details": create_intent_and_output_format("GET", "DETAILS"),
}
