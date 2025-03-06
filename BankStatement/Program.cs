using BankStatement.Services;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () =>
{
    ImportService importService = new ImportService();
    importService.Import(Path.Combine(Directory.GetCurrentDirectory(), "Files", "test.pdf"));
});

app.Run();