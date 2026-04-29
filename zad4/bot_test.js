import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '20s', target: 50 },
    { duration: '40s', target: 100 },
    { duration: '20s', target: 0 },
  ],
};

export default function () {
  const url = 'http://134.112.40.231/submit';

  const params = {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    redirects: 0,
  };

  // Symulacja bota — wypełnia również pole honeypot
  const res = http.post(url, {
    name: 'Bot',
    surname: 'Attack',
    website: 'http://spam.com'  // honeypot wypełniony
  }, params);

  check(res, {
    'is status 303': (r) => r.status === 303,
  });
}