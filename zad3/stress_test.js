import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '20s', target: 50 },  // Szybki skok do 50 użytkowników
    { duration: '40s', target: 100 }, // Max 100 użytkowników
    { duration: '20s', target: 0 },
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