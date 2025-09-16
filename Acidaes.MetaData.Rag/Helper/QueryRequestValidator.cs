using System.Text.RegularExpressions;

namespace Acidaes.MetaData.Rag.Model
{
    public static class QueryRequestValidator
    {
        private static readonly HashSet<string> AllowedOperators = new()
        {
            "=", "!=", ">", "<", ">=", "<=", "LIKE", "IN", "BETWEEN"
        };

        private static readonly HashSet<string> AllowedAggregations = new()
        {
            "SUM", "AVG", "COUNT", "MAX", "MIN"
        };

        private static readonly HashSet<string> AllowedSortDirections = new()
        {
            "ASC", "DESC"
        };

        private static readonly HashSet<string> AllowedFormats = new()
        {
            "table", "chart", "table_with_text", "card", "summary", "text"
        };

        private static readonly HashSet<string> AllowedRoutes = new()
        {
            "AI", "Client"
        };

        public static List<string> Validate(QueryRequest request)
        {
            var errors = new List<string>();

            if (string.IsNullOrWhiteSpace(request.RequestId))
                errors.Add("RequestId is required.");

            if (string.IsNullOrWhiteSpace(request.RoleContext))
                errors.Add("RoleContext is required.");

            if (request.Entity == null)
                errors.Add("Entity is required.");
            else
                errors.AddRange(ValidateEntity(request.Entity));

            if (request.Aggregations != null)
            {
                foreach (var agg in request.Aggregations)
                {
                    if (string.IsNullOrWhiteSpace(agg.Field))
                        errors.Add("Aggregation field is required.");
                    if (!AllowedAggregations.Contains(agg.Function.ToUpperInvariant()))
                        errors.Add($"Invalid aggregation function: {agg.Function}");
                }
            }

            if (request.Sort != null)
            {
                foreach (var sort in request.Sort)
                {
                    if (string.IsNullOrWhiteSpace(sort.Field))
                        errors.Add("Sort field is required.");
                    if (!AllowedSortDirections.Contains(sort.Direction.ToUpperInvariant()))
                        errors.Add($"Invalid sort direction: {sort.Direction}");
                }
            }

            if (request.Pagination != null)
            {
                if (request.Pagination.Limit <= 0 || request.Pagination.Limit > 1000)
                    errors.Add("Pagination limit must be between 1 and 1000.");
                if (request.Pagination.Offset < 0)
                    errors.Add("Pagination offset cannot be negative.");
            }

            if (request.Output == null)
                errors.Add("Output is required.");
            else
            {
                if (!AllowedFormats.Contains(request.Output.Format.ToLowerInvariant()))
                    errors.Add($"Invalid output format: {request.Output.Format}");
                if (!AllowedRoutes.Contains(request.Output.Route))
                    errors.Add($"Invalid output route: {request.Output.Route}");
            }

            return errors;
        }

        private static List<string> ValidateEntity(EntityQuery entity)
        {
            var errors = new List<string>();

            if (string.IsNullOrWhiteSpace(entity.Name))
                errors.Add("Entity name is required.");

            if (entity.Filters != null)
                errors.AddRange(ValidateFilterGroup(entity.Filters));

            if (entity.RelatedEntities != null)
            {
                foreach (var related in entity.RelatedEntities)
                {
                    errors.AddRange(ValidateRelatedEntity(related));
                }
            }

            return errors;
        }

        private static List<string> ValidateRelatedEntity(RelatedEntity entity)
        {
            var errors = new List<string>();

            if (string.IsNullOrWhiteSpace(entity.Name))
                errors.Add("Entity name is required.");

            if (entity.Filters != null)
                errors.AddRange(ValidateFilterGroup(entity.Filters));

            if (entity.RelatedEntities != null)
            {
                foreach (var related in entity.RelatedEntities)
                {
                    errors.AddRange(ValidateRelatedEntity(related));
                }
            }

            return errors;
        }

        private static List<string> ValidateFilterGroup(FilterGroup group)
        {
            var errors = new List<string>();

            if (group.Conditions != null)
            {
                foreach (var cond in group.Conditions)
                {
                    if (string.IsNullOrWhiteSpace(cond.Field))
                        errors.Add("Filter field is required.");
                    if (!AllowedOperators.Contains(cond.Operator.ToUpperInvariant()))
                        errors.Add($"Invalid operator: {cond.Operator}");
                    if (cond.Value == null)
                        errors.Add($"Filter value is required for field: {cond.Field}");
                }
            }

            if (group.NestedGroups != null)
            {
                foreach (var nested in group.NestedGroups)
                {
                    errors.AddRange(ValidateFilterGroup(nested));
                }
            }

            return errors;
        }
    }
}
