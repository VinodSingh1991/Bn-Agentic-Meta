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

        public List<string> GetRoles(FieldDocumentDto field, IEnumerable<LayoutRagDcoument> objectLayouts)
        {
            List<string> roles = ["Administrator"];

            if (objectLayouts != null && objectLayouts.Any() && field?.FieldId != null)
            {
                foreach (var layout in objectLayouts)
                {
                    var fields = layout.MetaData?.Fields;
                    var role = layout.MetaData?.RoleAccess;
                    var fld = $"cust_{field.FieldId}";

                    if (fields != null && fields.Contains(fld) && role != null && !roles.Contains(role))
                    {
                        // Add all roles, avoiding duplicates

                        roles.Add(role);
                    }
                }
            }

            return roles;
        }


        public IEnumerable<LayoutRagDcoument> GetLayoutByObjectId(int? objectId, IEnumerable<LayoutRagDcoument> allLayout)
        {
            if (allLayout == null || !allLayout.Any())
                return [];

            return [.. allLayout.Where(l => l.MetaData?.ObjectId != null && l.MetaData.ObjectId == objectId)];
        }

        private string BuildFieldContent(FieldDocumentDto fieldDto, List<string> roles, string fieldType)
        {
            var roleText = roles != null && roles.Count != 0 ? string.Join(", ", roles) : "Administrator";
            var mandatoryText = fieldDto.IsMandatory == true ? "Mandatory" : "Optional";
            var objectName = Utility.GetObjectNameById(fieldDto.ObjectId);

            return $"Field 'cust_{fieldDto.FieldId}' (ID: {fieldDto.FieldId}) and (Field Name {fieldDto.FieldName}) with Display Label {fieldDto.DisplayLabel} belongs to object '{objectName}' (ObjectId: {fieldDto.ObjectId}). " +
        $"It is of field type {fieldType}, {mandatoryText.ToLower()}, and accessible to {roleText}.";
        }
        public List<FieldDocument> PrepareFieldDocument(IEnumerable<FieldDocumentDto> fieldDocumentDtosList, IEnumerable<LayoutRagDcoument> layoutRagDcouments)
        {
            if (fieldDocumentDtosList == null || !fieldDocumentDtosList.Any())
                return [];

            List<FieldDocument> fieldDocuments = [];

            foreach (var fieldDto in fieldDocumentDtosList)
            {
                var objectLayouts = GetLayoutByObjectId(fieldDto.ObjectId, layoutRagDcouments);
                var roles = GetRoles(fieldDto, objectLayouts);
                var fieldType = Utility.GetFieldTypeName(fieldDto.FieldType);
                var content = BuildFieldContent(fieldDto, roles, fieldType);
                var objectName = Utility.GetObjectNameById(fieldDto.ObjectId);

                FieldDocument fieldDocument = new()
                {
                    Id = $"OBjectId_{fieldDto.ObjectId}_FieldId_{fieldDto.FieldId}",
                    Content = content,
                    MetaData = new FieldMetaData
                    {
                        FieldId = fieldDto.FieldId,
                        ModifiedFieldId = $"cust_{fieldDto.FieldId}",
                        FieldName = fieldDto.FieldName,
                        FieldType = fieldType,
                        ObjectName = objectName,
                        Description = fieldDto.Description,
                        DisplayLabel = fieldDto.DisplayLabel,
                        IsMandatory = fieldDto.IsMandatory ?? false,
                        FieldLabel = fieldDto.FieldLabel,
                        ObjectId = fieldDto.ObjectId,
                        TableName = $"{objectName} has a DataBase Table {fieldDto.TableName}",
                        RoleAccess = roles,
                        DataType = fieldType,
                        RenderingType = "Field"
                    }

                };
                fieldDocuments.Add(fieldDocument);
            }

            return fieldDocuments;
        }

        public async Task<ResponseData> GetFieldDocuments()
        {

            try
            {
                var layoutFields = await _layoutRagDocument.GetLayoutRagList();
                var fieldDocFromDb = await _fieldRagDocument.GetFieldDocument();

                IEnumerable<LayoutRagDcoument>? layoutList = layoutFields.Data as IEnumerable<LayoutRagDcoument>;

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
