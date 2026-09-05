# Autonomous AI Issue Triager 🤖

An event-driven CI/CD workflow that uses Large Language Models (LLMs) to autonomously categorize, triage, and respond to GitHub repository issues in real-time.

## 📖 Overview
Maintaining open-source projects requires significant overhead, with maintainers spending hours asking users for missing logs or categorizing unstructured bug reports. 

This project solves that by acting as a "first line of defense." It leverages **GitHub Actions** and the **Google Gemini REST API** to instantly evaluate inbound issues, apply the correct labels, and politely request missing information—allowing human developers to focus on writing code.

## ✨ Features
* **Event-Driven Automation:** Triggered instantly via GitHub Actions whenever a new issue is opened.
* **Intelligent Triage:** Uses Gemini 3.6 Flash to parse unstructured text and output strict, machine-readable JSON.
* **Defensive Engineering:** Built with strict Prompt Injection safeguards, including input sanitization and hardcoded output validation, to prevent malicious actors from hijacking the bot.
* **Serverless Architecture:** 100% cloud-native with zero local hosting or maintenance required.

## 🛠️ Tech Stack
* **Compute:** GitHub Actions (CI/CD)
* **Language:** Python 3.10
* **AI Provider:** Google Gemini API 
* **Integration:** GitHub REST API

## 🔒 Security Architecture
Deploying AI on untrusted user input presents a security risk. This agent implements "Defense in Depth":
1. **Principle of Least Privilege:** The GitHub Action token is strictly scoped to `issues: write`, preventing the AI from modifying source code or reading repository secrets.
2. **Delimiter Isolation & Sanitization:** User input is stripped of XML tags and isolated from system instructions to prevent prompt override attacks.
3. **Strict Validation:** The Python script acts as a hardcoded gatekeeper, dropping any AI-generated labels that do not match a strict internal allow-list.

## 📱 Customizing for Your Stack (e.g., Flutter)
Because this agent is driven by a customizable system prompt, it is entirely language-agnostic. You can tailor the AI's instructions to fit the specific needs of your framework.

**Example: Flutter Repositories**
By modifying the `system_prompt` in `agent.py`, you can instruct the bot to look for framework-specific diagnostic data:
> *"If the user is submitting a bug report for this Flutter app, verify they have included their `flutter doctor` output. If it is missing, politely ask them to run it and paste the logs before a human maintainer reviews the issue."*

## 🚀 How It Works
1. A user opens a new issue on GitHub.
2. GitHub Actions detects the `issues: opened` event and boots a temporary Ubuntu runner.
3. The runner injects the API credentials securely via GitHub Secrets.
4. The Python script sanitizes the issue body and requests a JSON evaluation from Google Gemini.
5. The script validates the AI's response and executes a REST API call to GitHub to label the issue and post a comment.