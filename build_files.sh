
#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting the build process..."

# Install Python (if not installed)
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found, installing..."
    apt-get update && apt-get install -y python3 python3-pip
else
    echo "Python3 is already installed."
fi


# Use pip3 if pip is not available
pip_cmd=$(command -v pip || command -v pip3)
echo "Using pip command: $pip_cmd"

# Install system-level dependencies
apk update
apk add libjpeg

# Install dependencies
echo "Installing dependencies..."
$pip_cmd install -r requirements.txt || { echo "Dependency installation failed"; exit 1; }
$pip_cmd install --upgrade -r requirements.txt

# Hard-code superuser credentials
SUPERUSER_USERNAME="linkan"
SUPERUSER_EMAIL="linkan@example.com"
SUPERUSER_PASSWORD="Linkan1@"
# Create the superuser
echo "Creating superuser..."
python3 manage.py shell -c "
from django.contrib.auth.models import User;
if not User.objects.filter(username='$SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')
" || { echo "Superuser creation failed"; exit 1; }

# Run database migrations
echo "Running database migrations..."
python3 manage.py makemigrations || { echo "Makemigrations failed"; exit 1; }
python3 manage.py migrate || { echo "Migration failed"; exit 1; }

# Set the STATIC_ROOT directory to match Vercel's expected output
export STATIC_ROOT=staticfiles_build

# Create the output directory
mkdir -p $STATIC_ROOT

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput || { echo "Static files collection failed"; exit 1; }

echo "Build process completed successfully."
