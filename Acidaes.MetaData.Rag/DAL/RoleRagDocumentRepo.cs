using Acidaes.MetaData.Rag.DAL.Helper;
using Acidaes.MetaData.Rag.DAL.IDAL;
using Acidaes.MetaData.Rag.Model;
using System.Data;

namespace Acidaes.MetaData.Rag.DAL
{
    public class RoleRagDocumentRepo : IRoleRagDocument
    {
        private readonly IConfiguration _configuration;
        private readonly string? _connectionString;
        private readonly List<RoleDocumentDTO> _roleDocumentList; 
        public RoleRagDocumentRepo(IConfiguration configuration)
        {
            _configuration = configuration;
            _connectionString = _configuration.GetConnectionString("DefaultConnection");
            _roleDocumentList = [];
        }
        public async Task<IEnumerable<RoleDocumentDTO>> GetRoleDocumentsList()
        {
            var sqlQuery = QueryHelper.RoleRagDocumentQuery;

            if(string.IsNullOrEmpty(_connectionString))
                throw new ArgumentNullException("Connection string is null or empty");

            using (var connection = ConnectionHelper.CreateConnection(_connectionString))
            {
               using var dbCommand = connection.CreateCommand();
                dbCommand.CommandText = sqlQuery;
                dbCommand.CommandType = CommandType.Text;
                dbCommand.CommandTimeout = 10;
                connection.Open();

                var reader = await dbCommand.ExecuteReaderAsync();

                if (reader != null) {

                    var roleIdIndex = reader.GetOrdinal("RoleId");
                    var descIndex = reader.GetOrdinal("Description");
                    var nameIndex = reader.GetOrdinal("Name");

                    while (reader.Read()) {
                        RoleDocumentDTO roleDocument = new()
                        {
                            RoleId = reader.IsDBNull(roleIdIndex) ? string.Empty : reader.GetInt32(roleIdIndex).ToString(),
                            RoleDescription = reader.IsDBNull(descIndex) ? string.Empty : reader.GetString(descIndex),
                            RoleName = reader.IsDBNull(nameIndex) ? string.Empty : reader.GetString(nameIndex)
                        };
                        _roleDocumentList.Add(roleDocument);
                    }

                }

                connection.Close();
            }

            return _roleDocumentList;
        }
    }
}
