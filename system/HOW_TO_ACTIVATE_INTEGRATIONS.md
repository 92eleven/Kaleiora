# How to Activate Integrations in Kaleiora

## 1. InVideo AI (Primary Video Generator) — Recommended
1. Sign up: https://invideo.io/pricing/ (Plus $17/mo recommended)
2. After signup, go to your account settings and get your API key
3. Open `/home/team/shared/config/api_keys.json`
4. Set: `"api_key": "your-key-here"` and `"enabled": true` under the `invideo` section
5. Creative Agent will now generate real AI videos (Seedance 2.0, Veo 3.1, Kling 3)

## 2. Canva API (Design Automation)
1. Sign up for Canva Pro (~$13/mo): https://www.canva.com
2. Go to https://www.canva.com/developers/ → Create a new app
3. Get your API key
4. Set: `"api_key": "your-key-here"` and `"enabled": true` under `canva`

## 3. Runway ML (Alternative Video Generator)
- Available if you prefer Runway instead. Same setup pattern.

## When You Activate
The team switches from mock mode to live automatically.
No code changes, no restarts. Just paste and go.