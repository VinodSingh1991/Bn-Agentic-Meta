using Acidaes.MetaData.Rag.DAL.IDAL;
using Acidaes.MetaData.Rag.Helper;
using Acidaes.MetaData.Rag.Model;

namespace Acidaes.MetaData.Rag.BLL
{
    public class LayoutRagDocumentBLL(ILayoutRagDocument layoutRagDocument)
    {
        private readonly ResponseData _response = new();
        private readonly ILayoutRagDocument _layoutRagDocument = layoutRagDocument;

        public List<LayoutRagDcoument> PrepareLayoutDocuemnt(IEnumerable<LayoutSectionDocumentDTO> layoutSectionDocumentDTOs)
        {
            if (layoutSectionDocumentDTOs == null || !layoutSectionDocumentDTOs.Any())
                return [];

            List<LayoutRagDcoument> layoutRagDcoument = [];

            foreach (var layoutItem in layoutSectionDocumentDTOs)
            {
                var layout = layoutItem.LayoutXml != null ? Utility.GetFieldMetaDataFromXML(layoutItem.LayoutXml) : new Layout();

                var fields = layout.Fields;
                var tabs = layout.Tabs;
                var sections = layout.Sections;

                LayoutRagDcoument _layout = new()
                {
                    
                    Id = $"ObjectName_{layoutItem.ObjectName}_LayoutId_{layoutItem.LayoutId}",
                    Content = $"Object {layoutItem.ObjectName} with layout name {layoutItem.LayoutName} is used to view the information. ",
                    MetaData = new()
                    {
                        LayoutId = layoutItem.LayoutId,
                        LayoutName = layoutItem.LayoutName,
                        ObjectName = layoutItem.ObjectName,
                        ObjectId = layoutItem.ObjectId,
                        RoleAccess = layoutItem.RoleName,
                        Fields = fields,
                        LayoutTabs = tabs,
                        Sections  = sections
                    }
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
                var parseFields = PrepareLayoutDocuemnt(layoutRagList);
                _response.IsSuccess = "True";
                _response.Message = "Success";
                _response.Data = parseFields;
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
