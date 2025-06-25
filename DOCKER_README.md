# 🐳 DSL Code Generator - Docker Setup

This guide will help you set up and run the DSL Code Generator using Docker.

## 📋 Prerequisites

1. **Docker Desktop** installed and running
2. **Docker Compose** (usually included with Docker Desktop)
3. **OpenRouter API Key** in your `.env` file

## 🚀 Quick Start

### 1. Prepare Your Environment

Create a `.env` file in the project root:
```bash
OPENROUTER_API_KEY=your-openrouter-api-key-here
LLM_MODEL=deepseek-chat
DEBUG=false
```

### 2. Build and Run (Windows)

```bash
# Run the build script
scripts\docker-build.bat
```

### 3. Build and Run (Linux/Mac)

```bash
# Make scripts executable
chmod +x scripts/docker-build.sh scripts/docker-test.sh

# Run the build script
./scripts/docker-build.sh
```

### 4. Test the Container

```bash
# Windows
scripts\docker-test.bat

# Linux/Mac
./scripts/docker-test.sh
```

## 🌐 API Endpoints

Once running, your API will be available at:

- **Health Check**: http://localhost:8001/health
- **Test Endpoint**: http://localhost:8001/test
- **Generate DSL**: POST http://localhost:8001/generate

## 📝 Example Usage

### Test the API
```bash
curl -X GET http://localhost:8001/test
```

### Generate DSL Code
```bash
curl -X POST "http://localhost:8001/generate" \
     -H "Content-Type: application/json" \
     -d '{"query": "Create a DSL rule to validate insurance coverage"}'
```

## 🛠️ Docker Commands

### Basic Operations
```bash
# Start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down

# Restart the container
docker-compose restart
```

### Development Mode
```bash
# Start with hot reload (for development)
docker-compose --profile dev up -d
```

### Container Management
```bash
# View running containers
docker ps

# View container logs
docker logs dsl-codegen

# Execute commands in container
docker exec -it dsl-codegen bash

# Remove container and image
docker-compose down --rmi all
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | Required |
| `LLM_MODEL` | Model to use (e.g., deepseek-chat) | deepseek-chat |
| `DEBUG` | Enable debug mode | false |

### Volumes

The container mounts these directories:
- `./examples` → `/app/examples` (read-only)
- `./grammars` → `/app/grammars` (read-only)
- `./logs` → `/app/logs` (read-write)

### Ports

- **Production**: Port 8001 (avoids conflict with Django on 8000)
- **Development**: Port 8002 (with hot reload)

## 🐛 Troubleshooting

### Container Won't Start
1. Check if Docker Desktop is running
2. Verify your `.env` file exists and has the correct API key
3. Check logs: `docker-compose logs`

### API Key Issues
1. Ensure your OpenRouter API key is valid
2. Check the key in your `.env` file
3. Restart the container after changing `.env`

### Port Already in Use
If port 8001 is busy, change it in `docker-compose.yml`:
```yaml
ports:
  - "8003:8000"  # Use port 8003 instead
```

### Permission Issues (Linux/Mac)
```