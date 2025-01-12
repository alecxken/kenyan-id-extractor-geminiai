# Kenyan ID Information Extractor

🔍 A powerful Flask API that leverages Google's Gemini AI to automatically extract information from Kenyan identification documents. Built with production-ready features including Nginx deployment, automated CI/CD, and secure API key management.

## 🌟 Repository Description

An intelligent document processing API that uses Google's Gemini AI to extract structured information from Kenyan ID images. Perfect for organizations needing to automate ID verification and data extraction. Features automated cloud deployment, secure API key management, and production-ready configuration.

## README.md

# 🎯 Kenyan ID Information Extractor

[![Deploy to Production](https://github.com/alecxken/kenyan-id-extractor-geminiai/actions/workflows/deploy.yml/badge.svg)](https://github.com/alecxken/kenyan-id-extractor-geminiai/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Extract structured information from Kenyan identification documents using Google's Gemini AI model. This production-ready Flask API includes automated deployment, secure key management, and enterprise-grade infrastructure setup.

## ✨ Features

- 🤖 Powered by Google's Gemini AI for accurate information extraction
- 🔒 Secure API key management via environment variables
- 🚀 Production-ready with Nginx and Gunicorn setup
- ⚡ Automated deployment using GitHub Actions
- 📝 Structured JSON output for easy integration
- 🛡️ Built-in security features and rate limiting

## 🔧 Technologies Used

- Flask (Web Framework)
- Google Gemini AI (Machine Learning Model)
- Nginx (Reverse Proxy)
- Gunicorn (WSGI Server)
- GitHub Actions (CI/CD)
- Docker (Containerization)

## 📋 Information Extracted

The API extracts the following information from Kenyan IDs:
- Serial Number
- Full Names
- Date of Birth
- Sex
- District of Birth
- Place of Issue
- Date of Issue
- Country (Fixed as "REPUBLIC OF KENYA")

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/alecxken/kenyan-id-extractor-geminiai.git
cd kenyan-id-extractor
```

2. **Set up environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure API key**
```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

4. **Run locally**
```bash
python main.py
```

## 🔌 API Endpoints

### Set Gemini API Key
```http
POST /set_api_key
Content-Type: application/json

{
    "api_key": "your-gemini-api-key"
}
```

### Process Image
```http
POST /process_image
Content-Type: multipart/form-data

file: <image_file>
```

Example Response:
```json
{
    "text_response": {
        "relevant_info": {
            "serial_number": "12345678",
            "full_names": "JOHN DOE SMITH",
            "date_of_birth": "01-01-1990",
            "sex": "M",
            "district_of_birth": "NAIROBI",
            "place_of_issue": "NAIROBI",
            "date_of_issue": "01-01-2020",
            "country": "REPUBLIC OF KENYA"
        }
    }
}
```

## 🚢 Deployment

### Automated Deployment
1. Configure GitHub Secrets:
   - `SSH_PRIVATE_KEY`
   - `VM_HOST`
   - `VM_USER`
   - `DEPLOY_PATH`

2. Push to main branch to trigger deployment:
```bash
git push origin main
```

### Manual Deployment
1. SSH into your server
```bash
ssh username@your-server-ip
```

2. Run setup script
```bash
./scripts/setup.sh
```

3. Deploy application
```bash
./scripts/deploy.sh
```

## 🛡️ Security Features

- Environment-based configuration
- API key validation
- Rate limiting
- SSL/TLS support
- Input validation
- Error handling

## 📈 Performance Optimization

- Nginx caching
- Gunicorn worker optimization
- Request pooling
- Response compression

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI team for the powerful ML model
- Flask community for the excellent web framework
- All contributors who help improve this project

## 📧 Contact

Your Name - alecxkendagor@gmail.com

Project Link: [https://github.com/alecxken/kenyan-id-extractor-geminiai](https://github.com/alecxken/kenyan-id-extractor-geminiai)

---
⭐️ Star this repo if you find it useful!