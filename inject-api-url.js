/**
 * Script to inject API URL into HTML files at build time
 * This is used by Vercel to set the API URL from environment variables
 */

const fs = require('fs');
const path = require('path');

const API_URL = process.env.NEXT_PUBLIC_API_URL || process.env.API_URL || 'http://127.0.0.1:8000';

console.log(`🔧 Injecting API URL: ${API_URL}`);

// List of HTML files to update
const htmlFiles = [
  'index.html',
  'login-fixed.html',
  'login.html',
  'election-registration.html',
  'personal-portal.html',
  'student-verification.html',
  'signup-complete.html',
  'admin-dashboard-enhanced.html',
  'admin-dashboard.html',
  'portal.html',
  'register.html',
  'verify.html',
];

// Determine frontend directory
// If running from project root, use frontend/ subdirectory
// If running from frontend directory, use current directory
const frontendDir = fs.existsSync(path.join(__dirname, 'frontend', 'index.html'))
  ? path.join(__dirname, 'frontend')
  : __dirname;

console.log(`📁 Frontend directory: ${frontendDir}`);

htmlFiles.forEach(file => {
  const filePath = path.join(frontendDir, file);
  
  if (!fs.existsSync(filePath)) {
    console.log(`⚠️  File not found: ${file}`);
    return;
  }
  
  let content = fs.readFileSync(filePath, 'utf8');
  
  // Add or update data-api-url attribute on html tag
  if (content.includes('<html')) {
    // Remove existing data-api-url if present
    content = content.replace(/\s*data-api-url="[^"]*"/g, '');
    // Add new data-api-url attribute
    content = content.replace(
      /<html([^>]*)>/,
      `<html$1 data-api-url="${API_URL}">`
    );
  }
  
  fs.writeFileSync(filePath, content, 'utf8');
  console.log(`✅ Updated: ${file}`);
});

console.log('✨ API URL injection complete!');

