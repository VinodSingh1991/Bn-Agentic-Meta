using Acidaes.MetaData.Rag.Model;

namespace Acidaes.MetaData.Rag.DAL.IDAL
{
    public interface ILayoutRagDocument
    {
        public Task<IEnumerable<LayoutSectionDocumentDTO>> GetLayoutSectionDocumentsList();
    }
}
