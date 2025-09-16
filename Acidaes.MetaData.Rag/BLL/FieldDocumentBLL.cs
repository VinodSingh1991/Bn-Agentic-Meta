using Acidaes.MetaData.Rag.DAL.IDAL;
using Acidaes.MetaData.Rag.Helper;
using Acidaes.MetaData.Rag.Model;
using Microsoft.VisualBasic.FileIO;
using System.Data;
using System.Linq;

namespace Acidaes.MetaData.Rag.BLL
{
    public class FieldDocumentBLL(IFieldRagDocument fieldRagDocument, ILayoutRagDocument layoutRagDocument)
    {
        private readonly ResponseData _response = new();
        private readonly IFieldRagDocument _fieldRagDocument = fieldRagDocument;
        private readonly LayoutRagDocumentBLL _layoutRagDocument = new(layoutRagDocument);

        public List<string> GetRoles(FieldDocumentDto field, IEnumerable<LayoutSectionDocumentMetaData> objectLayouts)
        {
            List<string> roles = ["0"];

            if (objectLayouts != null && objectLayouts.Any() && field?.FieldId != null)
            {
                foreach (var layout in objectLayouts)
                {
                    var fields = layout?.Fields;
                    var roleId = layout?.OrignalRoleId;
                    //var fld = $"cust_{field.FieldId}";

                    var fld = field.LayoutFieldId;

                    if (fields != null && fields.Contains(fld) && fields != null && !roles.Contains(roleId))
                    {
                        // Add all roles, avoiding duplicates

                        roles.Add(roleId);
                    }
                }
            }

            return roles;
        }


        public IEnumerable<LayoutSectionDocumentMetaData> GetLayoutByObjectId(int? objectId, IEnumerable<LayoutSectionDocumentMetaData> allLayout)
        {
            if (allLayout == null || !allLayout.Any())
                return [];

            return [.. allLayout.Where(l => l.ObjectId == objectId)];
        }

        public List<string> GetSynonyms(FieldDocumentDto field, IEnumerable<LayoutSectionDocumentMetaData> objectLayouts)
        {
            List<string> syn = new List<string>();

            if (objectLayouts != null && objectLayouts.Any() && field?.LayoutFieldId != null)
            {
                foreach (var layout in objectLayouts)
                {
                    var layoutProps = layout?.ModifiedLayoutFieldProps;

                    var fldId = field.LayoutFieldId;

                    var layoutItem = layoutProps?.FirstOrDefault(item => item.FieldId == fldId);

                    if (layoutItem != null && layoutItem.LayoutModifiedName != null && !syn.Contains(layoutItem.LayoutModifiedName))
                    {
                        // Add all roles, avoiding duplicates

                        syn.Add(layoutItem.LayoutModifiedName);
                    }
                }
            }

            return syn;
        }

        public List<FieldMetaData> PrepareFieldDocument(IEnumerable<FieldDocumentDto> fieldDocumentDtosList, IEnumerable<LayoutSectionDocumentMetaData> layoutRagDcouments)
        {
            if (fieldDocumentDtosList == null || !fieldDocumentDtosList.Any())
                return [];

            List<FieldMetaData> fieldDocuments = [];

            foreach (var fieldDto in fieldDocumentDtosList)
            {
                var objectLayouts = GetLayoutByObjectId(fieldDto.ObjectId, layoutRagDcouments);
                var roles = GetRoles(fieldDto, objectLayouts);
                var objectName = Utility.GetObjectNameById(fieldDto.ObjectId);
                var syn = GetSynonyms(fieldDto, objectLayouts);

                FieldMetaData fieldDocument = new()
                {
                    FieldId = fieldDto.FieldId,
                    ModifiedFieldId = fieldDto.LayoutFieldId,
                    FieldName = fieldDto.FieldName, //field name
                    ObjectName = objectName,
                    FieldLabel = fieldDto.FieldLabel, //label
                    ObjectId = fieldDto.ObjectId,
                    RoleAccess = roles,
                    LayoutFieldId = fieldDto.LayoutFieldId,
                    Synonyms = syn

                };
                fieldDocuments.Add(fieldDocument);
            }

            return fieldDocuments;
        }

        public async Task<ResponseData> GetFieldDocuments(bool isSystemField)
        {

            try
            {
                var layoutFields = await _layoutRagDocument.GetLayoutRagList();
                var fieldDocFromDb = await _fieldRagDocument.GetFieldDocument(isSystemField);

                IEnumerable<LayoutSectionDocumentMetaData>? layoutList = layoutFields.Data as IEnumerable<LayoutSectionDocumentMetaData>;

                var fieldDocuments = PrepareFieldDocument(fieldDocFromDb, layoutList);
                _response.Data = fieldDocuments;
                _response.IsSuccess = "True";
                return _response;
            }
            catch (Exception ex)
            {
                _response.IsSuccess = "False";
                _response.Message = ex.Message;
                return _response;
            }
        }
    }
}
