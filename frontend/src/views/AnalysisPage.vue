<script setup lang="ts">
import { ref } from 'vue'

const activeTab = ref('sentiment')
const entitiesExpanded = ref(true)
const themesExpanded = ref(true)
const keywordsExpanded = ref(false)

// Sample data
const sentimentData = {
    positive: 50.0,
    negative: 25.0,
    neutral: 25.0,
    overallScore: 0.50,
    overallSentiment: 'positif'
}

const entities = [
    { name: 'ITS', magnitude: '2.0', score: '+0.78', sentiment: 'positive' },
    { name: 'Surabaya', magnitude: '3.0', score: '+0.63', sentiment: 'positive' },
    { name: 'Gedung DPR', magnitude: '5.4', score: '-0.88', sentiment: 'negative' },
    { name: 'Rektorat', magnitude: '1.8', score: '+0.25', sentiment: 'neutral' },
    { name: 'BEM-ITS', magnitude: '1.5', score: '+0.20', sentiment: 'neutral' }
]

const goHome = () => {
    window.location.href = '/'
}

const switchTab = (tab: string) => {
    activeTab.value = tab
}

const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
        case 'positive': return '#8DDAB8'
        case 'negative': return '#FA928A'
        case 'neutral': return '#FFEB89'
        default: return '#C9DEFB'
    }
}
</script>

<template>
    <div class="analysis-page">
        <!-- Background blur elements -->
        <div class="bg-blur blur-left"></div>
        <div class="bg-blur blur-right"></div>

        <!-- Header -->
        <header class="header">
            <div class="container">
            <div class="header-left">
                <img src="/img/ReadaSense-logo.png" alt="ReadaSense Logo" class="logo-img" @click="goHome"/>

                <nav class="nav">
                <button class="nav-btn" @click="goHome">Home</button>
                <button class="nav-btn">Tentang Kami</button>
                </nav>
            </div>
            </div>
        </header>

        <!-- Analysis Dashboard -->
        <section class="analysis-dashboard">
        <div class="container">
            <div class="dashboard-header">
            <h1 class="page-title">Hasil Analisis</h1>
            <div class="tabs">
                <button 
                class="tab-btn" 
                :class="{ active: activeTab === 'readability' }"
                @click="switchTab('readability')"
                >
                <svg class="tab-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M2 14C2 16.2091 3.79086 18 6 18C8.20914 18 10 16.2091 10 14C10 11.7909 8.20914 10 6 10C3.79086 10 2 11.7909 2 14ZM2 14V6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M22 14C22 16.2091 20.2091 18 18 18C15.7909 18 14 16.2091 14 14C14 11.7909 15.7909 10 18 10C20.2091 10 22 11.7909 22 14ZM22 14V6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M14 14H10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Readability</span>
                </button>
                <button 
                class="tab-btn" 
                :class="{ active: activeTab === 'sentiment' }"
                @click="switchTab('sentiment')"
                >
                <svg class="tab-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M2 12C2 17.5228 6.47715 22 12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M11.5 15.5C11.5 15.5 13 13.5 16 13.5C19 13.5 20.5 15.5 20.5 15.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M3 4C3 1.24586 7 1.2458 7 3.99993C7 5.96716 5 5.63927 5 7.99994" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M5 11.01L5.01 10.9989" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M17.5 9C17.2239 9 17 8.77614 17 8.5C17 8.22386 17.2239 8 17.5 8C17.7761 8 18 8.22386 18 8.5C18 8.77614 17.7761 9 17.5 9Z" fill="currentColor" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M10.5 9C10.2239 9 10 8.77614 10 8.5C10 8.22386 10.2239 8 10.5 8C10.7761 8 11 8.22386 11 8.5C11 8.77614 10.7761 9 10.5 9Z" fill="currentColor" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Sentiment</span>
                </button>
            </div>
            </div>

            <div class="dashboard-content">
            <!-- Left Sidebar - Sentiment Score Card -->
            <div class="sentiment-card">
                <div class="card-header">
                <h2 class="card-title">Skor Sentimen</h2>
                <button class="help-btn">?</button>
                </div>
                <p class="card-subtitle">Persentase</p>

                <!-- Sentiment Meter -->
                <div class="sentiment-meter-container">
                <svg class="sentiment-meter" viewBox="0 0 264 264" fill="none">
                    <!-- Yellow arc (Neutral) -->
                    <path d="M252 132C252 198.274 198.274 252 132 252" 
                    stroke="#FFE14F" 
                    stroke-width="24" 
                    stroke-linecap="round"
                    class="meter-arc neutral-arc"/>
                    
                    <!-- Red section (Negative) -->
                    <path d="M132 264C138.627 264 144 258.628 144 252C144 245.373 138.627 240 132 240L132 252L132 264ZM132 252L132 240C72.3532 240 24 191.647 24 132L12 132L-4.36897e-06 132C-1.1354e-06 204.902 59.0984 264 132 264L132 252Z" 
                    fill="#F75D51"
                    class="meter-arc negative-arc"/>
                    
                    <!-- Green arc (Positive) -->
                    <path d="M252 132C252 65.7258 198.274 12 132 12C65.7258 12 12 65.7258 12 132" 
                    stroke="#55C895" 
                    stroke-width="24" 
                    stroke-linecap="round"
                    class="meter-arc positive-arc"/>
                    
                    <!-- Center circle (smiley face) -->
                    <circle cx="132" cy="131.6" r="69.6" fill="#55C895"/>
                    <circle cx="103.725" cy="118.55" r="13.05" fill="#F5F5F7"/>
                    <circle cx="158.1" cy="118.55" r="13.05" fill="#F5F5F7"/>
                    <path d="M106.987 154.438C109.174 159.15 117.134 168.575 131.474 168.575C145.815 168.575 153.774 159.15 155.961 154.438" 
                    stroke="#F5F5F7" 
                    stroke-width="7.2" 
                    stroke-linecap="round"/>
                </svg>
                </div>

                <!-- Percentages -->
                <div class="percentages">
                <div class="percentage-item">
                    <h3 class="percentage-label positive-label">Positif</h3>
                    <p class="percentage-value positive-value">{{ sentimentData.positive }}%</p>
                </div>
                <div class="percentage-row">
                    <div class="percentage-item">
                    <h3 class="percentage-label negative-label">Negatif</h3>
                    <p class="percentage-value negative-value">{{ sentimentData.negative }}%</p>
                    </div>
                    <div class="percentage-item">
                    <h3 class="percentage-label neutral-label">Netral</h3>
                    <p class="percentage-value neutral-value">{{ sentimentData.neutral }}%</p>
                    </div>
                </div>
                </div>

                <!-- Overall Rating -->
                <div class="overall-rating">
                <h3 class="rating-title">Rating Keseluruhan</h3>
                <p class="rating-text">
                    Teks ini secara keseluruhan memiliki sentimen yang 
                    <span class="positive-text">positif (+{{ sentimentData.overallScore }})</span>
                </p>
                </div>
            </div>

            <!-- Right Content Area -->
            <div class="content-area">
                <!-- Score Cards -->
                <div class="score-cards">
                <div class="score-card positive-card">
                    <div class="score-indicator"></div>
                    <div class="score-content">
                    <div class="score-header">
                        <h3 class="score-title positive-title">Positif</h3>
                        <button class="help-btn">?</button>
                    </div>
                    <div class="score-values">
                        <span class="score-value positive-dark">0.50</span>
                        <span class="score-max">dari 1.0</span>
                    </div>
                    </div>
                </div>

                <div class="score-card negative-card">
                    <div class="score-indicator"></div>
                    <div class="score-content">
                    <div class="score-header">
                        <h3 class="score-title negative-title">Negatif</h3>
                        <button class="help-btn">?</button>
                    </div>
                    <div class="score-values">
                        <span class="score-value negative-dark">0.25</span>
                        <span class="score-max">dari 1.0</span>
                    </div>
                    </div>
                </div>

                <div class="score-card neutral-card">
                    <div class="score-indicator"></div>
                    <div class="score-content">
                    <div class="score-header">
                        <h3 class="score-title neutral-title">Netral</h3>
                        <button class="help-btn">?</button>
                    </div>
                    <div class="score-values">
                        <span class="score-value neutral-dark">0.25</span>
                        <span class="score-max">dari 1.0</span>
                    </div>
                    </div>
                </div>
                </div>

                <!-- Analysis Details -->
                <div class="analysis-details">
                <!-- Entities Table -->
                <div class="detail-section">
                    <div class="section-header" @click="entitiesExpanded = !entitiesExpanded">
                    <h3 class="section-title">Entitas Terdeteksi</h3>
                    <button class="expand-btn">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </button>
                    </div>
                    <div v-show="entitiesExpanded" class="table-container">
                    <table class="data-table">
                        <thead>
                        <tr>
                            <th>Entitas Terdeteksi</th>
                            <th>Magnitudo</th>
                            <th>Skor Sentimen</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr v-for="(entity, index) in entities" :key="index" :class="{ 'row-alt': index % 2 === 0 }">
                            <td>{{ entity.name }}</td>
                            <td>{{ entity.magnitude }}</td>
                            <td :style="{ backgroundColor: getSentimentColor(entity.sentiment) }">{{ entity.score }}</td>
                        </tr>
                        </tbody>
                    </table>
                    </div>
                </div>

                <div class="section-divider"></div>

                <!-- Themes Table -->
                <div class="detail-section">
                    <div class="section-header" @click="themesExpanded = !themesExpanded">
                    <h3 class="section-title">Tema Terdeteksi</h3>
                    <button class="expand-btn">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </button>
                    </div>
                    <div v-show="themesExpanded" class="table-container">
                    <table class="data-table">
                        <thead>
                        <tr>
                            <th>Entitas Terdeteksi</th>
                            <th>Magnitudo</th>
                            <th>Skor Sentimen</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr v-for="(entity, index) in entities" :key="index" :class="{ 'row-alt': index % 2 === 0 }">
                            <td>{{ entity.name }}</td>
                            <td>{{ entity.magnitude }}</td>
                            <td :style="{ backgroundColor: getSentimentColor(entity.sentiment) }">{{ entity.score }}</td>
                        </tr>
                        </tbody>
                    </table>
                    </div>
                </div>
                </div>
            </div>
            </div>
        </div>
        </section>

        <!-- Footer -->
        <footer class="footer">
            <div class="container">
            <div class="footer-content">
                <div class="footer-brand">
                <img src="/img/ReadaSense-logo-white.png" alt="ReadaSense Logo" class="footer-logo" />
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
</template>

<style scoped>
    /* CSS Variables */
    :root {
    --primary-purple: #6540EF;
    --primary-blue: #5094F1;
    --light-blue: #8AB7F6;
    --dark-purple: #2A1B64;
    --neutral-white: #F5F5F7;
    --neutral-black: #1D1D1F;
    --grey-500: #AEAEBC;
    --green-500: #55C895;
    --green-300: #8DDAB8;
    --green-900: #24543F;
    --red-500: #F75D51;
    --red-300: #FA928A;
    --red-900: #682722;
    --yellow-500: #FFE14F;
    --yellow-600: #E8CD48;
    --yellow-300: #FFEB89;
    --yellow-900: #6B5F21;
    --blue-100: #C9DEFB;
    --blue-800: #2C5185;
    --border-radius: 12px;
    }

    * {
    box-sizing: border-box;
    }

    .analysis-page {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--neutral-black);
    background: var(--neutral-white);
    line-height: 1.5;
    min-height: 100vh;
    position: relative;
    }

    .container {
    max-width: 1440px;
    margin: 0 auto;
    padding: 0 48px;
    }

    /* Background blur elements */
    .bg-blur {
    position: absolute;
    border-radius: 50%;
    filter: blur(250px);
    z-index: 0;
    pointer-events: none;
    opacity: 0.5;
    }

    .blur-left {
    width: 620px;
    height: 620px;
    background: radial-gradient(50% 50% at 50% 50%, var(--primary-blue) 0%, rgba(80, 148, 241, 0) 100%);
    top: 170px;
    left: -100px;
    }

    .blur-right {
    width: 679px;
    height: 679px;
    background: radial-gradient(50% 50% at 50% 50%, var(--primary-blue) 0%, rgba(80, 148, 241, 0) 100%);
    top: 466px;
    right: -100px;
    }

    /* Header */
    .header {
    background: var(--neutral-white);
    padding: 24px 0;
    position: relative;
    z-index: 10;
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
    cursor: pointer;
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

    /* Analysis Dashboard */
    .analysis-dashboard {
    padding: 24px 0 80px;
    position: relative;
    z-index: 1;
    }

    .dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
    }

    .page-title {
    font-size: 48px;
    font-weight: 700;
    line-height: 1.2;
    color: var(--primary-purple);
    margin: 0;
    }

    .tabs {
    display: flex;
    gap: 16px;
    }

    .tab-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px;
    border: none;
    border-radius: 8px;
    background: transparent;
    color: var(--primary-purple);
    font-family: inherit;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    transition: background-color 0.2s;
    }

    .tab-btn.active {
    background: var(--primary-purple);
    color: var(--neutral-white);
    }

    .tab-btn:hover:not(.active) {
    background: rgba(101, 64, 239, 0.1);
    }

    .tab-icon {
    width: 24px;
    height: 24px;
    }

    /* Dashboard Content */
    .dashboard-content {
    display: grid;
    grid-template-columns: 384px 1fr;
    gap: 32px;
    }

    /* Sentiment Card */
    .sentiment-card {
    padding: 32px 24px;
    border-radius: 16px;
    border: 3px solid var(--neutral-white);
    background: rgba(80, 148, 241, 0);
    backdrop-filter: blur(2px);
    display: flex;
    flex-direction: column;
    gap: 40px;
    }

    .card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    }

    .card-title {
    font-size: 32px;
    font-weight: 700;
    color: var(--primary-purple);
    margin: 0;
    }

    .help-btn {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 1px solid var(--primary-purple);
    background: transparent;
    color: var(--primary-purple);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    }

    .card-subtitle {
    font-size: 18px;
    font-weight: 700;
    color: #987FF4;
    margin: -32px 0 0;
    }

    .sentiment-meter-container {
    display: flex;
    justify-content: center;
    align-items: center;
    }

    .sentiment-meter {
    width: 240px;
    height: 240px;
    }

    .percentages {
    display: flex;
    flex-direction: column;
    gap: 32px;
    align-items: center;
    }

    .percentage-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    width: 100%;
    }

    .percentage-row {
    display: flex;
    gap: 0;
    width: 100%;
    }

    .percentage-row .percentage-item {
    flex: 1;
    }

    .percentage-label {
    font-size: 18px;
    font-weight: 700;
    margin: 0;
    }

    .positive-label { color: var(--green-500); }
    .negative-label { color: var(--red-500); }
    .neutral-label { color: var(--yellow-600); }

    .percentage-value {
    font-size: 16px;
    margin: 0;
    }

    .positive-value { color: var(--green-900); }
    .negative-value { color: var(--red-900); }
    .neutral-value { color: var(--yellow-900); }

    .overall-rating {
    display: flex;
    flex-direction: column;
    gap: 16px;
    }

    .rating-title {
    font-size: 18px;
    font-weight: 700;
    color: #987FF4;
    margin: 0;
    }

    .rating-text {
    font-size: 16px;
    line-height: 1.5;
    text-align: center;
    margin: 0;
    color: var(--neutral-black);
    }

    .positive-text {
    color: var(--green-500);
    font-weight: 600;
    }

    /* Content Area */
    .content-area {
    display: flex;
    flex-direction: column;
    gap: 24px;
    }

    .score-cards {
    display: flex;
    gap: 24px;
    border-left-width: 6px;
    }

    .score-card {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 32px;
    padding: 0;
    border-radius: 0 16px 16px 0;
    border: 3px solid var(--neutral-white);
    background: rgba(245, 245, 247, 0.3);
    min-height: 117px;
    }

    .score-indicator {
    width: 12px;
    align-self: stretch;
    border-radius: 12px 0 0 12px;
    }

    .positive-card .score-indicator { background: var(--green-500); }
    .negative-card .score-indicator { background: var(--red-500); }
    .neutral-card .score-indicator { background: var(--yellow-500); }

    .score-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding-right: 24px;
    }

    .score-header {
    display: flex;
    align-items: center;
    gap: 16px;
    }

    .score-title {
    font-size: 32px;
    font-weight: 700;
    margin: 0;
    }

    .positive-title { color: var(--green-500); }
    .negative-title { color: var(--red-500); }
    .neutral-title { color: var(--yellow-600); }

    .score-values {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    }

    .score-value {
    font-size: 18px;
    font-weight: 700;
    }

    .positive-dark { color: var(--green-900); }
    .negative-dark { color: var(--red-900); }
    .neutral-dark { color: var(--yellow-900); }

    .score-max {
    font-size: 18px;
    font-weight: 700;
    color: var(--grey-500);
    }

    /* Analysis Details */
    .analysis-details {
    padding: 32px;
    border-radius: 16px;
    border: 3px solid var(--neutral-white);
    background: rgba(245, 245, 247, 0.3);
    display: flex;
    flex-direction: column;
    }

    .detail-section {
    display: flex;
    flex-direction: column;
    }

    .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0;
    cursor: pointer;
    }

    .section-title {
    font-size: 24px;
    font-weight: 700;
    color: var(--primary-purple);
    margin: 0;
    }

    .expand-btn {
    background: none;
    border: none;
    padding: 12px;
    cursor: pointer;
    color: var(--primary-purple);
    }

    .section-divider {
    height: 2px;
    background: var(--primary-blue);
    margin: 0;
    }

    .table-container {
    padding-bottom: 24px;
    }

    .data-table {
    width: 100%;
    border-collapse: collapse;
    }

    .data-table thead {
    border-bottom: 2px solid transparent;
    }

    .data-table th {
    padding: 8px 0;
    text-align: left;
    font-size: 16px;
    font-weight: 500;
    color: var(--primary-purple);
    }

    .data-table th:first-child {
    width: 60%;
    padding-left: 16px;
    }

    .data-table th:nth-child(2),
    .data-table th:nth-child(3) {
    width: 20%;
    padding-left: 8px;
    }

    .data-table tbody tr {
    background: transparent;
    }

    .data-table tbody tr.row-alt {
    background: var(--blue-100);
    }

    .data-table td {
    padding: 4px 8px;
    font-size: 14px;
    color: var(--neutral-black);
    }

    .data-table td:first-child {
    padding-left: 16px;
    }

    /* Footer */
    .footer {
    background: var(--dark-purple);
    color: var(--neutral-white);
    padding: 67px 0;
    position: relative;
    z-index: 1;
    }

    .footer-content {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 80px;
    }

    .footer-logo {
    width: 194px;
    height: 36px;
    object-fit: contain;
    margin-bottom: 24px;
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

    .social-icon {
    width: 20px;
    height: 20px;
    background: var(--grey-500);
    border-radius: 3px;
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
    .dashboard-content {
        grid-template-columns: 1fr;
    }

    .score-cards {
        flex-direction: column;
    }
    }

    @media (max-width: 992px) {
    .dashboard-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 20px;
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

    .header-left {
        flex-direction: column;
        gap: 16px;
    }

    .page-title {
        font-size: 36px;
    }

    .tabs {
        flex-direction: column;
        width: 100%;
    }

    .tab-btn {
        justify-content: center;
    }
}
</style>
