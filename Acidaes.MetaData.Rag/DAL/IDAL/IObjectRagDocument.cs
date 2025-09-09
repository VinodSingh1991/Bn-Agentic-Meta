using Acidaes.MetaData.Rag.Model;

namespace Acidaes.MetaData.Rag.DAL.IDAL
{
    public interface IObjectRagDocument
    {
        public Task<IEnumerable<ObjectDocumentDto>> GetObjectDocumentsList();
    }
}
