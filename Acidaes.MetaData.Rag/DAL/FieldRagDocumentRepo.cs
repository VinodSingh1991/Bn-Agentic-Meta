using Acidaes.MetaData.Rag.DAL.Helper;
using Acidaes.MetaData.Rag.DAL.IDAL;
using Acidaes.MetaData.Rag.Model;
using System.Data;

namespace Acidaes.MetaData.Rag.DAL
{
    public class FieldRagDocumentRepo : IFieldRagDocument
    {
        private readonly IConfiguration _configuration;
        private readonly string? _connectionString;
        private readonly List<FieldDocumentDto> _fieldDocumentList;

        public FieldRagDocumentRepo(IConfiguration configuration)
        {
            _configuration = configuration;
            _connectionString = _configuration.GetConnectionString("DefaultConnection");
            _fieldDocumentList = [];
        }
        public async Task<IEnumerable<FieldDocumentDto>> GetFieldDocument(bool isSystemField)
        {
            var sqlQuery = isSystemField ? QueryHelper.GetSystemFields : QueryHelper.GetCustomFields;

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
                    var fieldIdIndex = reader.GetOrdinal("FieldId");
                    var fieldNameIndex = reader.GetOrdinal("FieldName");
                    var tableNameIndex = reader.GetOrdinal("TableName");
                    var objectKeyIdIndex = reader.GetOrdinal("KeyId");
                    var typeIndex = reader.GetOrdinal("Type");
                    //var mandatoryIndex = reader.GetOrdinal("Mandatory");
                    var descriptionIndex = reader.GetOrdinal("Description");
                    //var internalLabelIndex = reader.GetOrdinal("InternalLabel");
                    var displayTypeIndex = reader.GetOrdinal("DisplayType");
                    var LabelIndex = reader.GetOrdinal("Label");
                    //var LayoutFieldId = reader.GetOrdinal("LayoutFieldId");

                    while (reader.Read())
                    {
                        FieldDocumentDto fieldDocument = new()
                        {
                            FieldId = reader.IsDBNull(fieldIdIndex) ? string.Empty : reader.GetInt64(fieldIdIndex).ToString(),
                            FieldLabel = reader.IsDBNull(LabelIndex) ? string.Empty : reader.GetString(LabelIndex),
                            FieldName = reader.IsDBNull(fieldNameIndex) ? string.Empty : reader.GetString(fieldNameIndex),
                            TableName = reader.IsDBNull(tableNameIndex) ? string.Empty : reader.GetString(tableNameIndex),
                            ObjectId = reader.GetInt32(objectKeyIdIndex),
                            FieldType = (FieldType)reader.GetInt32(typeIndex),
                            IsMandatory = false, //!reader.IsDBNull(mandatoryIndex) && reader.GetBoolean(mandatoryIndex),
                            Description = reader.IsDBNull(descriptionIndex) ? string.Empty : reader.GetString(descriptionIndex),
                            DisplayLabel = string.Empty,
                            LayoutFieldId = isSystemField ? reader.IsDBNull(reader.GetOrdinal("LayoutFieldId")) ? string.Empty : reader.GetString(reader.GetOrdinal("LayoutFieldId")).ToString() : reader.IsDBNull(fieldNameIndex) ? string.Empty : reader.GetString(fieldNameIndex),
                        };
                        _fieldDocumentList.Add(fieldDocument);

                    }
                }

                connection.Close();
            }

            return _fieldDocumentList;
        }
    }
}
