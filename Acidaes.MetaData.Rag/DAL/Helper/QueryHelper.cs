namespace Acidaes.MetaData.Rag.DAL.Helper
{
    public static class QueryHelper
    {
        public const string RoleRagDocumentQuery = "select * from RoleView where OwnerId = 101";
        public const string GetObectMastersQuery = "select * from ObjectMasterTableList where ItemType in(1,6,7,8,9)";
        public const string GetObjectListForRagQuery = "select TableName, ItemType, PrimaryField, SubjectField from ObjectMasterTableList where ItemType in(1,6,7,8,9)";
        public const string GetCustomFields = "select Label, FieldId, TableName, KeyId, Type, Mandatory, Description,InternalLabel, FieldName, DisplayType from CustomFieldSchema where OwnerId = 101 and KeyId in(1,6,7,8,9)";
        public const string GetSystemFields = "select Label, FieldId, TableName, KeyId, Type, Mandatory, Description,InternalLabel, FieldName, DisplayType from ObjectSchema where OwnerId = 101 and KeyId in(1,6,7,8,9)";
        public const string GetLayoutWithRolesAndObject = "select distinct lg.ItemTypeID,  lg.LayoutID,ul.Name as LayoutName,lgr.RoleId,Az_Role.Name,lg.LayoutXML from LayoutGroupView lg \r\njoin LayoutGroupRoleMapping lgr on lgr.OwnerId = lg.OwnerID and lgr.LayoutId = lg.LayoutID\r\nand lg.OwnerId = 101 and LayoutType in (2,1) and ItemTypeID in (1,6,7,8,9)\r\njoin UILayoutMaster ul on (ul.OwnerID = lg.OwnerID or ul.OwnerID = 0) and ul.ItemTypeID = lg.ItemTypeID and ul.LayoutID = lg.LayoutID\r\nleft join Az_Role on (Az_Role.AppOwnerID = lgr.OwnerID or Az_Role.AppOwnerID = 0) and lgr.RoleId = Az_Role.RoleID";
    }
}
