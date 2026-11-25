const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface FastOnboardData {
  phone: string;
  full_name: string;
  gender: 'Male' | 'Female' | 'Other';
  plan_id: string;
  start_date?: string;
  cash_amount?: number;
  online_amount?: number;
}

export async function loginUser(email: string, password: string) {
  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error('Login failed');
  return res.json();
}

export async function fastOnboardMember(token: string, data: FastOnboardData) {
  const res = await fetch(`${API_BASE_URL}/members/fast-onboard`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Onboarding failed');
  return res.json();
}

export async function checkinMember(token: string, memberId: string, qrToken: string) {
  const res = await fetch(`${API_BASE_URL}/attendance/qr-checkin`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ member_id: memberId, qr_token: qrToken }),
  });
  if (!res.ok) throw new Error('Check-in failed');
  return res.json();
}
