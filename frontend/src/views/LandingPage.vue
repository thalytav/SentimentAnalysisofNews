<script setup lang="ts">
import { ref } from 'vue'
import { onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const uploadedFile = ref<File|null>(null)
const uploadedUrl = ref<string>('')
const fileInput = ref<HTMLInputElement|null>(null)
const isDragging = ref(false)

onMounted(() => {
  document.body.addEventListener('dragover', preventDefault)
  document.body.addEventListener('drop', handleDrop)
  document.body.addEventListener('paste', handlePaste)
})

onUnmounted(() => {
  document.body.removeEventListener('dragover', preventDefault)
  document.body.removeEventListener('drop', handleDrop)
  document.body.removeEventListener('paste', handlePaste)
})

const uploadDocument = () => {
  fileInput.value?.click()
}

const handleFileChange = (e: Event) => {
  const files = (e.target as HTMLInputElement).files
  if (files && files[0]) {
    uploadedFile.value = files[0]
    alert(`File uploaded: ${files[0].name}`)
    router.push('/analyze') // Redirect setelah upload
  }
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  if (e.dataTransfer?.files && e.dataTransfer.files[0]) {
    uploadedFile.value = e.dataTransfer.files[0]
    alert(`File uploaded: ${e.dataTransfer.files[0].name}`)
    router.push('/analyze') // Redirect setelah upload
  }
}

const handlePaste = (e: ClipboardEvent) => {
  // Paste file
  if (e.clipboardData?.files && e.clipboardData.files.length > 0) {
    uploadedFile.value = e.clipboardData.files[0]
    alert(`File uploaded: ${e.clipboardData.files[0].name}`)
    router.push('/analyze') // Redirect setelah upload
    return
  }
  // Paste URL
  const text = e.clipboardData?.getData('text')
  if (text && (text.startsWith('http://') || text.startsWith('https://'))) {
    uploadedUrl.value = text
    alert(`URL pasted: ${text}`)
    router.push('/analyze') // Redirect setelah upload
  }
}

const preventDefault = (e: Event) => e.preventDefault()

const goHome = () => {
    window.location.href = '/'
}
</script>

<template>
  <div class="landing-page">
    <!-- Dropzone Overlay -->
    <div v-if="isDragging" class="dropzone-overlay">
      <div class="dropzone-message">
        <svg width="64" height="64" fill="none" viewBox="0 0 24 24">
          <path d="M6 20L18 20" stroke="#6540ef" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M12 16V4M12 4L15.5 7.5M12 4L8.5 7.5" stroke="#6540ef" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <div>Drop file anywhere</div>
      </div>
    </div>

    <!-- Background blur elements -->
    <div class="bg-blur blur-1"></div>
    <div class="bg-blur blur-2"></div>
    <div class="bg-blur blur-3"></div>
    <div class="bg-blur blur-4"></div>

    <div class="content">
      <!-- Header -->
      <header class="header">
        <div class="container">
          <div class="header-left">
            <img src="/img/ReadaSense-logo.png" alt="ReadaSense Logo" class="logo-img"/>

            <nav class="nav">
              <button class="nav-btn" @click="goHome">Home</button>
              <button class="nav-btn">Tentang Kami</button>
            </nav>
          </div>
        </div>
      </header>

      <!-- Hero Section -->
      <section class="hero">
        <div class="container">
          <div class="hero-content">
            <div class="hero-text">
              <h1 class="hero-title">Kenali nada dan makna di balik berita.</h1>
              <p class="hero-subtitle">ReadaSense membantu memahami sentimen serta tingkat keterbacaan secara instan.</p>
              <button class="upload-btn" @click="uploadDocument">
                <svg class="upload-icon" viewBox="0 0 24 24" fill="none">
                  <path d="M6 20L18 20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M12 16V4M12 4L15.5 7.5M12 4L8.5 7.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Upload Document
              </button>
              <input
                type="file"
                ref="fileInput"
                style="display:none"
                accept=".pdf,.docx"
                @change="handleFileChange"
              />
            </div>
            <div class="hero-visual">
              <img src="/img/landing-page-img.png" alt="ReadaSense Landing Page Illustration" class="hero-main-img" />
            </div>
          </div>
        </div>
      </section>

      <!-- Features Section -->
      <section class="features">
        <div class="container features-container">
          <h2 class="section-title">Fitur dari ReadaSense</h2>

          <div class="features-grid">
            <div class="features-col illustration-col">
              <img src="/img/ss-analysis.png" alt="Contoh hasil analisis" class="illustration-img" />
            </div>

            <div class="features-col content-col">
              <div class="features-list">
                <div class="feature-item">
                  <img src="/img/feature-sentimen.png" alt="Deteksi Sentimen" class="feature-img" />
                  <p class="feature-description">
                    Deteksi nada emosional dalam teks berita—apakah positif, netral, atau negatif—dengan visualisasi yang mudah dipahami.
                  </p>
                </div>
                <div class="feature-divider"></div>
                <div class="feature-item">
                  <img src="/img/feature-readability.png" alt="Nilai Keterbacaan" class="feature-img" />
                  <p class="feature-description">
                    Ukur tingkat keterbacaan artikel dengan metrik standar, lengkap dengan kategori (mudah, sedang, sulit) agar pembaca tahu seberapa kompleks teksnya.
                  </p>
                </div>
                <div class="feature-divider"></div>
                <div class="feature-item">
                  <img src="/img/feature-statistic.png" alt="Statistik Teks" class="feature-img" />
                  <p class="feature-description">
                    Ukur tingkat keterbacaan artikel dengan metrik standar, lengkap dengan kategori (mudah, sedang, sulit) agar pembaca tahu seberapa kompleks teksnya.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- How To Section -->
      <section class="how-to">
        <div class="container">
          <h2 class="section-title">Bagaimana cara menggunakan ReadaSense?</h2>
          <div class="steps">
            <div class="step">
              <img src="/img/1.png" alt="Step 1" class="step-number-img" />
              <div class="step-card">
                <img src="/img/illus-step-1.png" alt="Upload Document Illustration" class="step-illustration" />
                <div class="step-content">
                  <h3 class="step-title">Upload Teks Berita</h3>
                  <p class="step-description">
                    Upload atau drop teks berita yang ingin dianalisis dalam bentuk .docx atau .pdf ke ReadaSense. Hanya 1 dokumen yang dapat diupload dalam satu waktu.
                  </p>
                </div>
              </div>
            </div>

            <div class="step">
              <img src="/img/2.png" alt="Step 2" class="step-number-img" />
              <div class="step-card">
                <img src="/img/illus-step-2.png" alt="AI Analysis Illustration" class="step-illustration" />
                <div class="step-content">
                  <h3 class="step-title">AI Menganalisis Teks</h3>
                  <p class="step-description">
                    AI ReadaSense akan membaca teks secara menyeluruh, mendeteksi nada emosional (positif, netral, atau negatif), menghitung tingkat keterbacaan, serta menyiapkan statistik kata yang mendetail.
                  </p>
                </div>
              </div>
            </div>

            <div class="step">
              <img src="/img/3.png" alt="Step 3" class="step-number-img" />
              <div class="step-card">
                <img src="/img/illus-step-3.png" alt="Results Analysis Illustration" class="step-illustration" />
                <div class="step-content">
                  <h3 class="step-title">Lihat Hasil Analisis</h3>
                  <p class="step-description">
                    Nikmati hasil analisis: label sentimen, skor keterbacaan, statistik kata, serta visualisasi data. Semua ditampilkan dalam dashboard yang interaktif.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section class="cta">
        <div class="container">
          <img src="/img/CTA-Text.png" alt="Dapatkan insight yang lebih cepat, akurat, dan mendalam dari setiap artikel. Uji ReadaSense sekarang." class="cta-text-img" />
          <button class="try-btn" @click="uploadDocument">Coba Sekarang!</button>
        </div>
      </section>

      <!-- Footer -->
      <footer class="footer">
        <div class="container">
          <div class="footer-content">
            <div class="footer-brand">
              <img src="\img\ReadaSense-logo-white.png" alt="ReadaSense Logo" class="footer-logo" />
              <p class="footer-copyright">
                Copyright © 2025 ReadaSense.<br>
                All Rights Reserved.
              </p>
              <div class="social-media">
                <span class="social-label">Social Media</span>
                <div class="social-icons">
                  <a class="facebook-icon" target="_blank" rel="nofollow" href="https://www.facebook.com/"></a>
                  <a class="X-icon" target="_blank" rel="nofollow" href="https://www.twitter.com/"></a>
                  <a class="instagram-icon" target="_blank" rel="nofollow" href="https://www.instagram.com/"></a>
                  <a class="linkedin-icon" target="_blank" rel="nofollow" href="https://www.linkedin.com/"></a>
                </div>
              </div>
            </div>

            <div class="footer-section">
              <h3 class="footer-title">Tentang</h3>
              <ul class="footer-links">
                <li>Perusahaan Kami</li>
                <li>Produk Kami</li>
                <li>Tim Professional</li>
              </ul>
            </div>

            <div class="footer-section">
              <h3 class="footer-title">Alamat</h3>
              <div class="footer-contact-address content-col">
                <div class="contact-address-list">
                  <div class="contact-address-item">
                    <img src="/icons/location.svg" alt="Location Icon" class="contact-icon" />
                    <p class="address">
                    Kampus Institut Teknologi Sepuluh Nopember, Keputih, Sukolilo, Surabaya, East Java 60117
                  </p>
                  </div>
                  <div class="contact-address-item">
                    <img src="/icons/telephone.svg" alt="Telephone Icon" class="contact-icon" />
                    <p class="contact-item">+62 812 3456 7890</p>
                  </div>
                  <div class="contact-address-item">
                    <img src="/icons/email.svg" alt="Email Icon" class="contact-icon" />
                    <p class="contact-item">kelompok2@its.ac.id</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<style scoped>
/* CSS Variables */
* {
  box-sizing: border-box;
}

.landing-page {
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: var(--neutral-black);
  background: var(--neutral-white);
  line-height: 1.5;
}

.container {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 48px;
}

.content {
  z-index: 1;
}

/* Dropzone Overlay */
.dropzone-overlay {
  position: fixed;
  inset: 0;
  background: rgba(101, 64, 239, 0.12);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  transition: background 0.2s;
}

.dropzone-message {
  border: 2px dashed var(--neutral-white);
  border-radius: 16px;
  padding: 48px 64px;
  box-shadow: 0 8px 32px rgba(101,64,239,0.08);
  text-align: center;
  font-size: 1.5rem;
  color: var(--neutral-white);
  pointer-events: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

/* Header */
.header {
  background: var(--neutral-white);
  padding: 24px 0;
  position: relative;
  z-index: 10;
  position: sticky;
  top: 0;
}

.header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.logo-img {
  width: 194px;
  height: 36px;
  object-fit: contain;
}

.footer-logo {
  width: 194px;
  height: 36px;
  object-fit: contain;
  margin-bottom: 24px;
}

.nav {
  display: flex;
  gap: 0;
}

.nav-btn {
  background: none;
  border: none;
  padding: 12px 16px;
  border-radius: var(--border-radius);
  font-family: inherit;
  font-size: 14px;
  font-weight: 700;
  color: var(--primary-purple);
  cursor: pointer;
  transition: background-color 0.2s;
}

.nav-btn:hover {
  background: rgba(101, 64, 239, 0.1);
}

/* Hero Section */
.hero {
  position: relative;
  padding: 100px 0 120px;
  overflow: hidden;
  min-height: 80vh;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 86px;
  align-items: center;
  position: relative;
  z-index: 2;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  line-height: 1.2;
  color: var(--primary-purple);
  margin: 0 0 16px;
}

.hero-subtitle {
  font-size: 18px;
  font-weight: 600;
  line-height: 1.56;
  color: var(--neutral-black);
  margin: 0 0 24px;
}

.upload-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 24px;
  background: var(--primary-purple);
  color: var(--neutral-white);
  border: none;
  border-radius: var(--border-radius);
  font-family: inherit;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.2s;
}

.upload-btn:hover {
  background: var(--dark-purple);
}

.upload-icon {
  width: 24px;
  height: 24px;
}

.hero-visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.hero-main-img {
  width: 100%;
  max-width: 750px;
  height: auto;
  object-fit: contain;
}

/* Background blur elements */
.bg-blur {
  position: absolute;
  filter: blur(200px);
  z-index: 0;
}

.blur-1 {
  width: 536px;
  height: 536px;
  background: radial-gradient(50% 50% at 50% 50%, var(--primary-blue) 0%, rgba(80, 148, 241, 0) 100%);
  opacity: 0.5;
  bottom: -130%;
  right: -10%;
}

.blur-2 {
  width: 651px;
  height: 651px;
  background: radial-gradient(50% 50% at 50% 50%, var(--primary-blue) 0%, rgba(80, 148, 241, 0) 100%);
  bottom: -250%;
  left: -15%;
  filter: blur(250px);
  opacity: 0.5;
}

.blur-3 {
  width: 470px;
  height: 470px;
  background: radial-gradient(50% 50% at 50% 50%, #987FF4 0%, rgba(152, 127, 244, 0) 100%);
  top: 20%;
  left: 20%;
  filter: blur(150px);
}

.blur-4 {
  width: 470px;
  height: 470px;
  background: radial-gradient(50% 50% at 50% 50%, #987FF4 0%, rgba(152, 127, 244, 0) 100%);
  bottom: -300%;
  left: 70%;
  filter: blur(150px);
  opacity: 0.7;
}

/* Features Section */
.features {
  padding: 48px 0;
}

/* Override container padding for this section */
.features .features-container {
  padding: 0 32px;
}

.features-grid {
  display: flex;
  gap: 20px;
}

.features-col {
  display: flex;
  flex-direction: column;
  line-height: normal;
  width: 50%;
}

.illustration-img {
  width: 100%;
  max-width: 561px;
  height: auto;
  object-fit: contain;
  border-radius: 8px;
  border: 2px solid var(--neutral-white);
}

.section-title {
  font-size: 40px;
  font-weight: 700;
  line-height: 1.2;
  color: var(--primary-purple);
  text-align: center;
  margin: 0 0 48px;
}

.features-list {
  max-width: 800px;
  margin: 0 auto;
}

.feature-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 32px;
  margin: 24px 0;
}

.feature-img {
  height: 44px;
  object-fit: contain;
  flex-shrink: 0;
}

.feature-description {
  flex: 1;
  font-size: 16px;
  line-height: 1.5;
  margin: 0;
  color: var(--neutral-black);
}

.feature-divider {
  height: 2px;
  background: var(--primary-blue);
  margin: 16px 0;
}

/* How To Section */
.how-to {
  padding: 80px 0;
}

.steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 46px;
  margin-top: 64px;
}

.step {
  position: relative;
}

.step-number-img {
  position: absolute;
  top: -34px;
  left: 50%;
  transform: translateX(-50%);
  width: 68px;
  height: 68px;
  object-fit: contain;
  z-index: 2;
}

.step-card {
  background: linear-gradient(144deg, rgba(80, 148, 241, 0.3) 4.67%, rgba(245, 245, 247, 0.3) 95.33%);
  backdrop-filter: blur(2px);
  border: 2px solid var(--neutral-white);
  border-radius: 16px;
  padding: 56px 24px 48px;
  text-align: center;
}

.step-illustration {
  width: 300px;
  height: 200px;
  margin: 0 auto 24px;
  border-radius: 8px;
  object-fit: cover;
}

.step-title {
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 8px;
  color: var(--neutral-black);
}

.step-description {
  font-size: 16px;
  line-height: 1.5;
  margin: 0;
  color: var(--neutral-black);
  text-align: justify;
}


/* CTA Section */
.cta {
  padding: 80px 0;
  text-align: center;
  position: relative;
}

.cta-text-img {
  width: 100%;
  max-width: 1019px;
  height: auto;
  margin: 0 auto 32px;
  object-fit: contain;
}

.try-btn {
  background: var(--primary-purple);
  color: var(--neutral-white);
  border: none;
  padding: 16px 24px;
  border-radius: var(--border-radius);
  font-family: inherit;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.2s;
}

.try-btn:hover {
  background: var(--dark-purple);
}

/* Footer */
.footer {
  background: var(--dark-purple);
  color: var(--neutral-white);
  padding: 67px 0;
}

.footer-content {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 80px;
}


.footer-copyright {
  font-size: 14px;
  line-height: 1.7;
  color: var(--grey-500);
  margin: 0 0 32px;
}

.social-label {
  display: block;
  font-size: 16px;
  color: var(--grey-500);
  margin-bottom: 8px;
}

.social-icons {
  display: flex;
  gap: 20px;
}

.facebook-icon {
  width: 20px;
  height: 20px;
  background-image: url('/icons/facebook.svg');
  background-repeat: no-repeat;
  background-position: center;
  border-radius: 3px;
}

.facebook-icon:hover {
  background-image: url('/icons/facebook-hover.svg');
}

.X-icon {
  width: 20px;
  height: 20px;
  background-image: url('/icons/X.svg');
  background-repeat: no-repeat;
  background-position: center;
  border-radius: 3px;
}

.X-icon:hover {
  background-image: url('/icons/X-hover.svg');
}

.instagram-icon {
  width: 20px;
  height: 20px;
  background-image: url('/icons/instagram.svg');
  background-repeat: no-repeat;
  background-position: center;
  border-radius: 3px;
}

.instagram-icon:hover {
  background-image: url('/icons/instagram-hover.svg');
}

.linkedin-icon {
  width: 20px;
  height: 20px;
  background-image: url('/icons/linkedin.svg');
  background-repeat: no-repeat;
  background-position: center;
  border-radius: 3px;
}

.linkedin-icon:hover {
  background-image: url('/icons/linkedin-hover.svg');
}

.footer-title {
  font-size: 32px;
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 24px;
  color: var(--neutral-white);
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  font-size: 16px;
  line-height: 1.5;
  color: #A8ACB7;
  margin-bottom: 8px;
  cursor: pointer;
}

.footer-links li:hover {
  color: var(--neutral-white);
}

.footer-contact {
  font-size: 16px;
  line-height: 1.9;
  color: #A8ACB7;
}

.contact-address-item {
  display: flex;
  gap: 16px;
}

.address {
  margin-bottom: 16px;
}

.contact-item {
  margin: 0 0 8px;
  cursor: pointer;
}

.contact-item:hover {
  color: var(--neutral-white);
}

/* Responsive Design */
@media (max-width: 1200px) {
  .container {
    padding: 0 32px;
  }
  
  .hero-content {
    gap: 60px;
  }
  
  .document-img {
    width: 350px;
  }
}

@media (max-width: 992px) {
  .hero-content {
    grid-template-columns: 1fr;
    gap: 40px;
    text-align: center;
  }

  .hero-visual {
    order: -1;
  }

  .features-grid {
    flex-direction: column;
    align-items: stretch;
    gap: 0;
  }

  .features-col {
    width: 100%;
  }

  .content-col {
    margin-left: 0;
  }

  .steps {
    grid-template-columns: 1fr;
    gap: 60px;
  }

  .step-number-img {
    width: 68px;
    height: 68px;
  }

  .social-icons {
    justify-content: center;
    align-items: center;
  }

  .footer-content {
    grid-template-columns: 1fr;
    gap: 40px;
    text-align: center;
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 24px;
  }

  .logo-img {
    width: 150px;
    height: 28px;
  }
  
  .hero-title {
    font-size: 36px;
  }
  
  .section-title {
    font-size: 32px;
  }
  
  .cta-title {
    font-size: 32px;
  }
  
  .feature-item {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .hero-main-img {
    max-width: 400px;
  }
}

@media (max-width: 480px) {
    .header .container {
    flex-direction: column;
    gap: 20px;
  }

  .header-left {
    flex-direction: column;
    gap: 16px;
  }
  
  .hero-title {
    font-size: 28px;
  }
  
  .section-title {
    font-size: 24px;
  }
  
  .cta-title {
    font-size: 24px;
  }
  
  .upload-btn,
  .try-btn {
    width: 100%;
    justify-content: center;
  }
  
  .step-card {
    padding: 40px 16px 32px;
  }
  
  .step-illustration {
    width: 250px;
    height: 150px;
  }

  .footer-logo {
    width: 150px;
    height: 28px;
  }
}
</style>
