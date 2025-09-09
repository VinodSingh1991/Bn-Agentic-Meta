using Acidaes.MetaData.Rag.Model;
using System.Xml;
using System.Xml.Linq;

namespace Acidaes.MetaData.Rag.Helper
{
    public class Utility
    {
        public static string? GetSafeString(object? obj)
        {
            return obj?.ToString();
        }

        public static string GetObjectNameById(int itemType)
        {
            string objectName = itemType switch
            {
                1 => "Activity",
                6 => "Leads",
                7 => "Accounts",
                8 => "Opportunities",
                9 => "Cases",
                _ => "",
            };
            return objectName;
        }

        public static Layout GetFieldMetaDataFromXML(string xmlLayout)
        {
            var layouts = new Layout();

            var doc = new XmlDocument();
            doc.LoadXml(xmlLayout);

            var fieldIds = GetLayoutFields(doc);
            var tabs = GetTabs(doc);
            var sections = GetSections(doc, tabs);

            layouts.Fields = fieldIds;
            layouts.Sections = sections;
            layouts.Tabs = tabs;

            return layouts;
        }
        public static List<string> GetLayoutFields(XmlDocument xmlLayout)
        {
            var fieldIds = new List<string>();

            XmlNodeList? nodeList = xmlLayout.SelectNodes("//cols/col");
            if (nodeList != null)
            {
                foreach (XmlNode node in nodeList)
                {
                    var fldId = ((XmlElement)node).GetAttribute("fieldid");

                    if (fldId != "blankcell")
                    {
                        fieldIds.Add(fldId);
                    }
                }
            }

            return fieldIds;
        }

        public static List<string> GetSectionFields(XmlNode sectionXml)
        {
            var fieldIds = new List<string>();

            XmlNodeList? nodeList = sectionXml.SelectNodes(".//cols/col");
            if (nodeList != null)
            {
                foreach (XmlNode node in nodeList)
                {
                    var fldId = ((XmlElement)node).GetAttribute("fieldid");

                    if (fldId != "blankcell")
                    {
                        fieldIds.Add(fldId);
                    }
                }
            }

            return fieldIds;
        }

        public static List<LayoutTab> GetTabs(XmlDocument xmlLayout)
        {
            var tabs = new List<LayoutTab>();

            XmlNodeList? nodeList = xmlLayout.SelectNodes("//tabs/tab");
            if (nodeList != null)
            {
                foreach (XmlNode node in nodeList)
                {
                    var layoutTab = new LayoutTab();

                    var element = (XmlElement)node;
                    string id = element.GetAttribute("id");
                    string tabName = string.Empty;

                    var textNode = node.SelectSingleNode("text/lang[@text]");

                    if (textNode is XmlElement langElement)
                    {
                        tabName = langElement.GetAttribute("text");

                    }
                    layoutTab.TabName = tabName;
                    layoutTab.TabId = id;


                    tabs.Add(layoutTab);
                }
            }

            return tabs;
        }

        public static List<LayoutSections> GetSections(XmlDocument xmlLayout, List<LayoutTab> tabs)
        {
            var sections = new List<LayoutSections>();

            XmlNodeList? sectionList = xmlLayout.SelectNodes("//tab/section");
            if (sectionList != null)
            {
                foreach (XmlNode sec in sectionList)
                {
                    var fields = GetSectionFields(sec);

                    var tabElement = (XmlElement)sec;

                    string tabId = tabElement.GetAttribute("id");

                    var tabName = tabs.FirstOrDefault(tab => tab.TabId == tabId)?.TabName ?? string.Empty;

                    string _sectionName = string.Empty;

                    var textNode = sec.SelectSingleNode("text/lang[@text]");

                    if (textNode is XmlElement langElement)
                    {
                        _sectionName = langElement.GetAttribute("text");
                    }

                    var section = new LayoutSections();
                    section.TabId = tabId;
                    section.TabName = tabName;
                    section.SectionName = _sectionName;
                    section.SectionFields = fields;

                    sections.Add(section);
                }
            }

            return sections;
        }


        public static string GetFieldTypeName(FieldType fieldType)
        {
            return fieldType switch
            {
                FieldType.None => "None",
                FieldType.Lookup => "Lookup",
                FieldType.Number => "Number",
                FieldType.Text => "Text",
                FieldType.Amount => "Amount",
                FieldType.DateTime => "DateTime",
                FieldType.Email => "Email",
                FieldType.Url => "Url",
                FieldType.Phone => "Phone",
                FieldType.Date => "Date",
                FieldType.Comments => "Comments",
                FieldType.Check => "Check",
                FieldType.MulticurrencyAmount => "MulticurrencyAmount",
                FieldType.Time => "Time",
                FieldType.UserPicker => "UserPicker",
                FieldType.MultiPicker => "MultiPicker",
                FieldType.ComputedField => "ComputedField",
                FieldType.SequenceNumber => "SequenceNumber",
                FieldType.Decimal => "Decimal",
                FieldType.Percentage => "Percentage",
                FieldType.Document => "Document",
                FieldType.Duration => "Duration",
                FieldType.CurrencyPicker => "CurrencyPicker",
                FieldType.ObjectNumber => "ObjectNumber",
                FieldType.BigInt => "BigInt",
                FieldType.MultiLevel => "MultiLevel",
                FieldType.ExternalField => "ExternalField",
                FieldType.LookupWithId => "LookupWithId",
                FieldType.TemplatePicker => "TemplatePicker",
                FieldType.HTML => "HTML",
                FieldType.Aggregation => "Aggregation",
                FieldType.Image => "Image",
                FieldType.LongText => "LongText",
                FieldType.ReferenceLookup => "ReferenceLookup",
                FieldType.SmartImage => "SmartImage",
                FieldType.Rating => "Rating",
                FieldType.ProgressBar => "ProgressBar",
                FieldType.WebIntegerationUrl => "WebIntegrationUrl",
                _ => "Text",
            };
        }

        public static string GetFieldOperationName(FieldOperation operation)
        {
            return operation switch
            {
                FieldOperation.None => "None",
                FieldOperation.Equal => "Equal",
                FieldOperation.Greater => "Greater",
                FieldOperation.Lesser => "Lesser",
                FieldOperation.NotEqual => "NotEqual",
                FieldOperation.GreaterEqual => "GreaterEqual",
                FieldOperation.LesserEqual => "LesserEqual",
                FieldOperation.Like => "Like",
                FieldOperation.AnyOf => "AnyOf",
                FieldOperation.In => "In",
                FieldOperation.NotIn => "NotIn",
                FieldOperation.LikeAnd => "LikeAnd",
                FieldOperation.SameAsItemValue => "SameAsItemValue",
                FieldOperation.NotSameAsItemValue => "NotSameAsItemValue",
                FieldOperation.IsSpecified => "IsSpecified",
                FieldOperation.IsNotSpecified => "IsNotSpecified",
                FieldOperation.LikeAsItemValue => "LikeAsItemValue",
                FieldOperation.Expression => "Expression",
                _ => "None",
            };
        }


    }
}
