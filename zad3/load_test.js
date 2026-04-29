import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 40 },  
    { duration: '3m', target: 40 },
    { duration: '30s', target: 0 },
  ],
};

export default function () {
  const url = 'http://134.112.40.231/';

  const params = {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    redirects: 0, // nie podążaj za redirectem, mierz tylko /submit
  };

  const res = http.post(url, { name: 'Stress', surname: 'Test' }, params);

  check(res, {
    'is status 303': (r) => r.status === 302, // dla flask 302 dla fastapi 200
  });
}