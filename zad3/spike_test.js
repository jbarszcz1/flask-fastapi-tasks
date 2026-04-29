import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 10 },  // Normalny ruch
    { duration: '1s', target: 150 }, // NAGŁY SKOK do 150 VU
    { duration: '10s', target: 150 }, // Utrzymanie uderzenia
    { duration: '10s', target: 0 },   // Powrót do normy
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