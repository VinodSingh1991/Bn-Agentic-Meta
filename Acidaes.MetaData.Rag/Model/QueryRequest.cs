namespace Acidaes.MetaData.Rag.Model
{

    public enum QueryOperation
    {
        READ, CREATE, UPDATE, DELETE, AGGREGATE, ACTION, BULK
    }

    public class EntityQuery
    {
        public required string Name { get; set; }
        public required string Alias { get; set; }
        public required List<RelatedEntity> RelatedEntities { get; set; }
        public required List<string> OutPutFields { get; set; }
        public required FilterGroup Filters { get; set; }
    }

    public class RelatedEntity
    {
        public required string Name { get; set; }
        public required string Alias { get; set; }
        public required string Relationship { get; set; } // JOIN condition
        public required List<string> OutputFields { get; set; }
        public required FilterGroup Filters { get; set; }

        public required List<RelatedEntity> RelatedEntities { get; set; }
    }

    public class FilterGroup
    {
        public required string Logical { get; set; } // AND | OR
        public required List<FilterCondition> Conditions { get; set; }
        public required List<FilterGroup> NestedGroups { get; set; }
    }

    public class FilterCondition
    {
        public required string Field { get; set; }
        public required string Operator { get; set; } // =, !=, >, <, LIKE, IN, BETWEEN
        public required object Value { get; set; }
    }

    public class Aggregation
    {
        public required string Field { get; set; }
        public required string Function { get; set; } // SUM, AVG, COUNT, MAX, MIN
        public required string Alias { get; set; }
    }

    public class SortClause
    {
        public required string Field { get; set; }
        public required string Direction { get; set; } // ASC | DESC
    }

    public class Pagination
    {
        public int Limit { get; set; }
        public int Offset { get; set; }
    }

    public class OutputOptions
    {
        public required string Format { get; set; } // table, chart, kpi, summary, raw
        public required string Route { get; set; } // AI | Client
        public required bool Explain { get; set; }
    }
    public class QueryRequest
    {
        public required string RequestId { get; set; }
        public required string RoleContext { get; set; }
        public required QueryOperation Operation { get; set; }
        public required EntityQuery Entity { get; set; }
        public required List<string> GroupBy { get; set; }
        public required List<Aggregation> Aggregations { get; set; }
        public required List<SortClause> Sort { get; set; }
        public required Pagination Pagination { get; set; }
        public required OutputOptions Output { get; set; }
    }
}
