# cryptology
some python codes related with cryptology methods.

1. LSB (Least Significant Bit Insertion) Algoritması
lsb_steganography.py  ; Python'da LSB (Least Significant Bit Insertion) algoritmasını kullanarak ses veya video verilerine 160 karakterlik bir mesajı gizleyen bir örnek kod yapısı hazırladım. Bu örnekte, bir ses dosyası (WAV formatı) üzerinde LSB algoritması uygulanır, çünkü ses dosyaları LSB için yaygın bir kullanım alanıdır. Video için de benzer bir mantık kullanılabilir, ancak bu örnekte ses dosyasına odaklandım.
LSB (Least Significant Bit Insertion), bir dijital ortamda (örneğin, ses, görüntü veya video) verinin en az anlamlı bitlerini (least significant bits) değiştirerek mesaj gizleme işlemidir. Örneğin, bir ses dosyasındaki her örnek (sample) değerinin en düşük bitini değiştirerek bir mesajın bitlerini sırayla gömeriz. Bu değişiklik, insan kulağının algılayamayacağı kadar küçüktür, bu nedenle ses kalitesinde fark edilebilir bir bozulma olmaz.

2. JPEG Algoritması, görüntü dosyalarını sıkıştırmak için kullanılan DCT (Discrete Cosine Transform - Ayrık Kosinus Dönüşümü) tabanlı bir yöntemdir. Steganografi bağlamında, DCT katsayıları manipüle edilerek veri gizlenir.
JPEG sıkıştırması, görüntüyü 8x8 piksel bloklara böler ve her blok için DCT uygulanır. Bu, piksel verilerini frekans bileşenlerine dönüştürür.
DCT katsayılarının (özellikle düşük frekanslı olmayan katsayılar) en az anlamlı bitleri değiştirilerek mesaj bitleri gömülür.
Değişiklikler, görüntü kalitesinde gözle görülür bozulmalara neden olmayacak şekilde yapılır.
Çıkarma işlemi, aynı DCT katsayılarından mesaj bitlerinin okunmasıyla gerçekleştirilir.

3. BPCS (Bit Plane Complexity Segmentation) Algoritması ; BPCS, görüntü veya ses gibi dijital verilerin bit düzlemlerini (bit planes) analiz ederek karmaşık bölgelerine veri gizleyen bir steganografi yöntemidir. Her pikselin veya örneğin bit düzlemleri, karmaşıklıklarına göre seçilir.
Görüntü veya ses verisi, bit düzlemlerine ayrılır (örneğin, bir 8-bit piksel 8 bit düzlemine bölünür: en anlamlı bitten en az anlamlı bite).
Her bit düzleminin karmaşıklığı (örneğin, rastgelelik veya desen yoğunluğu) hesaplanır.
Yüksek karmaşıklığa sahip bit düzlemleri (rastgele görünenler), mesaj bitlerini gizlemek için kullanılır, çünkü bu bölgelerdeki değişiklikler daha az fark edilir.
Mesaj, seçilen bit düzlemlerine gömülür ve çıkarılırken aynı düzlemlerden okunur.

4. Maskeleme ve Filtreleme Yöntemleri ; Maskeleme ve filtreleme, insan algısını kullanarak veriyi dijital ortamda gizler. Görüntülerde, belirli desenler veya renk tonları mesajı gizlemek için maske olarak kullanılır; ses dosyalarında ise frekans filtreleri uygulanabilir.
Görüntülerde: Mesaj, görüntünün belirli bölgelerine (örneğin, yüksek kontrastlı kenarlara) gömülür. Örneğin, bir pikselin renk değerleri, mesaj bitlerine bağlı olarak hafifçe değiştirilir, ancak bu değişiklikler insan gözü tarafından fark edilmez.
Seslerde: Mesaj, belirli frekans bantlarına (örneğin, insan kulağının hassas olmadığı yüksek frekanslar) gömülür. Filtreleme teknikleri, mesajın ses kalitesine etkisini en aza indirir.
Maskeleme, genellikle insan algısının sınırlamalarından faydalanır (örneğin, parlak bir bölgede küçük renk değişiklikleri fark edilmez).

5. Sezgisel Steganaliz Yöntemleri ; Sezgisel steganaliz, gizlenmiş veriyi tespit etmek için istatistiksel veya makine öğrenimi tabanlı yöntemler kullanır. Steganografi bağlamında, bu yöntemler mesaj gizlemek yerine, gizlenmiş mesajların varlığını analiz eden yaklaşımları ifade eder. Ancak, ödev bağlamında, bu yöntemler mesaj gizlemek için uyarlanabilir (örneğin, sezgisel analizle hangi bölgelerin gizleme için uygun olduğunu belirlemek).
rinin (görüntü, ses veya video) istatistiksel özellikleri analiz edilir (örneğin, piksel korelasyonu, frekans dağılımı).
Mesaj, istatistiksel olarak "normal" görünen bölgelere gömülür, böylece steganalizle tespit edilmesi zorlaşır.
Makine öğrenimi modelleri (örneğin, SVM veya derin öğrenme), gizleme için en uygun bölgeleri seçebilir.
Çıkarma işlemi, gizleme sırasında kullanılan aynı sezgisel kurallara dayanır.
