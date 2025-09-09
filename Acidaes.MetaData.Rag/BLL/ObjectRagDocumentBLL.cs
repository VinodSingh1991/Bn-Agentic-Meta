using Acidaes.MetaData.Rag.DAL.IDAL;
using Acidaes.MetaData.Rag.Model;

namespace Acidaes.MetaData.Rag.BLL
{
    public class ObjectRagDocumentBLL(IObjectRagDocument objectRagDocument)
    {
        private readonly ResponseData _response = new();
        private readonly IObjectRagDocument _objectRagDocument = objectRagDocument;

        public List<ObjectDocument> PrepareObjectDocument(IEnumerable<ObjectDocumentDto> objectRagList)
        {
            if (objectRagList == null || !objectRagList.Any())
            {
                return [];
            }

            List<ObjectDocument> _objectList = [];

            foreach (var obj in objectRagList)
            {
                ObjectDocument o = new()
                {
                    Id = $"{obj.ObjectId}_{obj.ObjectName}",
                    Content = $"{obj.ObjectName} is object in metadata and it table name is {obj.TableName}",
                    MetaData = new()
                    { 
                        ObjectId = obj.ObjectId,
                        ObjectName = obj.ObjectName,
                        TableName = obj.TableName,
                        PrimaryField = obj.PrimaryField,
                        Description = obj.Description
                        
                    }
                };
                _objectList.Add(o);

            }

            return _objectList;
        }
        public async Task<ResponseData> GetObjectRagDocument()
        {
            try
            {
                var objectRagList = await _objectRagDocument.GetObjectDocumentsList();
                var _list = PrepareObjectDocument(objectRagList);
                _response.IsSuccess = "True";
                _response.Message = "Success";
                _response.Data = _list;
                return _response;

            }
            catch (Exception ex) { 
                _response.IsSuccess = "False";
                _response.Message = ex.Message;
                _response.Data = new object();
                return _response;
            }
        }
    }
}
