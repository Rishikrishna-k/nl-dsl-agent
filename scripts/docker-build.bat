@echo off
REM DSL Code Generator Docker Build Script for Windows

echo 🐳 Building DSL Code Generator Docker Container...

REM Check if .env file exists
if not exist .env (
    echo ❌ Error: .env file not found!
    echo Please create a .env file with your OpenRouter API key:
    echo OPENROUTER_API_KEY=your-api-key-here
    pause
    exit /b 1
)

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

REM Build the Docker image
echo 📦 Building Docker image...
docker build -t dsl-codegen:latest .

if %errorlevel% neq 0 (
    echo ❌ Docker build failed!
    pause
    exit /b 1
)

echo ✅ Docker image built successfully!

REM Run the container
echo 🚀 Starting DSL Code Generator container...
docker-compose up -d

if %errorlevel% neq 0 (
    echo ❌ Failed to start container!
    pause
    exit /b 1
)

echo ✅ Container started successfully!
echo.
echo 🌐 API is available at: http://localhost:8003
echo 📊 Health check: http://localhost:8003/health
echo 🧪 Test endpoint: http://localhost:8003/test
echo.
echo 📋 Useful commands:
echo   View logs: docker-compose logs -f
echo   Stop container: docker-compose down
echo   Restart container: docker-compose restart
echo   Development mode: docker-compose --profile dev up -d
echo.
pause 