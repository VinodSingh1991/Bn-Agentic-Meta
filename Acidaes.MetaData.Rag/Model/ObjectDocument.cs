namespace Acidaes.MetaData.Rag.Model
{
    public class ObjectDocumentMetaData: DefaultMetaData
    {
        public int? ObjectId { get; set; }
        public string? ObjectName { get; set; }
        public string? Description { get; set; }
        public List<string> Fields { get; set; } = [];
        public List<string> RolesWithAccess { get; set; } = [];
        public string? PrimaryField { get; set; }
        public string? SubjectField { get; set; }
        public string? TableName { get; set; }
    }

    public class ObjectDocument : RagDocumentBase
    { 
        public ObjectDocumentMetaData MetaData { get; set; } = new ObjectDocumentMetaData();
    }

    public class ObjectDocumentDto
    {
        public int? ObjectId { get; set; }
        public string? ObjectName { get; set; }
        public string? Description { get; set; }
        public string? PrimaryField { get; set; }
        public string? SubjectField { get; set; }
        public string? TableName { get; set; }

    }
}
