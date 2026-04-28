# 🤖 AI Daily Project Generator

Har kuni avtomatik ravishda yangi Python project yaratib GitHub'ga push qiluvchi AI agent.

## ⚙️ O'rnatish

### 1. Secrets qo'shish
GitHub repo → Settings → Secrets → Actions → New repository secret:

| Secret nomi | Qiymati |
|-------------|---------|
| `ANTHROPIC_API_KEY` | `sk-ant-...` kalitingiz |
| `GITHUB_USERNAME` | GitHub username |

> `GITHUB_TOKEN` avtomatik GitHub Actions tomonidan beriladi ✅

### 2. Actions ruxsati
Settings → Actions → General → Workflow permissions → **Read and write permissions** ✅

### 3. Qo'lda sinab ko'rish
Actions → "Daily AI Project Generator" → Run workflow

## 📅 Jadval
Har kuni soat **14:00 Toshkent vaqtida** (09:00 UTC) avtomatik ishlaydi.

## 🛠 Texnologiyalar
- Python 3.11
- GitHub Actions
- Claude AI (Anthropic)
- GitHub API
