using Acidaes.MetaData.Rag.DAL.Helper;
using Acidaes.MetaData.Rag.DAL.IDAL;
using Acidaes.MetaData.Rag.Helper;
using Acidaes.MetaData.Rag.Model;
using System.Data;

namespace Acidaes.MetaData.Rag.DAL
{
    public class ObjectRagDocumentRepo : IObjectRagDocument
    {
        private readonly IConfiguration _configuration;
        private readonly string? _connectionString;
        private readonly List<ObjectDocumentDto> _objectDocumentList;

        public ObjectRagDocumentRepo(IConfiguration configuration)
        {
            _configuration = configuration;
            _connectionString = _configuration.GetConnectionString("DefaultConnection");
            _objectDocumentList = [];
        }
        public async Task<IEnumerable<ObjectDocumentDto>> GetObjectDocumentsList()
        {
            var sqlQuery = QueryHelper.GetObjectListForRagQuery;
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

                if (reader != null)
                {
                    var TableName = reader.GetOrdinal("TableName");
                    var ItemType = reader.GetOrdinal("ItemType");
                    var PrimaryField = reader.GetOrdinal("PrimaryField");
                    var SubjectField = reader.GetOrdinal("SubjectField");

                    while (reader.Read())
                    {
                        ObjectDocumentDto objDoc = new()
                        {
                            ObjectName = reader.IsDBNull(TableName) ? string.Empty : Utility.GetObjectNameById(reader.GetInt32(ItemType)),
                            ObjectId = reader.GetInt32(ItemType),
                            PrimaryField = reader.IsDBNull(PrimaryField) ? string.Empty : reader.GetString(PrimaryField),
                            SubjectField = reader.IsDBNull(SubjectField) ? string.Empty : reader.GetString(SubjectField),
                            TableName = reader.IsDBNull(TableName) ? string.Empty : reader.GetString(TableName)
                        };
                        _objectDocumentList.Add(objDoc);

                    }
                }

                connection.Close();
            }

            return _objectDocumentList;
        }
    }
}
