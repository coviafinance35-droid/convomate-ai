FROM node:22-slim AS frontend
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY frontend ./frontend
COPY index.html vite.config.ts tsconfig.json ./
RUN npm run build
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend ./backend
COPY migrations ./migrations
COPY public ./public
COPY --from=frontend /app/dist ./dist
ENV PORT=3000
EXPOSE 3000
CMD ["sh","-c","uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-3000}"]
