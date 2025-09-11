#!/bin/bash

# ArrPy Release Script
# Automates the release process for new versions

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if version argument is provided
if [ $# -eq 0 ]; then
    print_error "No version number provided"
    echo "Usage: ./release.sh <version>"
    echo "Example: ./release.sh 1.0.1"
    exit 1
fi

VERSION=$1
BRANCH=$(git branch --show-current)

echo "======================================"
echo "ArrPy Release Process - Version $VERSION"
echo "======================================"
echo ""

# 1. Check current branch
print_status "Current branch: $BRANCH"
if [ "$BRANCH" != "main" ] && [ "$BRANCH" != "master" ]; then
    print_warning "Not on main branch. Continue? (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        exit 1
    fi
fi

# 2. Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    print_error "Uncommitted changes detected"
    git status --short
    echo "Please commit or stash changes before releasing"
    exit 1
fi
print_status "Working directory clean"

# 3. Pull latest changes
print_status "Pulling latest changes..."
git pull origin "$BRANCH"

# 4. Run tests
print_status "Running tests..."
if ! python -m pytest tests/ -v; then
    print_error "Tests failed! Fix issues before releasing"
    exit 1
fi
print_status "All tests passed"

# 5. Run linting
print_status "Running code quality checks..."
if command -v ruff &> /dev/null; then
    ruff check arrpy/ || true
fi
if command -v black &> /dev/null; then
    black --check arrpy/ || true
fi
print_status "Code quality checks complete"

# 6. Update version in files
print_status "Updating version to $VERSION..."

# Update pyproject.toml
sed -i.bak "s/version = \".*\"/version = \"$VERSION\"/" pyproject.toml && rm pyproject.toml.bak

# Update setup.py
sed -i.bak "s/version=\".*\"/version=\"$VERSION\"/" setup.py && rm setup.py.bak

# Update arrpy/__init__.py or version.py
if [ -f "arrpy/version.py" ]; then
    sed -i.bak "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" arrpy/version.py && rm arrpy/version.py.bak
elif [ -f "arrpy/__init__.py" ]; then
    sed -i.bak "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" arrpy/__init__.py && rm arrpy/__init__.py.bak
fi

print_status "Version updated in all files"

# 7. Update CHANGELOG
print_status "Updating CHANGELOG..."
DATE=$(date +%Y-%m-%d)
sed -i.bak "s/## \[Unreleased\]/## [$VERSION] - $DATE/" CHANGELOG.md && rm CHANGELOG.md.bak
print_warning "Please review and update CHANGELOG.md manually if needed"

# 8. Build distributions
print_status "Building distribution packages..."
rm -rf dist/ build/ *.egg-info
python -m build
print_status "Distribution packages built"

# 9. Create git commit and tag
print_status "Creating git commit and tag..."
git add -A
git commit -m "Release version $VERSION

- Updated version in package files
- Updated CHANGELOG.md
- Built distribution packages"

git tag -a "v$VERSION" -m "Release version $VERSION"
print_status "Git commit and tag created"

# 10. Build documentation
if [ -d "docs" ]; then
    print_status "Building documentation..."
    cd docs && make clean && make html && cd ..
    print_status "Documentation built"
fi

# 11. Run final checks
print_status "Running final checks..."
python -c "import arrpy; print(f'ArrPy version: {arrpy.__version__}')"

# 12. Display next steps
echo ""
echo "======================================"
echo "Release preparation complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Review the changes:"
echo "   git show HEAD"
echo ""
echo "2. Push to GitHub:"
echo "   git push origin $BRANCH"
echo "   git push origin v$VERSION"
echo ""
echo "3. Upload to PyPI (test):"
echo "   python -m twine upload --repository testpypi dist/*"
echo ""
echo "4. Test installation from TestPyPI:"
echo "   pip install --index-url https://test.pypi.org/simple/ arrpy==$VERSION"
echo ""
echo "5. Upload to PyPI (production):"
echo "   python -m twine upload dist/*"
echo ""
echo "6. Create GitHub release:"
echo "   - Go to https://github.com/yourusername/arrpy/releases"
echo "   - Click 'Create a new release'"
echo "   - Select tag v$VERSION"
echo "   - Add release notes from CHANGELOG.md"
echo "   - Upload dist/* files as release assets"
echo ""
echo "7. Update documentation:"
echo "   - Deploy docs to Read the Docs or GitHub Pages"
echo ""
echo "8. Announce the release:"
echo "   - Update project website"
echo "   - Post on social media"
echo "   - Notify users via mailing list"
echo ""
print_status "Good luck with the release!"