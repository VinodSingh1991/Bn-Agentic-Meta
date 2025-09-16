using Acidaes.MetaData.Rag.DAL.IDAL;
using Acidaes.MetaData.Rag.Helper;
using Acidaes.MetaData.Rag.Model;
using Microsoft.AspNetCore.DataProtection.KeyManagement;
using Swashbuckle.AspNetCore.SwaggerGen;
using System.Text;
using static System.Collections.Specialized.BitVector32;

namespace Acidaes.MetaData.Rag.BLL
{
    public class LayoutRagDocumentBLL(ILayoutRagDocument layoutRagDocument)
    {
        private readonly ResponseData _response = new();
        private readonly ILayoutRagDocument _layoutRagDocument = layoutRagDocument;

        public string GetSectionModel(List<LayoutSections> sections)
        {
            if (sections == null || sections.Count == 0)
                return string.Empty;

            var sectionStrings = sections.Select(s =>
                $"SectionName: {s.SectionName ?? ""}, " +
                $"TabName: {s.TabName ?? ""}, " +
                $"TabId: {s.TabId ?? ""}, " +
                $"SectionFields: [{string.Join(", ", s.SectionFields ?? new List<string>())}]"
            );

            return string.Join(" | ", sectionStrings);
        }

        public string GetTabs(List<LayoutSections> sections)
        {
            if (sections == null || sections.Count == 0)
                return string.Empty;

            var sectionStrings = sections.Select(s =>
                $"SectionName: {s.SectionName ?? ""}, " +
                $"TabName: {s.TabName ?? ""}, " +
                $"TabId: {s.TabId ?? ""}, " +
                $"SectionFields: [{string.Join(", ", s.SectionFields ?? new List<string>())}]"
            );

            return string.Join(" | ", sectionStrings);
        }

        public string PrepareContent(Layout layout, LayoutSectionDocumentDTO layoutItem)
        {
            var fields = layout.Fields;
            var sections = layout.Sections;

            var roleText = !string.IsNullOrWhiteSpace(layoutItem.RoleName)
                ? layoutItem.RoleName
                : "Administrator";

            var sb = new StringBuilder();

            // 1. Description
            sb.AppendLine($"Layout '{layoutItem.LayoutName}' (Id: {layoutItem.LayoutId}) belongs to object '{layoutItem.ObjectName}' (ObjectId: {layoutItem.ObjectId}).");
            sb.AppendLine($"Accessible by role(s): {roleText}.");
            sb.AppendLine($"This layout contains {fields.Count} fields, and {sections.Count} sections.");

            if (sections.Any())
                sb.AppendLine($"Sections: {string.Join(", ", GetSectionModel(sections))}.");

            if (fields.Any())
                sb.AppendLine($"Fields: {string.Join(", ", fields)}.");

            // 2. Synonyms
            sb.AppendLine();
            sb.AppendLine("Synonyms:");
            sb.AppendLine($"{layoutItem.LayoutName}, {layoutItem.ObjectName} layout, cust_layout_{layoutItem.LayoutId}, {string.Join(", ", fields)}, {string.Join(", ", sections)}");

            // 3. Tags
            sb.AppendLine();
            sb.AppendLine("Tags:");
            sb.AppendLine($"layout, {layoutItem.ObjectName} layout, UI structure, field placement, tab grouping, section organization, role-based view, layout {layoutItem.LayoutName}, object {layoutItem.ObjectName}, fields {string.Join(", ", fields)}");


            return sb.ToString();
        }


        public List<LayoutSectionDocumentMetaData> PrepareLayoutDocuemnt(IEnumerable<LayoutSectionDocumentDTO> layoutSectionDocumentDTOs)
        {
            if (layoutSectionDocumentDTOs == null || !layoutSectionDocumentDTOs.Any())
                return [];

            List<LayoutSectionDocumentMetaData> layoutRagDcoument = [];
            Dictionary<string, List<string>> roleAccessDict = new();
            HashSet<string> addedLayoutKeys = new();
            

            foreach (var layoutItem in layoutSectionDocumentDTOs)
            {
                var layoutKey = layoutItem.LayoutId.ToString() ?? string.Empty;
                //var roleName = layoutItem.RoleName ?? "Administrator";
                var roleId = layoutItem.RoleId?.ToString() ?? "0";

                // Track roles for each layout key
                if (!roleAccessDict.TryGetValue(layoutKey, out var roleList))
                {
                    roleList = new List<string>();
                    roleAccessDict[layoutKey] = roleList;
                }
                if (!roleList.Contains(roleId))
                {
                    roleList.Add(roleId);
                }

                // Only add unique layouts by layoutKey
                if (addedLayoutKeys.Contains(layoutKey))
                {
                    continue;
                }
                   
                addedLayoutKeys.Add(layoutKey);

                var layout = layoutItem.LayoutXml != null ? Utility.GetFieldMetaDataFromXML(layoutItem.LayoutXml) : new Layout();
                var fieldProps = layoutItem.LayoutXml != null ? Utility.GetLayoutFieldsProps(layoutItem.LayoutXml, layoutItem.RoleId, layoutKey) : [];

                var fields = layout.Fields;
                //var tabs = layout.Tabs;
                //var sections = layout.Sections;

                var content = PrepareContent(layout, layoutItem);

                LayoutSectionDocumentMetaData _layout = new()
                {
                    LayoutId = layoutItem.LayoutId,
                    LayoutName = layoutItem.LayoutName,
                    ObjectName = layoutItem.ObjectName,
                    ObjectId = layoutItem.ObjectId,
                    OrignalRoleAccess = layoutItem.RoleName,
                    OrignalRoleId = layoutItem.RoleId.ToString(),
                    RoleAccess = roleList,
                    Fields = fields,
                    ModifiedLayoutFieldProps = fieldProps,
                };

                layoutRagDcoument.Add(_layout);
            }

            return layoutRagDcoument;
        }
        public async Task<ResponseData> GetLayoutRagList()
        {
            try
            {
                var layoutRagList = await _layoutRagDocument.GetLayoutSectionDocumentsList();
                var layouts = PrepareLayoutDocuemnt(layoutRagList);
                _response.IsSuccess = "True";
                _response.Message = "Success";
                _response.Data = layouts;
                return _response;
            }
            catch (Exception ex)
            {
                _response.IsSuccess = "False";
                _response.Message = ex.Message;
                _response.Data = new object();
                return _response;
            }
        }
    }
}
