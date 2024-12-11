FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev
COPY src ./src
COPY rules ./rules
CMD ["node", "src/index.js"]
