import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },  
    { duration: '1m',  target: 100 }, 
    { duration: '30s', target: 0 },   
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<500'],
  },
};

export default function () {
  const url = 'http://localhost:3000';
  const payload = JSON.stringify({ test_metric: 'capacity_check' });
  const params = {
    headers: { 'Content-Type': 'application/json' },
  };

  const res = http.post(url, payload, params);
  
  check(res, {
    'status is 200': (r) => r.status === 200,
  });

}
