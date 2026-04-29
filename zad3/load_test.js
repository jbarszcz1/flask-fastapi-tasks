import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 40 },  // 1. RAMP-UP: Powolne wejście do 40 użytkowników
    { duration: '3m', target: 40 },  // 2. PLATEAU: Utrzymanie 40 osób przez 3 minuty
    { duration: '30s', target: 0 },  // 3. RAMP-DOWN: Spokojne wygaszanie ruchu
  ],
};

export default function () {
  const url = 'http://134.112.40.231/';

  const payload = JSON.stringify({
    name: 'Test',
    surname: 'User'
  });

  const params = {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  };

  const res = http.post(url, { name: 'Stress', surname: 'Test' }, params);

  check(res, {
    'is status 200': (r) => r.status === 200,
  });

}