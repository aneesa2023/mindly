# Mindly

Welcome to **Mindly** – Personalized AI-Powered Learning Paths.  
Craft your own study curriculum with YouTube videos, structured notes, and dynamic summaries in minutes.

---

## 🧠 1. Inspiration

As developers and students, we often struggled to find structured, high-quality learning resources tailored to our exact needs. Tutorials were too generic. Video playlists were unorganized. PDFs were boring.

We wanted something smarter.

Mindly was built to solve this: a platform that takes your curiosity and instantly turns it into a personalized learning path — complete with chapters, videos, summaries, and study links — powered by AI.

No fluff. No chaos. Just structured learning, your way.

---

## 💡 2. What It Does

Mindly generates a complete **learning path** from a single topic input. Here's how it works:

- 🧠 **You provide**:
  - A topic (e.g., “React Hooks” or “Probability Theory”)
  - Short description
  - Category (Tech, Math, History, etc.)
  - Difficulty (Beginner–Advanced)
  - Tone (Conversational, Educational, etc.)
  - Number of chapters

- ⚡ **Mindly generates**:
  - 📖 Chapter-wise content with learning objectives, concepts, study notes
  - 📺 Curated YouTube videos per chapter via real-time API search
  - 📚 Course overview, summary, time commitment, and recommended links
  - 🧾 Everything saved to Amazon S3 as JSON and served instantly to the frontend

---

## 🔨 3. How We Built It

### 🖥️ Frontend
- **React + Bootstrap** for smooth and responsive UI
- Pages:
  - `Create Course`: dynamic form with validation and loading state
  - `Course List`: sorted display of all saved courses with metadata
  - `Course Detail`: side-by-side chapter viewer with embedded video + notes
- Toast alerts, conditional navigation, and beautiful button UX

### ⚙️ Backend
- **FastAPI (Python)** with structured Pydantic models
- Prompts generated and passed to **Amazon Bedrock (Claude 3.5 Sonnet)**
- **YouTube Data API v3** used to get top 3–5 relevant videos per chapter
- Final structured course is saved to **Amazon S3** under a unique course ID
- APIs include: `generate-learning-path`, `upload-course-to-s3`, `get-course`, and `list-courses`

---

## 🚀 4. Accomplishments We're Proud Of

- ⚡ Full course generation in under 2 minutes
- 📚 Real-time YouTube search that adapts per chapter
- 🎥 Embedded video viewer with auto chapter sync
- 🔄 Stateless backend using AWS + FastAPI
- 🧠 Actually used it to learn "LLMs" while commuting — and it worked!

---

## ✨ 5. Key Features

- ✅ Fully dynamic curriculum generation via Claude 3.5
- ✅ Supports multiple tones, difficulty levels, and topics
- ✅ Embedded YouTube videos based on auto-ranked queries
- ✅ Study notes are audio-friendly and visually structured
- ✅ Clean UI/UX with chapter switcher, summaries, and study tips
- ✅ Responsive frontend with loading states and toast notifications

---

## 🔌 6. Backend API Integration

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/generate-learning-path/` | `POST` | Accepts topic + config and returns a full course object |
| `/upload-course-to-s3` | `POST` | Saves generated course JSON to S3 |
| `/get-course/{course_id}` | `GET` | Fetches course data from S3 by ID |
| `/list-courses/` | `GET` | Returns a list of all saved course IDs |

---

## 🧰 7. Built With

- **Frontend**
  - React
  - React-Bootstrap
  - Toast/Spinner/Router DOM
  - JSX + Styled Components

- **Backend**
  - FastAPI (Python)
  - Pydantic
  - Boto3
  - Amazon Bedrock (Claude 3.5)
  - YouTube Data API
  - Amazon S3

- **Infra / Hosting**
  - AWS (S3, Bedrock, Polly-ready)
  - dotenv for config management

---

## 🌱 8. What’s Next for Mindly

- 🗓️ Calendar View: Estimate weekly study goals based on chapter count
- 🧪 AI-generated quiz questions for each chapter
- 📈 Completion tracking and "Best Learner" leaderboard
- 📊 Chapter Visuals: auto-generate diagrams and flowcharts via AI
- 🌍 Language Support: Hindi, Spanish, Arabic, Telugu & more

---

Feel free to contribute, suggest features, or fork this repo to build your own personalized learning platform 🚀  
