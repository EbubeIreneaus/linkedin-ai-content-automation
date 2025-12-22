# LinkedIn AI Content Automation Project

A Python-based automation tool that uses Generative AI to create and post niche-specific content to LinkedIn, tracks engagement over time, and intelligently generates future posts based on what performs best.

This project started as a dual-platform automation for both LinkedIn and Twitter (X), but due to API token/cost limitations with the AI provider, it now focuses exclusively on LinkedIn.

## Key Features

- **AI-Powered Content Generation**: Generates high-quality, niche-focused LinkedIn posts using a Generative AI model (GoogleAi).
- **Unique Hashtag Tracking**: Each post includes a unique, content-related hashtag with a random alphanumeric suffix (e.g., `#AIAutomationInsights_G2R9`) that serves as a unique post ID for tracking engagement.
- **Automated Posting**: Uses Playwright to automate posting to LinkedIn in a browser context.
- **Engagement Tracking**: Periodically scrapes engagement metrics (likes, views/impressions, comments) for each post by searching the unique hashtag and updates the CSV database.
- **Smart Content Evolution**: When generating new posts, previous high-engagement posts are fed back into the AI prompt to guide it toward creating similar, higher-performing content.
- **Data Persistence**: All posts and their metrics are stored in a CSV file (`linkedin_content.csv`) using Pandas.
- **Backup Mechanism**: CSV files are backed up automatically (in case of errors or crashes).
- **Error Handling**: Basic try-except blocks with potential backup triggers on failure.

## Project Workflow

1. **Initial Post**:
   - Generate new AI content based on the niche and optionally past data.
   - Add metadata (title, unique hashtag, timestamp, summary).
   - Post to LinkedIn via Playwright.
   - Save to CSV.

2. **Subsequent Posts (Loop)**:
   - Load existing CSV.
   - For each previous post, fetch current engagement using its unique hashtag.
   - Update likes/views/comments in the CSV.
   - Feed high-engagement posts/summaries into the AI prompt for analysis.
   - Generate new content inspired by top performers.
   - Post, save, and backup.

This creates a feedback loop that continuously improves content performance.

## CSV Structure Example (`data/linkedin_content.csv`)

```csv
title,unique_hashtag,createdAt,likes,views,comments,summary
The Real AI Automation ROI: Beyond the Hype,#AIAutomationInsights_G2R9,2025-12-10 22:07:02.284213,1,32,0,"We've all heard the buzzwords: 'AI-powered efficiency,' 'streamlined workflows'"
The Power of a Well-Defined API Gateway,#APIGatewayPros_B3K7,2025-12-11 15:47:18.785261,0,9,0,"In the world of microservices and complex web applications, a robust API gateway isn't just a nice-to-have, it's foundat"
Cracking the Code: From Legacy Systems to Seamless AI Integration,#AIIntegrationJourney_M5P1,2025-12-11 21:27:51.289277,0,0,0,"Migrating from clunky, legacy systems to modern, AI-driven workflows can feel like navigating a minefield"