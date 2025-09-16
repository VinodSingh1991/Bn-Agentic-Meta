using Acidaes.MetaData.Rag.Model;

namespace Acidaes.MetaData.Rag.DAL.IDAL
{
    public interface IFieldRagDocument
    {
        public Task<IEnumerable<FieldDocumentDto>> GetFieldDocument(bool isSystemField);
    }
}
