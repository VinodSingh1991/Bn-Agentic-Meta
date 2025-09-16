using Acidaes.MetaData.Rag.BLL;
using Acidaes.MetaData.Rag.DAL.IDAL;
using Acidaes.MetaData.Rag.Model;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace Acidaes.MetaData.Rag.Controllers
{
    [ApiController]
    public class ObjectRagDocumentController(IObjectRagDocument objectRagDocument) : ControllerBase
    {
        private readonly ResponseModel _response = new();
        private readonly ObjectRagDocumentBLL _objectRagDocumentBLL = new(objectRagDocument);

        [HttpGet("api/getObjects")]
        public async Task<ResponseModel> GetObjects()
        {
            var objectList = await _objectRagDocumentBLL.GetObjectRagDocument();
            if (objectList.IsSuccess == "True")
            {
                _response.ResponseData = objectList;
            }
            return _response;
        }
    }
}
