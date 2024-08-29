import java.io.FileInputStream;
import org.apache.pdfbox.pdfparser.PDFParser;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

public class PdfBoxUtils {
    public static String extractText(String filename) throws Exception {
        FileInputStream input = new FileInputStream(filename);
        PDFParser parser = new PDFParser(input);
        parser.parse();
        PDDocument document = parser.getPDDocument();
        PDFTextStripper stripper = new PDFTextStripper();
        String text = stripper.getText(document);
        input.close();
        document.close();
        return text;
    }
}
