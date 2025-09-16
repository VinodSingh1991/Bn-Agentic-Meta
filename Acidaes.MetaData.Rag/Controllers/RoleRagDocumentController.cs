using Acidaes.MetaData.Rag.BLL;
using Acidaes.MetaData.Rag.DAL.IDAL;
using Acidaes.MetaData.Rag.Model;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace Acidaes.MetaData.Rag.Controllers
{
    [ApiController]
    public class RoleRagDocumentController(IRoleRagDocument roleRagRepository) : ControllerBase
    {
        private readonly RoleRagDocumentBLL _roleRagDocumnts = new(roleRagRepository);
        private readonly ResponseModel _response = new();

        [HttpGet("api/getRoles")]
        public async Task<ResponseModel> GetRoles()
        {
            var roleResponse = await _roleRagDocumnts.GetRoleDocuments();

            if (roleResponse.IsSuccess == "True")
            {
                _response.ResponseData = roleResponse;
                return _response;
            }

            return _response;

        }
    }
}
