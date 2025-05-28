# Tickets P2P - Event Ticket Reselling Platform

A peer-to-peer marketplace platform that connects ticket holders who cannot attend events with potential buyers. The platform facilitates secure ticket reselling for various event types including concerts, theatre shows, and sports events.

## 🎯 Project Overview

Tickets P2P is designed to create a trusted marketplace for ticket reselling, reduce ticket fraud through verified listings, and provide an easy-to-use interface for both sellers and buyers.

### Key Features

- **Secure Marketplace**: Trusted environment for ticket transactions
- **Event Categories**: Support for concerts, theatre, sports, and other events
- **Advanced Filtering**: Search by date, price, location, and event type
- **User Dashboard**: Manage offers, view purchase history, and track activity
- **Responsive Design**: Mobile-first approach with desktop optimization

## 🏗️ Technical Architecture

### Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Next.js (React/TypeScript)
- **Database**: SQLite
- **Testing**: Playwright (E2E tests)
- **Authentication**: JWT-based authentication

### Project Structure

```
tickets-p2p/
├── backend/           # FastAPI application
├── frontend/          # Next.js application
├── testing/           # Playwright E2E tests
├── docs/             # Documentation
├── PRD.md            # Product Requirements Document
└── README.md
```

## 👥 User Roles

- **Anonymous User**: Browse listings without registration
- **Registered User**: Create offers, buy tickets, manage profile
- **Seller**: Create and manage ticket offers
- **Buyer**: Purchase tickets from offers

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/tickets-p2p.git
   cd tickets-p2p
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Database Setup**
   ```bash
   cd backend
   python -m alembic upgrade head
   ```

### Running the Application

1. **Start the Backend**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload
   ```

2. **Start the Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📊 Core Features

### Authentication
- User registration and login
- JWT-based session management
- Secure password hashing

### Offer Management
- Create, edit, and delete ticket offers
- Mark offers as sold
- Comprehensive offer details including seat information

### Search & Filtering
- Filter by event type (concert, theatre, sports)
- Date range filtering (next 7 days, next month, custom)
- Price range and location filtering
- Real-time search functionality

### User Dashboard
- Manage active offers
- View purchase history
- Profile management
- Saved listings

## 🧪 Testing

### Running Tests

```bash
# Backend unit tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# E2E tests with Playwright
cd testing
npx playwright test
```

### Test Coverage
- Minimum 80% code coverage target
- Unit, integration, and E2E testing
- Cross-browser compatibility testing

## 📱 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info

### Offers
- `GET /api/offers` - List all active offers
- `POST /api/offers` - Create new offer
- `PUT /api/offers/{id}` - Update offer
- `PATCH /api/offers/{id}/mark-sold` - Mark as sold

### Events
- `GET /api/events` - List events
- `POST /api/events` - Create event

## 🛣️ Development Roadmap

### Phase 1 - Core MVP (4-6 weeks)
- ✅ Basic authentication system
- ✅ Offer CRUD operations
- ✅ Simple search and filtering
- ✅ Basic responsive UI

### Phase 2 - Enhanced Features (3-4 weeks)
- 🔄 Advanced filtering options
- 🔄 User dashboard improvements
- 🔄 Image upload functionality
- 🔄 Email notifications

### Phase 3 - Polish & Testing (2-3 weeks)
- ⏳ Comprehensive E2E testing
- ⏳ Performance optimizations
- ⏳ UI/UX improvements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow existing code style and conventions
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For questions or support, please open an issue on GitHub or contact the development team.

## 🔮 Future Enhancements

- Mobile application
- Payment integration
- Advanced messaging system
- User ratings and reviews
- Machine learning recommendations
- Fraud detection system

---

**Version**: 1.0  
**Last Updated**: December 2024 