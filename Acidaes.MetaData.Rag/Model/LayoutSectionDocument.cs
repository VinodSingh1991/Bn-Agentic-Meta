using System.Xml;

namespace Acidaes.MetaData.Rag.Model
{
    public class LayoutTab
    {
        public string? TabId { get; set; }
        public string? TabName { get; set; }
    }

    public class LayoutSections
    {
        public string? SectionName { get; set; }
        public string? TabName { get; set; }
        public string? TabId { get; set; }
        public List<string> SectionFields { get; set; } = [];
    }
    public class LayoutSectionDocumentMetaData : DefaultMetaData
    {
        public List<LayoutTab> LayoutTabs { get; set; } = [];
        public List<LayoutSections> Sections { get; set; } = [];
        public List<string>? Fields { get; set; }
        public int? ObjectId { get; set; }
        public string? ObjectName { get; set; }
        public string? RoleAccess { get; set; }
        public int? LayoutId { get; set; }
        public string? LayoutName { get; set; }

    }

    public class LayoutRagDcoument : RagDocumentBase
    {
        public LayoutSectionDocumentMetaData MetaData { get; set; } = new LayoutSectionDocumentMetaData();
    }

    public class LayoutSectionDocumentDTO
    {
        public int? LayoutId { get; set; }
        public string? LayoutName { get; set; }
        public string? LayoutXml { get; set; }
        public string? LayoutType { get; set; } = "2";
        public int? ObjectId { get; set; }
        public string? ObjectName { get; set; }
        public int? RoleId { get; set; }
        public string? RoleName { get; set; }
    }

    public class Layout
    {
        public List<string> Fields { get; set; }
        public List<LayoutSections> Sections { get; set; }
        public List<LayoutTab> Tabs { get; set; }
    }
}
