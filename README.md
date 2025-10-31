# 🤖 SDR Agent — AI-Powered Sales Development Automation

An intelligent sales development assistant built for **Verzel** job opportunity.

> **Note:** Due to time constraints, this project wasn't completed within the one-week deadline. However, I'm continuing development as a personal project to deliver a fully functional solution.

This project integrates advanced conversational AI with workflow automation to create a seamless lead management experience for sales teams.

---

## 🚀 Key Features

- 💬 **Conversational AI** powered by OpenAI for natural lead interaction  
- 🧠 **Lead qualification workflow** using intent classification and dynamic context memory  
- 📅 **Automatic meeting scheduling** via Google Calendar with Google Meet links  
- 🔁 **Pipefy synchronization** after qualification or booking events  
- 🧾 **Persistent conversation tracking** and logging with repositories  
- 🔐 **Secure OAuth2 integration** for Google API  
- ⚙️ **Modular architecture** for easy expansion and workflow customization  
- 🌐 **Web-based chat interface** for seamless user interaction  

---

## 🧩 System Architecture

> **Note:** Some files in the repository may be reorganized or removed as development progresses.
>
> > ```
> src/
> ├── agents/
> │   ├── cv_manager.py              # Manages conversational context  
> │   ├── intent_classifier.py       # Classifies user intent  
> │   └── cv_agent.py                # Main conversational agent  
> │
> ├── DB/
> │   └── repositories/              # Data repositories  
> │       ├── conversation_rep.py    # Conversation storage  
> │       ├── lead_rep.py            # Lead data handling  
> │       └── log_rep.py             # Event logging  
> │
> ├── integrations/
> │   ├── gcalendar.py               # Google Calendar API wrapper  
> │   ├── OpenAi_client.py           # OpenAI API wrapper  
> │   └── pipefy.py                  # Pipefy API wrapper  
> │
> ├── services/
> │   ├── calendar_service.py        # Google Calendar booking service  
> │   └── pipefy_service.py          # Pipefy integration service  
> │
> ├── workflows/
> │   ├── lead_qualification.py      # Lead qualification process  
> │   ├── meet_booking.py            # Meeting scheduling workflow  
> │   └── pipefy_sync.py             # Synchronization after qualification  
> │
> ├── prompts/
> │   ├── system_p.py                # System-level prompts for classification  
> │   ├── scheduling_p.py            # Scheduling data prompt  
> │   └── qualification_p.py         # Qualification data prompt  
> │
> ├── models/
> │   └── conversation.py            # Conversation data model  
> │
> ├── config/
> │   └── settings.py                # Environment variables and configuration  
> │
> └── main.py                        # Entry point for local testing  
> ```

---

## 🎯 Project Vision

The goal is to deploy this SDR agent as a fully functional solution, integrated with a modern web-based chat interface (front-end) that provides:

- Real-time conversational experience  
- Seamless lead qualification flows  
- Instant meeting scheduling capabilities  
- Professional user interface for lead interactions  




https://github.com/user-attachments/assets/c6b90eec-96a2-4618-a60f-7727ada1ef0f



> **Note:** This is *not* a final version of the web chat, and the SDR agent is *not* yet integrated into the prototype.

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/BrenoMacedo56/sdr-agent.git
cd sdr-agent
```
## 2. Install Dependencies
pip install -r requirements.txt

## 3. Configure Environment Variables

Create a .env file in the root directory:

OPENAI_API_KEY=your_openai_api_key
GOOGLE_CREDENTIALS_PATH=path/to/credentials.json
PIPEFY_API_TOKEN=your_pipefy_token
PIPEFY_PIPE_ID=your_pipe_id

## 4. Set Up Google Calendar OAuth

Enable Google Calendar API in Google Cloud Console

Download OAuth2 credentials as credentials.json

Place the file in the project root directory

Run authentication flow on first use

## 5. Run the Application
python src/main.py

## 🔧 Configuration

Key configuration options in config/settings.py:

OpenAI Model: Configure GPT model version and parameters

Calendar Settings: Set availability windows and meeting duration

Pipefy Integration: Configure pipe IDs and field mappings

Conversation Settings: Adjust context window and memory retention

## 📝 Usage

The SDR Agent follows this workflow:

- Intent Classification — Identifies whether the lead wants to schedule a meeting or needs qualification

- Context Management — Maintains conversation history for personalized interactions

- Lead Qualification — Collects necessary information through natural conversation

- Meeting Scheduling — Books available slots and generates Google Meet links

- Pipefy Sync — Updates CRM with qualification data and meeting details

## 🛠️ Technologies Used

- 🐍 Python 3.8+ — Core backend language

- 🤖 OpenAI GPT API — Conversational AI engine

- 📅 Google Calendar API — Meeting scheduling

- 🔁 Pipefy API — CRM integration

- 🔐 OAuth2 — Secure authentication

## 🚧 Roadmap

- Complete core workflow implementation

- Add comprehensive error handling

- Implement conversation analytics

- Develop web-based chat interface

- Add automated testing suite

- Implement multi-language support

- Deploy production-ready version with frontend integration

# 👤 Author

**Breno Macedo**
🔗 GitHub: @BrenoMacedo56
