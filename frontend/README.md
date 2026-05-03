# Frontend Dashboard

Next.js + Material UI dashboard for defect detection monitoring and uploads.

## Files

- `pages/index.js` - Main dashboard
- `pages/_app.js` - App wrapper
- `components/UploadCard.js` - Upload interface
- `components/StatsCard.js` - Statistics display
- `services/api.js` - Backend API client
- `cypress/e2e/upload.cy.js` - E2E tests

## Quick Start

### Local Development

```bash
npm install
npm run dev
```

Open http://localhost:3000

### Docker

```bash
docker build -t frontend .
docker run -p 3000:3000 frontend
```

## Features

- **Upload Interface** - Select and upload PNG/JPEG images
- **Live Dashboard** - Real-time statistics and defect history
- **History Table** - View recent predictions with confidence scores
- **Color-coded Results** - Red for defects, Green for clean products

## Environment Variables

- `NEXT_PUBLIC_BACKEND_URL` - Backend API base URL

## Testing

### E2E Tests

```bash
npm run cy:open   # Open Cypress UI
npm run cy:run    # Run tests
```

## Build & Deployment

```bash
npm run build
npm run start
```

## UI Components

- **UploadCard** - File input and submission
- **StatsCard** - Summary statistics
- **History Table** - Defect log with pagination
- **Charts** - Defect frequency (optional)
