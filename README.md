# ArXiv Recommendation System

A personalized paper recommendation system for arXiv submissions, helping researchers stay up-to-date with the latest research in their field.

## Features

- Daily updates of new arXiv submissions
- Personalized paper recommendations based on user preferences
- Interactive rating system for papers
- Clean and intuitive user interface

## Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Node.js (v16 or higher)
- Python 3.8+

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ArXivRecSys.git
cd ArXivRecSys
```

2. Set up environment variables:
```bash
cp client/.env.example client/.env
cp backend/.env.example backend/.env
```

3. Start the development environment:
```bash
docker-compose up
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Contributing

Please read our contributing guidelines before submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 