import os
import random
import requests
import base64
from datetime import datetime

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
GITHUB_TOKEN = os.environ["MY_GH_TOKEN"]
GITHUB_USERNAME = "Islom-Radjapov"

HEADERS_GITHUB = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

HEADERS_CLAUDE = {
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

PROJECT_THEMES = [
    "calculator", "todo list", "quiz game", "password generator",
    "text analyzer", "number guessing game", "BMI calculator",
    "palindrome checker", "fibonacci generator", "prime number finder",
    "word counter", "temperature converter", "simple chatbot",
    "rock paper scissors", "tip calculator", "age calculator",
    "random quote generator", "dice roller", "unit converter",
    "grade calculator", "morse code converter", "binary converter",
    "simple ATM simulator", "library book tracker", "contact book"
]

def ask_claude(system_prompt, user_prompt):
    """Claude AI dan javob olish"""
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=HEADERS_CLAUDE,
        json={
            "model": "claude-haiku-4-5",
            "max_tokens": 3000,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}]
        }
    )
    data = response.json()
    if "content" not in data:
        raise Exception(f"Claude API xatosi: {data}")
    return data["content"][0]["text"].strip()

def generate_code(theme):
    """Python kodni alohida so'rash"""
    system = "You are a Python developer. Write clean, well-commented Python code. Return ONLY the Python code, no explanations, no markdown fences."
    prompt = f"""Write a complete, working Python script for a '{theme}' application.
Requirements:
- Beginner-friendly with comments
- Interactive (uses input/output)
- Has error handling with try/except
- At least 50 lines of code
- Works standalone with no external libraries"""
    return ask_claude(system, prompt)

def generate_readme(theme, repo_name):
    """README ni alohida so'rash"""
    system = "You are a technical writer. Write clear README files in Markdown. Return ONLY the markdown content, no extra text."
    prompt = f"""Write a README.md for a Python '{theme}' project named '{repo_name}'.
Include: project title, description, how to run it, features list, and author section.
Keep it concise and practical."""
    return ask_claude(system, prompt)

def create_github_repo(repo_name, description):
    """GitHub'da yangi repo yaratish"""
    response = requests.post(
        "https://api.github.com/user/repos",
        headers=HEADERS_GITHUB,
        json={
            "name": repo_name,
            "description": description,
            "public": True,
            "auto_init": False
        }
    )
    data = response.json()
    if "full_name" in data:
        print(f"✅ Repo yaratildi: {data['html_url']}")
        return data
    else:
        raise Exception(f"Repo yaratishda xato: {data}")

def push_file(repo_name, file_path, content, commit_message):
    """Faylni GitHub'ga yuklash"""
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    response = requests.put(
        f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/contents/{file_path}",
        headers=HEADERS_GITHUB,
        json={
            "message": commit_message,
            "content": encoded
        }
    )
    return response.json()

def main():
    print("🚀 AI Daily Project Agent ishga tushdi!")
    print("=" * 50)

    today = datetime.now().strftime("%Y-%m-%d")
    theme = random.choice(PROJECT_THEMES)
    repo_name = f"daily-{theme.replace(' ', '-')}-{today}"
    description = f"A simple {theme} built with Python - Daily AI Project"

    print(f"🤖 Bugun: {today} | Mavzu: {theme}")
    print(f"📁 Repo nomi: {repo_name}")

    # 1. Kod yaratish
    print("⏳ Python kodi yozilmoqda...")
    code = generate_code(theme)
    print("✅ Kod tayyor!")

    # 2. README yaratish
    print("⏳ README yozilmoqda...")
    readme = generate_readme(theme, repo_name)
    print("✅ README tayyor!")

    # 3. GitHub repo yaratish
    create_github_repo(repo_name, description)

    # 4. Fayllarni yuklash
    push_file(repo_name, "main.py", code, "🤖 AI generated Python project")
    print("✅ main.py yuklandi")

    push_file(repo_name, "README.md", readme, "📝 Add README")
    print("✅ README.md yuklandi")

    gitignore = "__pycache__/\n*.py[cod]\n.env\nvenv/\n.vscode/\n"
    push_file(repo_name, ".gitignore", gitignore, "🔧 Add .gitignore")
    print("✅ .gitignore yuklandi")

    print("=" * 50)
    print(f"🎉 Tayyor! https://github.com/{GITHUB_USERNAME}/{repo_name}")

if __name__ == "__main__":
    main()
