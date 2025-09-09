using Acidaes.MetaData.Rag.DAL.Helper;
using Acidaes.MetaData.Rag.DAL.IDAL;
using Acidaes.MetaData.Rag.Helper;
using Acidaes.MetaData.Rag.Model;
using System.Data;
using System.Xml;

namespace Acidaes.MetaData.Rag.DAL
{
    public class LayoutRagDocumentRepo : ILayoutRagDocument
    {
        private readonly IConfiguration _configuration;
        private readonly string? _connectionString;
        private readonly List<LayoutSectionDocumentDTO> _layoutDocumentList;

        public LayoutRagDocumentRepo(IConfiguration configuration)
        {
            _configuration = configuration;
            _connectionString = _configuration.GetConnectionString("DefaultConnection");
            _layoutDocumentList = [];
        }

        public async Task<IEnumerable<LayoutSectionDocumentDTO>> GetLayoutSectionDocumentsList()
        {
            var sqlQuery = QueryHelper.GetLayoutWithRolesAndObject;
            if (string.IsNullOrEmpty(_connectionString))
            {
                throw new ArgumentNullException("Connection string is null or empty");
            }

            using (var connection = ConnectionHelper.CreateConnection(_connectionString))
            {
                using var dbCommand = connection.CreateCommand();
                dbCommand.CommandText = sqlQuery;
                dbCommand.CommandType = CommandType.Text;
                dbCommand.CommandTimeout = 10;
                connection.Open();

                var reader = await dbCommand.ExecuteReaderAsync();
                //ItemTypeID LayoutID LayoutName RoleId Name LayoutXML
                if (reader != null)
                {
                    var LayoutID = reader.GetOrdinal("LayoutID");
                    var ItemTypeID = reader.GetOrdinal("ItemTypeID");
                    var LayoutName = reader.GetOrdinal("LayoutName");
                    var RoleId = reader.GetOrdinal("RoleId");
                    var Name = reader.GetOrdinal("Name");
                    var LayoutXML = reader.GetOrdinal("LayoutXML");


                    while (reader.Read())
                    {
                        LayoutSectionDocumentDTO objDoc = new()
                        {
                            ObjectName = Utility.GetObjectNameById(reader.GetInt32(ItemTypeID)),
                            ObjectId = reader.GetInt32(ItemTypeID),
                            LayoutId = reader.GetInt32(LayoutID),
                            LayoutName = reader.IsDBNull(LayoutName) ? string.Empty : reader.GetString(LayoutName),
                            RoleId = reader.GetInt32(RoleId),
                            RoleName = reader.IsDBNull(Name) ? string.Empty : reader.GetString(Name),
                            LayoutXml = reader.IsDBNull(LayoutXML)? string.Empty: reader.GetString(LayoutXML).ToString(),

                        };
                        _layoutDocumentList.Add(objDoc);

                    }
                }

                connection.Close();
            }

            return _layoutDocumentList;
        }
    }
}
