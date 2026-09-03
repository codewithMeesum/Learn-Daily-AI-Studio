# ⚡ LEARN DAILY AI — CONTENT STUDIO

> **Internal Content Generation & Publishing Engine for [@learningdailyai](https://instagram.com/learningdailyai)**

Turn raw tech screenshots, video frames, and messy transcripts into production-ready, highly accurate Instagram packages in seconds.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://learn-daily-ai-studio.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Google GenAI SDK](https://img.shields.io/badge/Gemini-3.6%20Flash-orange.svg)](https://aistudio.google.com/)
[![Code Style: Clean](https://img.shields.io/badge/design-minimal%20dark-8A2BE2.svg)](#)

---

### 🚀 Live Application

Access the live cloud workspace directly:

👉 **[https://learn-daily-ai-studio.streamlit.app/](https://learn-daily-ai-studio.streamlit.app/)**

---

## 🎯 What It Does

Most AI content tools output generic, hallucinated fluff loaded with buzzwords. **Content Studio** enforces strict editorial rules for high-authority tech media:

* **Accuracy Over Virality**: Forbids unsupported superlatives ("first ever", "revolutionary", "fastest") unless verified.
* **10 Native Lowercase Hooks**: Generates curiosity-driven reel hooks formatted specifically for the Learn Daily AI brand style.
* **Turnkey Content Package**: Automatically drafts the caption, comment triggers, story poll, SEO keywords, and topic tags.
* **Permanent Brand CTA**: Enforces the brand closing line on every generated post without LLM tampering.
* **One-Click Native Copy**: Instant markdown-compatible clipboard blocks for single-tap mobile or desktop posting.

---

## ⚡ The Publishing Pipeline

```text
       Raw Asset
   [Screenshot / Frame]  +  [Transcript / Context]
            │
            ▼
   ┌───────────────────────────────────────────────┐
   │         Multimodal Analysis Engine            │
   │            (Gemini 3.6 Flash)                 │
   ├───────────────────────────────────────────────┤
   │  1. Extract Visual Subjects & OCR Evidence   │
   │  2. Cross-check Context Against Claims        │
   │  3. Filter Speculation & Enforce Guardrails   │
   └───────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────┐
│             Ready-to-Post Output                 │
├──────────────────────┬───────────────────────────┤
│ 🔥 Best Hook         │ 10 Lowercase Hook Pool    │
│ 📝 Formatted Caption │ 📊 Interactive Poll       │
│ 💬 Engagement Debate │ 🏷️ SEO Discovery & Tags   │
│ #️⃣ Curated Hashtags │ 📋 Complete Bundle Export │
└──────────────────────┴───────────────────────────┘
