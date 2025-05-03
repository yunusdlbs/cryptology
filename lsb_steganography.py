import wave
import numpy as np

def text_to_bits(text):
    """Metni ikili (binary) formata çevirir."""
    bits = ''.join(format(ord(c), '08b') for c in text)
    return bits

def bits_to_text(bits):
    """İkili formattan metne çevirir."""
    text = ''
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text

def hide_message(input_wav, output_wav, message):
    """Mesajı ses dosyasına gizler."""
    # Mesaj uzunluğunu kontrol et
    if len(message) > 160:
        raise ValueError("Mesaj 160 karakterden uzun olamaz!")
    
    # WAV dosyasını oku
    with wave.open(input_wav, 'rb') as wav:
        # Ses verilerini al
        frames = wav.readframes(wav.getnframes())
        samples = np.frombuffer(frames, dtype=np.int16)
        
        # Mesajı bitlere çevir ve uzunluğunu ekle
        message_bits = text_to_bits(message)
        length_bits = format(len(message_bits), '032b')  # Mesaj uzunluğu 32 bit
        bits_to_hide = length_bits + message_bits
        
        if len(bits_to_hide) > len(samples):
            raise ValueError("Ses dosyası mesajı gizlemek için çok kısa!")
        
        # Ses örneklerini kopyala
        modified_samples = samples.copy()
        
        # LSB ile mesajı gizle
        for i, bit in enumerate(bits_to_hide):
            modified_samples[i] = (modified_samples[i] & ~1) | int(bit)
        
        # Yeni WAV dosyasını yaz
        with wave.open(output_wav, 'wb') as wav_out:
            wav_out.setparams(wav.getparams())
            wav_out.writeframes(modified_samples.tobytes())

def extract_message(input_wav):
    """Gizlenmiş mesajı çıkarır."""
    # WAV dosyasını oku
    with wave.open(input_wav, 'rb') as wav:
        frames = wav.readframes(wav.getnframes())
        samples = np.frombuffer(frames, dtype=np.int16)
        
        # İlk 32 bit mesaj uzunluğunu içerir
        length_bits = ''
        for i in range(32):
            length_bits += str(samples[i] & 1)
        message_length = int(length_bits, 2)
        
        # Mesaj bitlerini çıkar
        message_bits = ''
        for i in range(32, 32 + message_length):
            message_bits += str(samples[i] & 1)
        
        # Bitleri metne çevir
        return bits_to_text(message_bits)

def main():
    # Örnek kullanım
    input_wav = "input.wav"
    output_wav = "output.wav"
    message = "Bu 160 karakterlik bir test mesajıdır. Steganaliz ile gizlenmiş! xAI Grok tarafından oluşturuldu."
    
    # Mesajı gizle
    print(f"Gizlenen mesaj: {message}")
    hide_message(input_wav, output_wav, message)
    print("Mesaj ses dosyasına gizlendi!")
    
    # Gizlenmiş mesajı çıkar
    extracted_message = extract_message(output_wav)
    print(f"Çıkarılan mesaj: {extracted_message}")

if __name__ == "__main__":
    main()
