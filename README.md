# AcademiSync
Web development + cloud

AcademiSync
Learning Management System | Hackathon Submission

1. Project Snapshot
Team Size: 4 members
Key Innovation: Hierarchical code-based access system

2. Core Features
User Hierarchy System
Admins generate 8-digit institution codes

Trainers register using admin codes

Students enroll with trainer codes (auto-batch assignment)

Key Modules
Course management dashboard

Assignment submission portal with file uploads

Real-time progress tracking

3. Technical Implementation
Backend Logic
The registration flow uses Django's model inheritance:

CustomUser model extends AbstractUser

Code model generates unique identifiers using UUID

Django signals automate batch assignments

Performance Optimizations
Database indexing reduces query times by 300ms

Cached frequently-accessed resources

Async file uploads to Cloudinary

4. Setup Instructions
Clone repository: git clone https://github.com/ThePranish03/AcademiSync.git

Install dependencies: pip install -r requirements.txt

Configure .env file

Run migrations: python manage.py migrate

Quick Start:
docker-compose up (pre-configured with sample data)

5. Hackathon Challenges
Challenge	Solution
Complex user flows	Custom Django middleware
Mobile rendering	Bootstrap 5 + Flexbox
Secure file handling	Cloudinary signed uploads

6. Future Roadmap
Integrate WebSocket notifications

Develop React Native mobile app

Add plagiarism detection

License: MIT