using System.Data.Common;
using Microsoft.Data.SqlClient;

namespace Acidaes.MetaData.Rag.DAL.Helper
{
    public class ConnectionHelper
    {
        public static DbConnection CreateConnection(string connectionString)
        {
            return new SqlConnection(connectionString);
        }
    }
}
