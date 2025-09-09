using Acidaes.MetaData.Rag.Model;

namespace Acidaes.MetaData.Rag.DAL.IDAL
{
    public interface IRoleRagDocument
    {
        public Task<IEnumerable<RoleDocumentDTO>> GetRoleDocumentsList();
    }
}
