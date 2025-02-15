# AI Schedule Maker

## Overview
AI Schedule Maker is an advanced AI-powered scheduling tool that optimizes task allocation and generates scientifically effective timetables for various use cases, including personal productivity, school schedules, and work routines.

## Features
- **AI-Powered Scheduling**: Uses constraint optimization and AI models to generate the best schedule.
- **Custom Task Inputs**: Users can enter tasks with priority levels and duration.
- **School Timetable Generator**: Automatically balances subject distribution.
- **User Authentication**: Save and retrieve schedules.
- **Modern UI**: Built with React and TailwindCSS.
- **Backend**: Flask API with SQLite database.

## Installation & Setup
### 1. Clone the Repository
```sh
git clone https://github.com/youssof20/ai-schedule-maker.git
cd ai-schedule-maker
```

### 2. Backend Setup (Flask API)
#### Install Dependencies
```sh
cd backend
pip install -r requirements.txt
```
#### Run the Backend Server
```sh
flask run
```

### 3. Frontend Setup (React)
#### Install Dependencies
```sh
cd ../frontend
npm install
```
#### Start the Frontend
```sh
npm run dev
```

### 4. Deployment (Docker)
#### Build and Run with Docker
```sh
docker-compose up --build
```

## API Endpoints
- `POST /generate` - Generate an optimized schedule.
- `POST /timetable` - Generate a school timetable.
- `POST /save_schedule` - Save a schedule.
- `GET /get_schedule` - Retrieve a saved schedule.

## Contributing
Feel free to fork the repository, submit issues, and open pull requests!

## License
MIT License
