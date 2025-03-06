using System.Diagnostics;
using UglyToad.PdfPig;
using UglyToad.PdfPig.Content;

namespace BankStatement.Services
{
    public class ImportService
    {
        public void Import(string filePath)
        {
            string path = Path.Combine(Directory.GetCurrentDirectory(), "Files", "file-pdf-chuyen-khoan.pdf");
            using (PdfDocument document = PdfDocument.Open(filePath))
            {
                foreach (Page page in document.GetPages())
                {
                    string pageText = page.Text;

                    foreach (Word word in page.GetWords())
                    {
                        if (word.Text.Contains("5213.45946"))
                        {

                        }
                    }
                }
            }
        }
    }
}
