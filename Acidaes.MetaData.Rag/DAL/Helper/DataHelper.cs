using System.Data.Common;
using System.Data;

namespace Acidaes.MetaData.Rag.DAL.Helper
{
    public class DalHelper
    {
        public static DbParameter CreateDbParameter(DbCommand command, string parameterName, object value, TypeCode typeCode)
        {
            var parameter = command.CreateParameter();
            parameter.ParameterName = parameterName;
            parameter.Value = value;
            parameter.DbType = GetDbType(typeCode);
            return parameter;
        }

        public static T GetValue<T>(IDataReader reader, string columnName)
        {
            var index = reader.GetOrdinal(columnName);

            if (reader.IsDBNull(index))
                return default!;

            return (T)reader.GetValue(index);
        }

        public static DbType GetDbType(TypeCode typeCode)
        {
            switch (typeCode)
            {
                case TypeCode.Int32:
                    return DbType.Int32;

                case TypeCode.Int64:
                    return DbType.Int64;

                case TypeCode.Boolean:
                    return DbType.Boolean;

                case TypeCode.Decimal:
                    return DbType.Decimal;

                case TypeCode.DateTime:
                    return DbType.DateTime;

                default:
                    return DbType.String;
            }
        }

    }
}
