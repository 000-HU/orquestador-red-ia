import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

public class SeguridadRed {
    private static final String LLAVE_MAESTRA = "000-HU-SECRET-99"; // 16 caracteres

    public static String encriptar(String datos) throws Exception {
        SecretKeySpec secretKey = new SecretKeySpec(LLAVE_MAESTRA.getBytes(), "AES");
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        byte[] encriptado = cipher.doFinal(datos.getBytes());
        return Base64.getEncoder().encodeToString(encriptado);
    }

    public static void main(String[] args) {
        try {
            // El orquestador le pasará la latencia como argumento
            if (args.length > 0) {
                System.out.println(encriptar(args[0]));
            }
        } catch (Exception e) {
            System.out.println("ERROR_SEGURIDAD");
        }
    }
}


