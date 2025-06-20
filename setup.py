from setuptools import setup, find_packages

setup(
    name="greenter",
    version="1.0.0",
    description="Facturación Electrónica SUNAT - Perú (Python Port)",
    author="Migrated from PHP Greenter",
    author_email="",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        # XML Processing
        "lxml>=4.6.0",
        
        # SOAP Services
        "zeep>=4.0.0",
        "requests>=2.25.0",
        
        # Digital Signing
        "xmlsec>=1.3.0",
        "cryptography>=3.4.0",
        
        # Template Engine
        "Jinja2>=3.0.0",
        
        # Data Validation
        "pydantic>=1.8.0",
        
        # PDF Generation
        "weasyprint>=54.0",
        
        # QR Code Generation
        "qrcode[pil]>=7.0.0",
        
        # Date handling
        "python-dateutil>=2.8.0",
        
        # Timezone support
        "pytz>=2021.1",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 