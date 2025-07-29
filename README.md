# Steganography Tool 🔐

A powerful GUI-based steganography application built in Python that allows you to hide and extract secret messages within images using LSB (Least Significant Bit) technique with optional encryption.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## 🚀 Features

- **User-Friendly GUI**: Clean and intuitive interface built with tkinter
- **LSB Steganography**: Uses Least Significant Bit technique for invisible message hiding
- **Password Protection**: Optional AES-128 encryption for added security
- **Multiple Image Formats**: Supports PNG, JPEG, BMP, TIFF formats
- **Image Preview**: Visual preview of selected images with fixed sizing
- **Scrollable Interface**: Responsive design that works with any screen size
- **Message Validation**: Automatic checks for message size compatibility
- **Cross-Platform**: Works on Windows, Linux, and macOS

## 📋 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Screenshots](#screenshots)
- [Requirements](#requirements)
- [Security Features](#security-features)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

## 🛠 Installation

### Prerequisites

Make sure you have Python 3.7 or higher installed on your system.

### Install Required Dependencies

```bash
pip install Pillow cryptography
```

### Download and Run

1. Clone or download the steganography tool
2. Save the code as `main.py`
3. Run the application:

```bash
python main.py
```

## 📖 Usage

### Hiding a Secret Message

1. **Select Image**: Click "Browse" to select a carrier image (PNG, JPEG, BMP, or TIFF)
2. **Enter Message**: Go to the "Hide Message" tab and type your secret message
3. **Add Password** (Optional): Enter a password for encryption
4. **Hide Message**: Click "Hide Message" to embed the text
5. **Save Image**: Click "Save Image" to save the steganographic image

### Extracting a Hidden Message

1. **Select Image**: Choose the image containing the hidden message
2. **Enter Password**: Go to "Extract Message" tab and enter the password (if used)
3. **Extract**: Click "Extract Message" to reveal the hidden text
4. **View Result**: The secret message will appear in the text area below

## 🔧 How It Works

### LSB Steganography Technique

The application uses the **Least Significant Bit (LSB)** method:

1. **Message Encoding**: 
   - Converts text message to binary representation
   - Optionally encrypts using Fernet (AES-128) with PBKDF2 key derivation
   - Adds delimiter markers to detect message boundaries

2. **Image Modification**:
   - Modifies the least significant bit of each RGB color channel
   - Distributes message bits across multiple pixels
   - Maintains visual imperceptibility of changes

3. **Message Extraction**:
   - Reads LSB from each pixel's RGB channels
   - Reconstructs binary message and converts to text
   - Decrypts using password if encryption was used

### Security Features

- **AES-128 Encryption**: Messages can be encrypted using Fernet symmetric encryption
- **PBKDF2 Key Derivation**: Passwords are strengthened using 100,000 iterations
- **Message Integrity**: End markers ensure complete message extraction
- **Visual Stealth**: LSB modification is virtually undetectable to human eye

## 📱 Screenshots

### Main Interface
```
┌─────────────────────────────────────────────────────────┐
│                 Steganography Tool                      │
├─────────────────────────────────────────────────────────┤
│ Image Selection                                         │
│ Select Image: [/path/to/image.png    ] [Browse]         │
├─────────────────────────────────────────────────────────┤
│ Image Preview                                           │
│              [   Image Preview   ]                      │
├─────────────────────────────────────────────────────────┤
│ [Hide Message] [Extract Message]                        │
│                                                         │
│ Secret Message:                                         │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Your secret message here...                         │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ Password (optional): [********]                         │
│                                                         │
│        [Hide Message]  [Save Image]                     │
└─────────────────────────────────────────────────────────┘
```

## ⚙️ Requirements

### System Requirements
- Python 3.7 or higher
- At least 100MB free disk space
- 4MB RAM minimum

### Python Dependencies
```
Pillow>=8.0.0
cryptography>=3.0.0
tkinter (usually included with Python)
```

### Supported Image Formats
- **Input**: PNG, JPEG, JPG, BMP, TIFF
- **Output**: PNG (recommended), JPEG
- **Recommended**: Use PNG for best quality preservation

## 🔒 Security Features

### Encryption Details
- **Algorithm**: AES-128 in CBC mode (via Fernet)
- **Key Derivation**: PBKDF2 with SHA-256
- **Salt**: Fixed salt (upgrade to random salt recommended for production)
- **Iterations**: 100,000 iterations for key strengthening

### Privacy Considerations
- Messages are embedded in image pixel data
- No metadata is added to image files
- Password-based encryption adds extra security layer
- Original image quality is preserved

## ⚠️ Limitations

### Technical Limitations
- **Message Size**: Limited by image resolution (1 character per 3 pixels approximately)
- **Image Quality**: JPEG compression may affect message integrity
- **File Size**: Steganographic images may be slightly larger due to format conversion

### Security Limitations
- **Visual Analysis**: Advanced steganalysis tools may detect hidden content
- **Password Security**: Use strong passwords for better protection
- **Salt Reuse**: Current implementation uses fixed salt (should be randomized)

### Compatibility
- **Format Loss**: Some metadata may be lost during image processing
- **Color Depth**: Works best with 24-bit RGB images
- **Transparency**: Alpha channels are preserved but not used for data hiding

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Bug Reports
- Use the issue tracker to report bugs
- Include Python version, OS, and error messages
- Provide sample images (without sensitive data)

### Feature Requests
- Suggest new features via issues
- Explain use cases and benefits
- Consider backward compatibility

### Code Contributions
1. Fork the repository
2. Create a feature branch
3. Follow PEP 8 style guidelines
4. Add tests for new functionality
5. Submit a pull request

### Suggested Improvements
- Random salt generation for encryption
- Support for additional image formats
- Batch processing capabilities
- Advanced steganalysis resistance
- GUI themes and customization

## 📄 License

This project is made for only the educational purpose.

## 📞 Support

### Getting Help
- Check the [Issues](https://github.com/shuvomdhar/steganography-tool/issues) page for common problems
- Review this README for usage instructions
- Test with sample images before using important data

### Troubleshooting

**Common Issues:**

1. **"Required module not found"**
   ```bash
   pip install Pillow cryptography
   ```

2. **"Message too long for this image"**
   - Use a larger image or shorter message
   - Rule of thumb: 1 character per 3 pixels

3. **"No hidden message found"**
   - Ensure the image contains a hidden message
   - Check if correct password was used
   - Verify image hasn't been compressed or modified

4. **Image quality issues**
   - Use PNG format for best results
   - Avoid JPEG for images with hidden messages

## 🎯 Use Cases

### Personal Security
- Secure communication in restrictive environments
- Password storage in innocent-looking images
- Personal diary entries hidden in photos

### Educational Purposes
- Learn about steganography and cryptography
- Demonstrate information security concepts
- Computer science projects and assignments

### Professional Applications
- Digital watermarking for copyright protection
- Covert communication channels
- Data integrity verification

---

**⚠️ Disclaimer**: This tool is for educational and legitimate use only. Users are responsible for complying with local laws and regulations regarding encryption and data hiding. The authors are not liable for any misuse of this software.

**🔐 Security Note**: While this tool provides basic steganography capabilities, it should not be considered cryptographically secure for high-stakes applications without additional security measures.