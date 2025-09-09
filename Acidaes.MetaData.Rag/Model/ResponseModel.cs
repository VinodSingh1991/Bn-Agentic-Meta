namespace Acidaes.MetaData.Rag.Model
{
    public class ResponseData
    {
        public string IsSuccess { get; set; } = "True";
        public string Message { get; set; } = "Success";
        public object Data { get; set; } = new object();
    }

    public class ResponseModel
    {
        public ResponseData ResponseData { get; set; } = new ResponseData();
    }
}
