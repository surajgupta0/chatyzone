# Stage 1: Build the React App
FROM node:lts-alpine

WORKDIR /var/www/html/chatifizer/frontend

# Copy only package.json first for layer caching
COPY package*.json ./

# Clean install
RUN npm install --no-optional --legacy-peer-deps

# Now copy source
COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev"]
