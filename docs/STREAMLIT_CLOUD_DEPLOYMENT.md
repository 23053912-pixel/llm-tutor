# Streamlit Cloud Deployment Guide

## Quick Deployment to Streamlit Cloud

### Step 1: Push to GitHub
Make sure all your code is committed and pushed to GitHub:
```bash
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

### Step 2: Connect to Streamlit Cloud
1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Click "New app"
3. Select your GitHub repository: `https://github.com/23053912-pixel/llm-tutor`
4. Branch: `main`
5. Main file path: `capstone_streamlit.py`

### Step 3: Configure Secrets
1. After deployment, click the three dots (⋮) menu
2. Select "Settings"
3. Click "Secrets"
4. Add your Groq API key:
   ```
   GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxxx"
   ```
5. Save and the app will automatically redeploy

### Step 4: Share the App
Your app is now live! Share the URL:
```
https://llm-tutor-[random-string].streamlit.app/
```

## Environment Setup on Streamlit Cloud

The app automatically:
- Loads the API key from Streamlit Cloud secrets
- Falls back to environment variables if needed
- Shows a helpful error message if no API key is configured

## Troubleshooting

**App timing out or not loading:**
- Check that the API key is configured in Secrets
- Click "Rerun" or refresh the page
- Check the logs in Streamlit Cloud dashboard

**API errors:**
- Verify your Groq API key is correct
- Check that your account has API quota remaining
- Ensure the key is exactly as provided in console.groq.com

## Local Testing Before Deployment

Test the app locally before deploying:
```bash
# Setup local secrets
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit and add your API key
notepad .streamlit/secrets.toml

# Run the app
streamlit run capstone_streamlit.py
```

## Streamlit Cloud Free Tier Limits

- CPU: 1 vCPU
- Memory: 2GB
- Concurrent sessions: 3
- App timeout: 30 minutes of inactivity

For production use with more traffic, upgrade to a Streamlit Community Cloud paid plan.

## Monitoring and Logs

Check logs in the Streamlit Cloud dashboard:
1. Go to your app settings
2. Click "Logs" to see error messages
3. Check for any import or dependency issues

## Environment Variables

The following are automatically available:
- `GROQ_API_KEY` - Your Groq API key (from Secrets)
- Built-in Streamlit environment variables

## Updating the Deployment

To update your deployed app:
1. Make changes locally
2. Commit and push to GitHub
3. The app automatically redeploys within a few minutes
4. Refresh your browser to see changes
