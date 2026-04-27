```python?code_reference&code_event_index=2
markdown_content = """# 🤖 Auto-Draft: 24/7 AI Email Assistant

Welcome to the **Auto-Draft AI Email Assistant**! This project turns your Gmail inbox into a self-driving machine. It runs quietly in the background 24 hours a day, reads your new unread emails, and uses Google's powerful Gemini AI to automatically write professional draft responses for you. 

Even if you have very little coding experience, this guide will walk you through exactly how to set it up, test it on your computer, and host it in the cloud for **100% free forever**.

---

## ✨ What Does It Do?
1. **Always Awake:** Checks your inbox every 5 minutes, 24/7.
2. **Smart Filtering:** Automatically skips newsletters, "no-reply" addresses, and automated alerts so it doesn't waste time on robots.
3. **AI Brain:** Uses `gemini-2.5-flash-lite` (Google's high-volume AI model) to read the email and understand the context.
4. **Drafts, Not Sends:** It safely saves a polite, professional reply in your "Drafts" folder. It **never** sends an email without your permission.
5. **Speed Limit Safe:** Built-in "speed governors" ensure it never gets blocked by Google's API limits.

---

## 🛠️ What You Need Before Starting
You don't need to be a programmer, but you will need a few free accounts:
* **A Gmail Account:** The inbox you want to automate.
* **Google Cloud Console:** To get permission to read your emails.
* **Google AI Studio:** To get your free Gemini AI brain.
* **GitHub Account:** To store your code.
* **Render.com Account:** The cloud server that runs your code 24/7.
* **UptimeRobot Account:** A free tool to make sure your server never falls asleep.

---

## 🚀 Step-by-Step Setup Guide

### Phase 1: Getting Your Golden Keys (API Setup)

Your script needs two "keys" to work: one for your Inbox, and one for the AI.

**1. The Gemini AI Key**
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Click **Get API Key** and create a new key.
3. Copy this long string of letters and numbers. This is your `GEMINI_API_KEY`. Keep it secret!

**2. The Gmail Credentials**
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a New Project.
3. Search for the **Gmail API** and click "Enable".
4. Go to **Credentials** -> **Create Credentials** -> **OAuth Client ID** (Choose "Desktop App").
5. Download the JSON file it gives you. 
6. Rename that file to exactly **`credentials.json`** and put it inside your project folder.

---

### Phase 2: Testing on Your Computer

Before we put it in the cloud, let's make sure it works on your laptop.

1. **Install the required libraries:** Open your computer's terminal (or command prompt) and run:
   ```
```text?code_stdout&code_event_index=2
[file-tag: README.md]

```bash
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib google-genai flask
   ```
2. **Add your AI Key:** Open the `main.py` file in a text editor. Find the line that says `GEMINI_API_KEY = ...` and temporarily paste your real AI key inside the quotes.
3. **Run the script:** In your terminal, run:
   ```bash
   python main.py
   ```
4. **The Login Screen:** Because this is your first time, a web browser will pop up asking you to log into your Google Account. It might give you a scary warning saying "Google hasn't verified this app." That is normal (you made the app!). Click **Advanced** and **Continue**.
5. **The Magic Token:** After logging in, a new file called `token.json` will magically appear in your folder. This is your permanent login pass!

**Send yourself a test email from another account, leave it Unread, and watch the terminal. It should find the email, draft a response, and wait 15-20 seconds before checking the next one.**

---

### Phase 3: Moving to the Cloud (Render)

Now we want this to run even when your laptop is turned off. 

**1. Hide Your Secrets**
Never put passwords on the internet! Create a file named `.gitignore` in your folder and paste this inside:
```text
credentials.json
token.json
__pycache__/
```

**2. Upload to GitHub**
Create a new **Private** repository on GitHub. Upload three files: `main.py`, `requirements.txt`, and `.gitignore`.

**3. Set up the Render Server**
1. Log into [Render.com](https://render.com/) and click **New +** -> **Web Service**.
2. Connect your GitHub account and select your repository.
3. Settings:
   * **Language:** Python
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `python main.py`
   * **Instance Type:** Free

**4. Inject Your Secrets into the Cloud**
Since we hid your passwords from GitHub, we have to give them directly to Render.
1. Scroll down to **Environment Variables** and click **Add Environment Variable**.
2. **Variable 1:**
   * Key: `GEMINI_API_KEY`
   * Value: Paste your actual Gemini API key here.
3. **Variable 2:**
   * Key: `GMAIL_TOKEN`
   * Value: Open the `token.json` file on your computer, copy **everything** inside it (including the `{ }` brackets), and paste it here.
4. **Variable 3:**
   * Key: `PYTHONUNBUFFERED`
   * Value: `1` *(This forces Render to show you live logs).*

Click **Deploy**! Wait a few minutes, click the "Logs" tab, and you should see it say `"Using cloud environment variables for Gmail login..."`

---

### Phase 4: Keeping It Awake 24/7

Render's free tier goes to sleep if nobody visits it for 15 minutes. We built a tiny "fake website" into your script to prevent this.

1. Once Render finishes deploying, it will give you a web link at the top (e.g., `https://my-email-bot.onrender.com`).
2. Go to [UptimeRobot.com](https://uptimerobot.com/).
3. Click **Add New Monitor**.
4. Set Monitor Type to **HTTP(s)**.
5. Paste your Render URL into the box.
6. Set the monitoring interval to **5 minutes**.

UptimeRobot will now "visit" your app every 5 minutes. Render will think you have a very dedicated fan, and it will never turn off your AI!

---

## 🛑 Troubleshooting & Important Notes

* **I have 100+ unread emails, why is it only doing a few?** Google places strict rate limits on free AI accounts. The code is designed to only pull **3 emails at a time**, wait 20 seconds between each one, and then sleep. It will slowly and safely chew through your massive backlog over the next few hours without crashing.
* **Why did it skip my test email?**
  Make sure your test email is marked as **Unread**. If you open it on your phone before the bot gets to it, the bot will ignore it. It also ignores anything containing the words "no-reply" or "newsletter".
* **What AI model is this using?**
  It is strictly coded to use `gemini-2.5-flash-lite`. This is Google's high-volume tier that allows you to process enough emails without hitting the strict "20 per day" limit placed on other models.
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(markdown_content)

print("[file-tag: README.md]")

```
Your Markdown file is ready
[file-tag: code-generated-file-0-1777314334042294669]

I have created a comprehensive, beginner-friendly `README.md` file for your Auto-Draft AI Email Assistant project. It breaks down the entire process from getting API keys to setting up the local environment, deploying securely on Render using environment variables, and configuring UptimeRobot to keep the service running 24/7. 

It also includes a troubleshooting section covering the specific hurdles we navigated today, such as the `gemini-2.5-flash-lite` model selection and API rate-limit batching. Let me know if you would like anything else added to the documentation!