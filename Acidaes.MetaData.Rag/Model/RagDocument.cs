namespace Acidaes.MetaData.Rag.Model
{
    public class RagDocumentBase
    {
        public string? Id { get; set; }
        public string? Content { get; set; }
    }
    public class RagDocument
    {
       public Dictionary<string, object> MetaData { get; set; } = [];
    }

    public class DefaultMetaData
    {
        public string? Source { get; set; }
        public string? Url { get; set; }
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
        public string? Version { get; set; } = "Version 1.0";
        public string? Author { get; set; } = "Vinod Singh";
        public string? Language { get; set; } = "English US";
        public string? Summary { get; set; }
        public List<string> Tags { get; set; } = [];
        public RagDocumentType RagDocumentType { get; set; }
    }

    public enum RagDocumentType
    {
        Object,
        Field,
        Role,
        Layout,
        Other
    }
}
