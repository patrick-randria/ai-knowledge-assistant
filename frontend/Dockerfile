<<<<<<< HEAD
FROM node:23-alpine

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5713

ENTRYPOINT ["npm", "run", "dev", "--", "--port=5713", "--host=0.0.0.0"]
=======
# Use Node.js 20 as the base image for building the frontend
FROM node:20 AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# Use an Nginx image to serve the built application
FROM nginx:alpine

# Copy the built application to the Nginx web root
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
>>>>>>> c1ff09266e50a3e4698620158bc1be04963e8a2d
