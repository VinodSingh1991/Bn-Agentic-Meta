namespace Acidaes.MetaData.Rag.Model
{
    public class RoleDocumentMetaData 
    {
        public string? RoleName { get; set; }
        public string? RoleDescription { get; set; }
        public string? RoleId { get; set; }
    }

    public class ObjectPermission
    {
        public string? ObjectName { get; set; }
        public List<string> ObjectOperationName { get; set; } = [];
    }

    public enum ObjectPermissionType { 
        Create, Update, Read
    }

    public class RoleDocument: RagDocumentBase
    { 
        public RoleDocumentMetaData MetaData { get; set; } = new RoleDocumentMetaData();
    }

    public class RoleDocumentDTO
    {
        public string? RoleId { get; set; }
        public string? RoleName { get; set; }
        public string? RoleDescription { get; set; }
    }

}
