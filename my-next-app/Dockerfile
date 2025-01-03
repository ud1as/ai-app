FROM node:18-alpine

WORKDIR /src

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Expose the port Next.js runs on
EXPOSE 3000

# Start the application in dev mode
CMD ["npm", "run", "dev"]