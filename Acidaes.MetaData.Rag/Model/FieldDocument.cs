
namespace Acidaes.MetaData.Rag.Model
{
    public class FieldDocumentDto
    {
        public int ObjectId { get; set; }
        public string? FieldId { get; set; }
        public string? FieldName { get; set; }
        public string? FieldLabel { get; set; }
        public string? DisplayLabel { get; set; }
        public FieldType FieldType { get; set; }
        public string? TableName { get; set; }
        public string? Description { get; set; }
        public bool? IsMandatory { get; set; }

    }
    public class FieldMetaData: DefaultMetaData
    {
        public int ObjectId { get; set; }
        public string? FieldId { get; set; }

        public string? ModifiedFieldId { get; set; }
        public string? FieldName { get; set; }
        public string? FieldType { get; set; }
        public string? Description { get; set; }

        public string? FieldLabel { get; set; }
        public string? DisplayLabel { get; set; }
        public string? TableName { get; set; }

        public string? ObjectName { get; set; }
        public string? DataType { get; set; }
        public bool IsFilterable { get; set; }
        public bool IsVisible { get; set; }
        public string? LookUpType { get; set; }
        public List<string> RoleAccess { get; set; } = [];
        public List<string> ValidationRules { get; set; } = [];
        public string? DefaultValue { get; set; }
        public string? RenderingType { get; set; }
        public bool? IsMandatory { get; set; }
    }

    public class FieldDocument : RagDocumentBase
    {
        public FieldMetaData MetaData { get; set; } = new FieldMetaData();
    }

    public enum FieldType
    {
        None = -1,
        Lookup = 0,
        Number = 1,
        Text = 2,
        Amount = 3,
        DateTime = 4,
        Email = 5,
        Url = 6,
        Phone = 7,
        Date = 8,
        Comments = 9,
        Check = 10,
        MulticurrencyAmount = 11,
        Time = 12,
        UserPicker = 13,
        MultiPicker = 14,
        ComputedField = 15,
        SequenceNumber = 16,
        Decimal = 17,
        Percentage = 18,
        Document = 19,
        Duration = 20,
        CurrencyPicker = 21,
        ObjectNumber = 22,
        BigInt = 23,
        MultiLevel = 24,
        ExternalField = 25,
        LookupWithId = 26,
        TemplatePicker = 27,
        HTML = 28,
        Aggregation = 29,
        Image = 30,
        LongText = 31,
        //Image = 29,
        //File = 30,
        ReferenceLookup = 32,//used only for Creating ReferenceLookup & Note that FieldType of Lookup will be used ,
        SmartImage = 33,
        Rating = 34,
        ProgressBar = 35,
        WebIntegerationUrl = 36
    }

    public enum FieldOperation
    {
        None = -1,
        Equal = 0,
        Greater = 1,
        Lesser = 2,
        NotEqual = 3,
        GreaterEqual = 4,
        LesserEqual = 5,
        Like = 6,
        AnyOf = 7,
        In = 8,
        NotIn = 9,
        LikeAnd = 10,
        SameAsItemValue = 11,
        NotSameAsItemValue = 12,
        IsSpecified = 13,
        IsNotSpecified = 14,
        LikeAsItemValue = 15,
        Expression = 16
    }

}
