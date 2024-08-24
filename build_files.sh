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

# Install setuptools, which includes the functionality of distutils
echo "Installing setuptools..."
$pip_cmd install setuptools || { echo "Failed to install setuptools"; exit 1; }

# Install dependencies
echo "Installing dependencies..."
$pip_cmd install -r requirements.txt || { echo "Dependency installation failed"; exit 1; }

# Verify Django installation
echo "Verifying Django installation..."
python3 -m django --version || { echo "Django is not installed"; exit 1; }
# Install or upgrade django-environ
$pip_cmd install --upgrade django-environ || { echo "Failed to install/upgrade django-environ"; exit 1; }

echo "django-environ upgraded successfully."


# Run database migrations
echo "Running database migrations..."
python3 manage.py makemigrations || { echo "Makemigrations failed"; exit 1; }
python3 manage.py migrate || { echo "Migration failed"; exit 1; }

# Set the STATIC_ROOT directory to match Vercel's expected output
export STATIC_ROOT=staticfiles_build

# Create the output directory
mkdir -p $STATIC_ROOT
chmod -R 755 $STATIC_ROOT

# Ensure the static directory exists
mkdir -p /vercel/path0/static
chmod -R 755 /vercel/path0/static
# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput || { echo "Static files collection failed"; exit 1; }

echo "Build process completed successfully."
