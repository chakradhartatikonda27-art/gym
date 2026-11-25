# Siyantech Gym OS – All-in-One Fitness & Wellness Operating Platform

A modern, high-performance, multi-tenant operating system for gym chains and fitness studios. Featuring an instant client demo, complete billing POS, biometric & QR access control simulator, retention AI, member 360 CRM, and multi-branch management.

---

## ⚡ Live Demo
- **Local:** Run `http://localhost:3000` or open `index.html` directly in any browser.
- **Hosted on Vercel:** Instant static deployment with zero external dependencies.

---

## 🚀 Key Modules & Capabilities

1. **Dashboard & Command Center:** Real-time occupancy gauge, peak-hour heatmaps, live revenue metrics.
2. **Billing Counter & POS:** Barcode scanning, itemized invoicing, GST 18%, discounts/coupons, partial/advance payments, refunds & credit notes.
3. **Members 360 & CRM:** Member directory, 28-day attendance streak matrix, KYC details, plan renewal & freeze controls.
4. **Access Control & Turnstiles:** Gate verification simulator supporting Face Recognition, Dynamic QR, RFID, and Fingerprint.
5. **Class Timetable & PT Booking:** Weekly interactive slot booking, trainer assignment, capacity management.
6. **Retention AI & Lead Pipeline:** Drag-and-drop conversion funnel, automated churn risk scoring, WhatsApp/SMS nudges.
7. **Staff & Payroll:** Shift rosters, leave approvals, automated trainer commission calculations.
8. **Finance & P&L:** Cash drawer shift closing reconciliation, expense breakdowns, 16 downloadable CSV reports.
9. **Equipment Maintenance:** QR asset scanning, health degradation scoring, maintenance logging.
10. **Multi-Branch & Franchise:** Centralized pricing, cross-branch access, 5% royalty auto-calculations.

---

## 📁 Repository Structure
```
siyantech-gym-os/
├── index.html               # Production-ready client demo (all 35 modules)
├── client_demo.html         # Synced demo distribution
├── vercel.json              # Vercel deployment configuration
├── docker-compose.yml       # PostgreSQL 15, Redis 7 & FastAPI backend
├── backend/                 # FastAPI REST API + SQLAlchemy async RLS engine
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   └── schemas/
│   ├── alembic/
│   ├── Dockerfile
│   └── requirements.txt
└── frontend/                # Next.js 14 App Router application
```

---

## 🛠️ Local Development

### 1. Run Client Demo (Port 3000)
```bash
python3 -m http.server 3000
```
Open **[http://localhost:3000](http://localhost:3000)** in your browser.

### 2. Run Full Backend Stack (Docker)
```bash
docker-compose up --build -d
```
Interactive Swagger API docs available at: **[http://localhost:8000/docs](http://localhost:8000/docs)**.

---

## 📄 License
Proprietary – © Siyantech Global. All rights reserved.
