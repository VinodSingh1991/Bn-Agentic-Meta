using Acidaes.MetaData.Rag.DAL.IDAL;
using Acidaes.MetaData.Rag.Model;

namespace Acidaes.MetaData.Rag.BLL
{
    public class RoleRagDocumentBLL(IRoleRagDocument roleRagRepository)
    {
        private readonly ResponseData _response = new();
        private readonly IRoleRagDocument _roleRagRepository = roleRagRepository;

        public List<RoleDocumentMetaData> PrepareRagDocument(IEnumerable<RoleDocumentDTO> documents)
        {
            List<RoleDocumentMetaData> _roleDocs = [];
            HashSet<string> addedRolesKeys = new();

            if (documents == null || !documents.Any())
                return [];

            foreach (var document in documents)
            {
                var roleId = document.RoleId;

                if (addedRolesKeys.Contains(roleId))
                {
                    continue;
                }
                RoleDocumentMetaData doc = new()
                {
                    RoleId = roleId,
                    RoleName = document.RoleName,
                    RoleDescription = document.RoleDescription
                };

                addedRolesKeys.Add(roleId);
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
