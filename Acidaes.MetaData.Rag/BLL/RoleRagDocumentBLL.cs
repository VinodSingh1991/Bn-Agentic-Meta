using Acidaes.MetaData.Rag.DAL.IDAL;
using Acidaes.MetaData.Rag.Model;

namespace Acidaes.MetaData.Rag.BLL
{
    public class RoleRagDocumentBLL(IRoleRagDocument roleRagRepository)
    {
        private readonly ResponseData _response = new();
        private readonly IRoleRagDocument _roleRagRepository = roleRagRepository;

        public List<RoleDocument> PrepareRagDocument(IEnumerable<RoleDocumentDTO> documents)
        {
            List<RoleDocument> _roleDocs = [];

            if (documents == null || !documents.Any())
                return [];

            foreach (var document in documents)
            {
                RoleDocument doc = new()
                {
                    Id = $"{document.RoleId}_{document.RoleName}",
                    Content = document.RoleDescription,
                    MetaData = new()
                    {
                        RoleId = document.RoleId,
                        RoleName = document.RoleName,
                        RoleDescription = document.RoleDescription,
                        Language = "English",
                        Tags = [document.RoleName]
                    }
                };
                _roleDocs.Add(doc);
            }

            return _roleDocs;
        }

        public async Task<ResponseData> GetRoleDocuments()
        {
            try
            {
                var roleDocFromDb = await _roleRagRepository.GetRoleDocumentsList();

                var roleDocuments = PrepareRagDocument(roleDocFromDb);
                _response.Data = roleDocuments;
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
