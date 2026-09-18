# Cloudflare deployment

The frontend is a static Vite application and can be deployed to Cloudflare Pages.

## Pages build settings
- Root directory: frontend
- Build command: npm run build
- Output directory: dist
- Node.js: 20
- Environment variable: VITE_API_URL=https://your-api-origin

The FastAPI backend is not a Cloudflare Pages runtime. Deploy it to an HTTPS origin that supports WebSockets, then point VITE_API_URL at that origin.

## WebSocket
The browser derives the WebSocket URL from VITE_API_URL by switching http to ws and https to wss. The API origin therefore needs a publicly reachable /ws endpoint.

## Security
- Restrict CORS to the deployed Pages origin.
- Authenticate operator WebSocket sessions before production use.
- Keep secrets in environment/secret stores, never in Vite source.
