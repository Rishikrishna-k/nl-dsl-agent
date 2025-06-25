@echo off
REM DSL Code Generator Docker Test Script for Windows

echo 🧪 Testing DSL Code Generator Docker Container...

REM Check if container is running
docker ps | findstr dsl-codegen >nul
if %errorlevel% neq 0 (
    echo ❌ Error: DSL Code Generator container is not running!
    echo Please start it first with: scripts\docker-build.bat
    pause
    exit /b 1
)

echo ✅ Container is running!

REM Wait for container to be ready
echo ⏳ Waiting for container to be ready...
timeout /t 10 /nobreak >nul

REM Test health endpoint
echo 🏥 Testing health endpoint...
curl -f http://localhost:8003/health >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Health check failed!
    pause
    exit /b 1
)
echo ✅ Health check passed!

REM Test the main endpoint
echo 🧪 Testing DSL generation endpoint...
curl -s -X GET http://localhost:8003/test > temp_response.json
if %errorlevel% neq 0 (
    echo ❌ DSL generation test failed!
    pause
    exit /b 1
)

echo ✅ DSL generation test passed!
echo.
echo 📋 Test Response:
type temp_response.json
del temp_response.json

echo.
echo 🎉 All tests passed! Your DSL Code Generator is working correctly.
echo.
echo 🌐 API Endpoints:
echo   Health: http://localhost:8003/health
echo   Test: http://localhost:8003/test
echo   Generate: POST http://localhost:8003/generate
echo.
echo 📝 Example curl command:
echo curl -X POST "http://localhost:8003/generate" ^
echo      -H "Content-Type: application/json" ^
echo      -d "{\"query\": \"Create a DSL rule to validate insurance coverage\"}"
echo.
pause 