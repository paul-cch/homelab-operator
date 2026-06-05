# Privacy Model

Homelab Operator is designed for infrastructure repositories that may be
private, sensitive, or operationally revealing.

Public examples must be synthetic. Do not publish:

- hostnames, private domains, real IP addresses, or network ranges
- VM, container, cluster, or service inventories from a real estate
- secrets, token names, authorization headers, cookies, or `.env` content
- runtime logs, deployment markers, backups, or generated private reports
- personal schedules, messages, academic materials, or assistant memory payloads

Safe examples use names like `source`, `host`, `runtime`, `live-config`, and
`external-service`. They show the shape of the contract without revealing the
shape of a real system.
