using Acidaes.MetaData.Rag.BLL;
using Acidaes.MetaData.Rag.DAL.IDAL;
using Acidaes.MetaData.Rag.Model;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;
using System.Text.Json.Serialization;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace Acidaes.MetaData.Rag.Controllers
{
    [ApiController]
    public class FieldRagDocumentController(IFieldRagDocument fieldRagDocument, ILayoutRagDocument layoutRagDocument) : ControllerBase
    {
        private readonly ResponseModel _response = new();
        private readonly FieldDocumentBLL _fieldDocumentBLL = new(fieldRagDocument, layoutRagDocument);

        [HttpGet("api/getFieldRagDocuemnt")]
        public async Task<ResponseModel> GetFieldRagDocument()
        {
           var fieldResponse = await _fieldDocumentBLL.GetFieldDocuments();
            if (fieldResponse.IsSuccess == "True")
            {
                _response.ResponseData = fieldResponse;
            }

            return _response;
        }
    }
}
