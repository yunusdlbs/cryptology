from PIL import Image
import numpy as np
from scipy.fft import dct, idct

def text_to_bits(text):
    """Metni ikili formata çevirir."""
    return ''.join(format(ord(c), '08b') for c in text)

def bits_to_text(bits):
    """İkili formattan metne çevirir."""
    text = ''
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text

def hide_message(input_image, output_image, message):
    """Mesajı JPEG görüntüsüne DCT ile gizler."""
    if len(message) > 160:
        raise ValueError("Mesaj 160 karakterden uzun olamaz!")
    
    # Görüntüyü oku
    img = Image.open(input_image).convert('L')  # Gri tonlamaya çevir
    img_array = np.array(img, dtype=np.float32)
    
    # 8x8 bloklara böl
    height, width = img_array.shape
    if height % 8 != 0 or width % 8 != 0:
        raise ValueError("Görüntü boyutları 8'e tam bölünmeli!")
    
    # Mesajı bitlere çevir ve uzunluğunu ekle
    message_bits = text_to_bits(message)
    length_bits = format(len(message_bits), '032b')  # 32 bit uzunluk
    bits_to_hide = length_bits + message_bits
    
    # DCT uygulama
    dct_blocks = np.zeros_like(img_array)
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = img_array[i:i+8, j:j+8]
            dct_blocks[i:i+8, j:j+8] = dct(dct(block.T, norm='ortho').T, norm='ortho')
    
    # Mesaj bitlerini DCT katsayılarına gizle
    bit_index = 0
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            for u in range(8):
                for v in range(8):
                    if bit_index < len(bits_to_hide) and u + v > 4:  # Orta-yüksek frekans katsayıları
                        coeff = dct_blocks[i+u, j+v]
                        dct_blocks[i+u, j+v] = int(coeff) | int(bits_to_hide[bit_index])
                        bit_index += 1
                    if bit_index >= len(bits_to_hide):
                        break
                if bit_index >= len(bits_to_hide):
                    break
            if bit_index >= len(bits_to_hide):
                break
        if bit_index >= len(bits_to_hide):
            break
    
    # Ters DCT ile görüntüyü geri dönüştür
    output_array = np.zeros_like(img_array)
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = dct_blocks[i:i+8, j:j+8]
            output_array[i:i+8, j:j+8] = idct(idct(block.T, norm='ortho').T, norm='ortho')
    
    # Görüntüyü kaydet
    output_array = np.clip(output_array, 0, 255).astype(np.uint8)
    Image.fromarray(output_array).save(output_image, quality=95)

def extract_message(input_image):
    """Gizlenmiş mesajı JPEG görüntüsünden çıkarır."""
    img = Image.open(input_image).convert('L')
    img_array = np.array(img, dtype=np.float32)
    
    height, width = img_array.shape
    dct_blocks = np.zeros_like(img_array)
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = img_array[i:i+8, j:j+8]
            dct_blocks[i:i+8, j:j+8] = dct(dct(block.T, norm='ortho').T, norm='ortho')
    
    # İlk 32 bit mesaj uzunluğunu içerir
    length_bits = ''
    bit_index = 0
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            for u in range(8):
                for v in range(8):
                    if bit_index < 32 and u + v > 4:
                        coeff = dct_blocks[i+u, j+v]
                        length_bits += str(int(coeff) & 1)
                        bit_index += 1
                    if bit_index >= 32:
                        break
                if bit_index >= 32:
                    break
            if bit_index >= 32:
                break
        if bit_index >= 32:
            break
    
    message_length = int(length_bits, 2)
    
    # Mesaj bitlerini çıkar
    message_bits = ''
    bit_index = 0
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            for u in range(8):
                for v in range(8):
                    if bit_index < message_length and u + v > 4:
                        coeff = dct_blocks[i+u, j+v]
                        message_bits += str(int(coeff) & 1)
                        bit_index += 1
                    if bit_index >= message_length:
                        break
                if bit_index >= message_length:
                    break
            if bit_index >= message_length:
                break
        if bit_index >= message_length:
            break
    
    return bits_to_text(message_bits)

def main():
    input_image = "input.jpg"
    output_image = "output.jpg"
    message = "Bu 160 karakterlik bir test mesajıdır. JPEG DCT ile gizlenmiş! YunusDlb tarafından oluşturuldu."
    
    print(f"Gizlenen mesaj: {message}")
    hide_message(input_image, output_image, message)
    print("Mesaj görüntüsüne gizlendi!")
    
    extracted_message = extract_message(output_image)
    print(f"Çıkarılan mesaj: {extracted_message}")

if __name__ == "__main__":
    main()
