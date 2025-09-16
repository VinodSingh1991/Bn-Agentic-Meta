using Acidaes.MetaData.Rag.BLL;
using Acidaes.MetaData.Rag.DAL.IDAL;
using Acidaes.MetaData.Rag.Model;
using Azure;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace Acidaes.MetaData.Rag.Controllers
{
    [ApiController]
    public class LayoutRagDocumentController(ILayoutRagDocument layoutRagDocument) : ControllerBase
    {
        private readonly ResponseModel _response = new();
        private readonly LayoutRagDocumentBLL _layoutRagDocumentBLL = new(layoutRagDocument);

        [HttpGet("api/getLayout")]
        public async Task<ResponseModel> GetLayouts()
        {
            var fieldResponse = await _layoutRagDocumentBLL.GetLayoutRagList();
            if (fieldResponse.IsSuccess == "True")
            {
                _response.ResponseData = fieldResponse;
            }

            return _response;
        }
    }
}
