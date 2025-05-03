from PIL import Image
import numpy as np

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

def calculate_complexity(bit_plane):
    """Bit düzleminin karmaşıklığını hesaplar (0-1 arasında)."""
    transitions = 0
    height, width = bit_plane.shape
    for i in range(height):
        for j in range(width - 1):
            if bit_plane[i, j] != bit_plane[i, j + 1]:
                transitions += 1
        if i < height - 1:
            for j in range(width):
                if bit_plane[i, j] != bit_plane[i + 1, j]:
                    transitions += 1
    max_transitions = 2 * (height * (width - 1) + width * (height - 1))
    return transitions / max_transitions if max_transitions > 0 else 0

def hide_message(input_image, output_image, message):
    """Mesajı BPCS ile görüntüsüne gizler."""
    if len(message) > 160:
        raise ValueError("Mesaj 160 karakterden uzun olamaz!")
    
    # Görüntüyü oku
    img = Image.open(input_image).convert('L')
    img_array = np.array(img, dtype=np.uint8)
    
    # Bit düzlemlerine ayır
    bit_planes = [(img_array >> i) & 1 for i in range(8)]
    
    # Mesajı bitlere çevir ve uzunluğunu ekle
    message_bits = text_to_bits(message)
    length_bits = format(len(message_bits), '032b')
    bits_to_hide = length_bits + message_bits
    
    # Karmaşık bit düzlemlerini seç
    complex_planes = []
    for i, plane in enumerate(bit_planes):
        if calculate_complexity(plane) > 0.3:  # Eşik: %30 karmaşıklık
            complex_planes.append(i)
    
    if not complex_planes:
        raise ValueError("Yeterli karmaşık bit düzlemi bulunamadı!")
    
    # Mesajı karmaşık bit düzlemlerine gizle
    bit_index = 0
    for plane_idx in complex_planes:
        plane = bit_planes[plane_idx]
        for i in range(plane.shape[0]):
            for j in range(plane.shape[1]):
                if bit_index < len(bits_to_hide):
                    plane[i, j] = int(bits_to_hide[bit_index])
                    bit_index += 1
                if bit_index >= len(bits_to_hide):
                    break
            if bit_index >= len(bits_to_hide):
                break
        bit_planes[plane_idx] = plane
        if bit_index >= len(bits_to_hide):
            break
    
    # Görüntüyü yeniden oluştur
    output_array = np.zeros_like(img_array)
    for i in range(8):
        output_array |= (bit_planes[i] << i)
    
    Image.fromarray(output_array).save(output_image)

def extract_message(input_image):
    """Gizlenmiş mesajı BPCS ile çıkarır."""
    img = Image.open(input_image).convert('L')
    img_array = np.array(img, dtype=np.uint8)
    bit_planes = [(img_array >> i) & 1 for i in range(8)]
    
    # İlk 32 bit mesaj uzunluğunu içerir
    length_bits = ''
    bit_index = 0
    for plane in bit_planes:
        if calculate_complexity(plane) > 0.3:
            for i in range(plane.shape[0]):
                for j in range(plane.shape[1]):
                    if bit_index < 32:
                        length_bits += str(plane[i, j])
                        bit_index += 1
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
    for plane in bit_planes:
        if calculate_complexity(plane) > 0.3:
            for i in range(plane.shape[0]):
                for j in range(plane.shape[1]):
                    if bit_index < message_length:
                        message_bits += str(plane[i, j])
                        bit_index += 1
                    if bit_index >= message_length:
                        break
                if bit_index >= message_length:
                    break
            if bit_index >= message_length:
                break
    
    return bits_to_text(message_bits)

def main():
    input_image = "input.png"
    output_image = "output.png"
    message = "Bu 160 karakterlik bir test mesajıdır. BPCS ile gizlenmiş! YunusDlb tarafından oluşturuldu."
    
    print(f"Gizlenen mesaj: {message}")
    hide_message(input_image, output_image, message)
    print("Mesaj görüntüsüne gizlendi!")
    
    extracted_message = extract_message(output_image)
    print(f"Çıkarılan mesaj: {extracted_message}")

if __name__ == "__main__":
    main()
