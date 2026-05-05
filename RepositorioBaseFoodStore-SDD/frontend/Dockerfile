# Base stage
FROM node:20-alpine

# Set work directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy project files
COPY . .

# Expose port (Vite default)
EXPOSE 5173

# Run development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
