class QueryHelper:
    GetRoles = "select * from RoleView"

    GetObjects = "select * from ObjectMasterTableList where ItemType in(1,2,4,5,6,7,8,9,19,34,43,56)"

    GetObjectList = "select TableName, ItemType, PrimaryField, SubjectField from ObjectMasterTableList where ItemType in(1,2,4,5,6,7,8,9,19,34,43,56)"

    GetCustomFields = "select Label, FieldId, TableName, KeyId, Type, Description, FieldName, DisplayType from CustomFieldSchema where OwnerId = 101 and KeyId in(1,2,4,5,6,7,8,9,19,34,43,56)"

    GetSystemFields = "select * from ObjectSchema where OwnerId in (0, 101) and KeyId in(1,2,4,5,6,7,8,9,19,34,43,56)"

    GetLayoutWithRolesAndObject = "select distinct lg.ItemTypeID,  lg.LayoutID,ul.Name as LayoutName,lgr.RoleId, Az_Role.Name,lg.LayoutXML from LayoutGroupView lg join LayoutGroupRoleMapping lgr on lgr.OwnerId = lg.OwnerID and lgr.LayoutId = lg.LayoutID and lg.OwnerId = 101 and LayoutType in (2,1) and ItemTypeID in (1,2,4,5,6,7,8,9,19,34,43,56) join UILayoutMaster ul on (ul.OwnerID = lg.OwnerID or ul.OwnerID = 0) and ul.ItemTypeID = lg.ItemTypeID and ul.LayoutID = lg.LayoutID left join Az_Role on (Az_Role.AppOwnerID = lgr.OwnerID or Az_Role.AppOwnerID = 0) and lgr.RoleId = Az_Role.RoleID"
    
    
    GetLayoutGroupView = "select ItemTypeID, LayoutID, LayoutType, LayoutXML from LayoutGroupView where OwnerId in (0, 101) and LayoutType = 2 and ItemTypeID in(1,2,4,5,6,7,8,9,19,34,43,56)"
    
    GetLayoutUIMaster = "select  LayoutID, ItemTypeID, Name from UILayoutMaster where OwnerId in (0, 101) and ItemTypeID in(1,2,4,5,6,7,8,9,19,34,43,56)"
    
    GetLayoutGroupRoleMapping = "select * from LayoutGroupRoleMapping where OwnerId in (0, 101)"
    
    GetListingFromRptQuery = "select * from RPT_Query where OwnerID in (0,101) and KeyId in (1,2,4,5,6,7,8,9,19,34,43,56)"
    
    GetListingFromGold5Listing = "select * from crmnextlisting_gold5 where OwnerID in (0,101) and RelatedToTypeID in (1,2,4,5,6,7,8,9,19,34,43,56)"
    
    GetListingFromObjectRelationship = "select distinct keyid,listingtype,RelatedKeyID, RelationShipID, RelationShipName from objectrelationship where KeyID in (1,2,4,5,6,7,8,9,19,34,43,56) and RelatedKeyID in (1,2,4,5,6,7,8,9,19,34,43,56)"
