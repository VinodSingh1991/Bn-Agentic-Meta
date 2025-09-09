
using Acidaes.MetaData.Rag.DAL;
using Acidaes.MetaData.Rag.DAL.IDAL;

namespace Acidaes.MetaData.Rag
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            // Add services to the container.

            builder.Services.AddControllers();
            // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen();

            builder.Services.AddScoped<IRoleRagDocument, RoleRagDocumentRepo>();
            builder.Services.AddScoped<IFieldRagDocument, FieldRagDocumentRepo>();
            builder.Services.AddScoped<IObjectRagDocument, ObjectRagDocumentRepo>();
            builder.Services.AddScoped<ILayoutRagDocument, LayoutRagDocumentRepo>();

            var app = builder.Build();

            // Configure the HTTP request pipeline.
            if (app.Environment.IsDevelopment())
            {
                app.UseSwagger();
                app.UseSwaggerUI();
            }

            app.UseHttpsRedirection();

            app.UseAuthorization();


            app.MapControllers();

            app.Run();
        }
    }
}
