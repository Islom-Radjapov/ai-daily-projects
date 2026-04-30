import os
import json
import random
import requests
from datetime import datetime

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
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
    "calculator", "todo list", "weather app", "quiz game", "password generator",
    "text analyzer", "number guessing game", "BMI calculator", "currency converter",
    "palindrome checker", "fibonacci generator", "prime number finder",
    "word counter", "email validator", "temperature converter", "simple chatbot",
    "rock paper scissors", "alarm clock", "tip calculator", "age calculator",
    "random quote generator", "dice roller", "countdown timer", "unit converter",
    "simple budget tracker", "grade calculator", "morse code converter"
]

def ask_claude(prompt):
    """Claude AI dan javob olish"""
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=HEADERS_CLAUDE,
        json={
            #"model": "claude-sonnet-4-20250514",
            "model": "claude-haiku-4-5",
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    return response.json()["content"][0]["text"]

def generate_project():
    """Yangi Python project yaratish"""
    today = datetime.now().strftime("%Y-%m-%d")
    theme = random.choice(PROJECT_THEMES)
    
    print(f"🤖 Bugun: {today} | Mavzu: {theme}")
    
    prompt = f"""Create a complete Python project for a "{theme}".

Requirements:
1. Write a fully working Python script (main.py)
2. The code must be beginner-friendly and well-commented
3. Include error handling
4. Make it interactive (input/output)

Respond ONLY in this exact JSON format (no markdown, no extra text):
{{
  "repo_name": "daily-{theme.replace(' ', '-')}-{today}",
  "description": "A simple {theme} built with Python - Daily AI Project",
  "main_code": "# Full Python code here",
  "readme": "# Full README.md content here"
}}"""

    print("⏳ Claude AI kod yozmoqda...")
    result = ask_claude(prompt)
    
    # JSON tozalash
    result = result.strip()
    if result.startswith("```"):
        result = result.split("```")[1]
        if result.startswith("json"):
            result = result[4:]
    result = result.strip()
    
    return json.loads(result)

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
    import base64
    encoded = base64.b64encode(content.encode()).decode()
    
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
    
    # 1. Project yaratish
    project = generate_project()
    repo_name = project["repo_name"]
    
    print(f"📁 Project nomi: {repo_name}")
    
    # 2. GitHub repo yaratish
    create_github_repo(repo_name, project["description"])
    
    # 3. main.py yuklash
    push_file(
        repo_name, 
        "main.py", 
        project["main_code"],
        "🤖 AI generated: Add main Python script"
    )
    print("✅ main.py yuklandi")
    
    # 4. README yuklash
    push_file(
        repo_name,
        "README.md",
        project["readme"],
        "📝 Add README"
    )
    print("✅ README.md yuklandi")
    
    # 5. .gitignore yuklash
    gitignore = "__pycache__/\n*.py[cod]\n*.pyo\n.env\nvenv/\n.vscode/\n"
    push_file(repo_name, ".gitignore", gitignore, "🔧 Add .gitignore")
    print("✅ .gitignore yuklandi")
    
    print("=" * 50)
    print(f"🎉 Tayyor! https://github.com/{GITHUB_USERNAME}/{repo_name}")

if __name__ == "__main__":
    main()
