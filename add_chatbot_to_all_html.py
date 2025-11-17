#!/usr/bin/env python3
"""
Script to add chatbot, Instagram, and Facebook buttons to all HTML files
"""
import os
import re

# CSS to add
CSS_STYLES = """    <!-- Floating Buttons & Chatbot Styles -->
    <style>
        /* Floating Buttons Container */
        .floating-buttons {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 15px;
            align-items: flex-end;
        }

        /* Floating Button Base Styles */
        .floating-btn {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            text-decoration: none;
            position: relative;
        }

        .floating-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }

        /* Chatbot Button */
        .chatbot-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .chatbot-btn:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }

        .chatbot-badge {
            position: absolute;
            top: -5px;
            right: -5px;
            background: #ff4444;
            color: #fff;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
            border: 2px solid #fff;
        }

        /* Instagram Button */
        .instagram-btn {
            background: linear-gradient(135deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
            transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }

        .instagram-btn:hover {
            opacity: 0.9;
        }

        /* Facebook Button */
        .facebook-btn {
            background: #1877f2;
            transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }

        .facebook-btn:hover {
            background: #166fe5;
        }

        /* When chatbot is active, move social buttons back */
        .floating-buttons.chatbot-active .instagram-btn,
        .floating-buttons.chatbot-active .facebook-btn {
            transform: translateY(540px) scale(0.8);
            opacity: 0.2;
            pointer-events: none;
        }

        /* Chatbot Widget */
        .chatbot-widget {
            position: fixed;
            bottom: 110px;
            right: 30px;
            width: 380px;
            max-width: calc(100vw - 60px);
            height: 500px;
            max-height: calc(100vh - 140px);
            background: #fff;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            display: none;
            flex-direction: column;
            z-index: 9998;
            overflow: hidden;
        }

        .chatbot-widget.active {
            display: flex;
            animation: slideUp 0.3s ease;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Chatbot Header */
        .chatbot-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .chatbot-header-content h4 {
            margin: 0;
            font-size: 18px;
            font-weight: 600;
        }

        .chatbot-header-content p {
            margin: 5px 0 0 0;
            font-size: 13px;
            opacity: 0.9;
        }

        .chatbot-close {
            background: transparent;
            border: none;
            color: #fff;
            font-size: 20px;
            cursor: pointer;
            padding: 5px;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: background 0.3s ease;
        }

        .chatbot-close:hover {
            background: rgba(255, 255, 255, 0.2);
        }

        /* Chatbot Body */
        .chatbot-body {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f5f5f5;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .chatbot-body::-webkit-scrollbar {
            width: 6px;
        }

        .chatbot-body::-webkit-scrollbar-track {
            background: #f1f1f1;
        }

        .chatbot-body::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 3px;
        }

        .chatbot-body::-webkit-scrollbar-thumb:hover {
            background: #555;
        }

        /* Chatbot Messages */
        .chatbot-message {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 18px;
            word-wrap: break-word;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(5px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .bot-message {
            background: #fff;
            align-self: flex-start;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .user-message {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            align-self: flex-end;
        }

        .chatbot-message p {
            margin: 0;
            font-size: 14px;
            line-height: 1.5;
        }

        /* Chatbot Input */
        .chatbot-input {
            padding: 15px;
            background: #fff;
            border-top: 1px solid #e0e0e0;
            display: flex;
            gap: 10px;
        }

        .chatbot-input input {
            flex: 1;
            padding: 12px 15px;
            border: 1px solid #e0e0e0;
            border-radius: 25px;
            outline: none;
            font-size: 14px;
        }

        .chatbot-input input:focus {
            border-color: #667eea;
        }

        .chatbot-input button {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            border: none;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s ease;
        }

        .chatbot-input button:hover {
            transform: scale(1.1);
        }

        /* Quick Actions */
        .quick-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }

        .quick-action-btn {
            padding: 8px 15px;
            background: #fff;
            border: 1px solid #e0e0e0;
            border-radius: 20px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .quick-action-btn:hover {
            background: #667eea;
            color: #fff;
            border-color: #667eea;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .floating-buttons {
                bottom: 20px;
                right: 20px;
                gap: 12px;
            }

            .floating-btn {
                width: 55px;
                height: 55px;
                font-size: 20px;
            }

            .chatbot-widget {
                bottom: 90px;
                right: 20px;
                width: calc(100vw - 40px);
                height: calc(100vh - 120px);
            }

            /* Adjust translateY for mobile when chatbot is active */
            .floating-buttons.chatbot-active .instagram-btn,
            .floating-buttons.chatbot-active .facebook-btn {
                transform: translateY(calc(100vh - 150px));
            }
        }
    </style>
"""

# HTML to add before footer
HTML_CONTENT = """    <!-- Floating Social & Chat Buttons Start -->
    <div class="floating-buttons">
        <!-- Chatbot Button -->
        <button class="floating-btn chatbot-btn" id="chatbotBtn" title="Chat with us">
            <i class="fa-solid fa-comments"></i>
            <span class="chatbot-badge">1</span>
        </button>
        
        <!-- Instagram Button -->
        <a href="https://www.instagram.com/dr_nitin_sapat/" target="_blank" class="floating-btn instagram-btn" title="Follow us on Instagram">
            <i class="fa-brands fa-instagram"></i>
        </a>
        
        <!-- Facebook Button -->
        <a href="https://www.facebook.com/shrisaimultispecialitydental/" target="_blank" class="floating-btn facebook-btn" title="Like us on Facebook">
            <i class="fa-brands fa-facebook-f"></i>
        </a>
    </div>

    <!-- Chatbot Widget Start -->
    <div class="chatbot-widget" id="chatbotWidget">
        <div class="chatbot-header">
            <div class="chatbot-header-content">
                <h4>Shri Sai Dental Clinic</h4>
                <p>We're here to help!</p>
            </div>
            <button class="chatbot-close" id="chatbotClose">
                <i class="fa-solid fa-times"></i>
            </button>
        </div>
        <div class="chatbot-body" id="chatbotBody">
            <div class="chatbot-message bot-message">
                <p>Hello! 👋 Welcome to Shri Sai Dental Clinic. How can we help you today?</p>
            </div>
        </div>
        <div class="chatbot-input">
            <input type="text" id="chatbotInput" placeholder="Type your message...">
            <button id="chatbotSend">
                <i class="fa-solid fa-paper-plane"></i>
            </button>
        </div>
    </div>
    <!-- Chatbot Widget End -->
    <!-- Floating Social & Chat Buttons End -->
"""

# JavaScript to add before </body>
JS_CONTENT = """    
    <!-- Floating Buttons & Chatbot JavaScript -->
    <script>
        // Chatbot functionality
        document.addEventListener('DOMContentLoaded', function() {
            const chatbotBtn = document.getElementById('chatbotBtn');
            const chatbotWidget = document.getElementById('chatbotWidget');
            const chatbotClose = document.getElementById('chatbotClose');
            const chatbotBody = document.getElementById('chatbotBody');
            const chatbotInput = document.getElementById('chatbotInput');
            const chatbotSend = document.getElementById('chatbotSend');
            const chatbotBadge = document.querySelector('.chatbot-badge');
            const floatingButtons = document.querySelector('.floating-buttons');

            // Toggle chatbot widget
            chatbotBtn.addEventListener('click', function() {
                chatbotWidget.classList.toggle('active');
                if (chatbotWidget.classList.contains('active')) {
                    chatbotBadge.style.display = 'none';
                    chatbotInput.focus();
                    floatingButtons.classList.add('chatbot-active');
                } else {
                    floatingButtons.classList.remove('chatbot-active');
                }
            });

            // Close chatbot widget
            chatbotClose.addEventListener('click', function() {
                chatbotWidget.classList.remove('active');
                floatingButtons.classList.remove('chatbot-active');
            });

            // Send message function
            function sendMessage() {
                const message = chatbotInput.value.trim();
                if (message === '') return;
                addMessage(message, 'user');
                chatbotInput.value = '';
                setTimeout(() => {
                    const botResponse = getBotResponse(message);
                    addMessage(botResponse, 'bot');
                }, 500);
            }

            chatbotSend.addEventListener('click', sendMessage);
            chatbotInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            function addMessage(text, type) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `chatbot-message ${type}-message`;
                const formattedText = text.replace(/\\n/g, '<br>');
                messageDiv.innerHTML = `<p>${formattedText}</p>`;
                chatbotBody.appendChild(messageDiv);
                chatbotBody.scrollTop = chatbotBody.scrollHeight;
            }

            function getBotResponse(userMessage) {
                const message = userMessage.toLowerCase();
                if (message.includes('hi') || message.includes('hello') || message.includes('hey')) {
                    return 'Hello! 👋 Thank you for contacting Shri Sai Dental Clinic. How can I help you today?';
                }
                if (message.includes('appointment') || message.includes('book') || message.includes('schedule')) {
                    return 'To book an appointment, please call us at 9226807779 or 9999999999. Our clinic timings are: Mon-Sat: 10 AM - 2 PM & 5 PM - 9 PM, Sun: 10 AM - 2 PM.';
                }
                if (message.includes('service') || message.includes('treatment') || message.includes('what do you offer')) {
                    return 'We offer a wide range of services including:\\n• Braces & Clear Aligners\\n• Root Canal Treatment\\n• Dental Implants\\n• Cosmetic Dentistry\\n• Preventive Care\\n• And much more!';
                }
                if (message.includes('location') || message.includes('address') || message.includes('where')) {
                    return 'We are located at: Shop No.10, Chowrang Residency, Satavwadi, Hadapsar, Pune - 411028. You can also check our location on Google Maps.';
                }
                if (message.includes('time') || message.includes('hours') || message.includes('open') || message.includes('closed')) {
                    return 'Our clinic timings are:\\nMonday to Saturday: 10:00 AM - 2:00 PM & 5:00 PM - 9:00 PM\\nSunday: 10:00 AM - 2:00 PM';
                }
                if (message.includes('price') || message.includes('cost') || message.includes('charge') || message.includes('fee')) {
                    return 'Pricing varies based on the treatment. For accurate pricing information, please call us at 9226807779 or visit our clinic for a consultation. We offer transparent pricing with no hidden charges.';
                }
                if (message.includes('emergency') || message.includes('urgent') || message.includes('pain')) {
                    return 'For dental emergencies, please call us immediately at 9226807779. We prioritize emergency cases and will do our best to accommodate you.';
                }
                if (message.includes('contact') || message.includes('phone') || message.includes('number') || message.includes('call')) {
                    return 'You can reach us at:\\n📞 Phone: 9226807779   \\n📧 Email: info@drnitinsapat.in\\n📍 Address: Shop No.10, Chowrang Residency, Satavwadi, Hadapsar, Pune - 411028';
                }
                return 'Thank you for your message! For more specific information, please call us at 9226807779 or visit our clinic. Our team is here to help with all your dental needs. 😊';
            }

            setTimeout(() => {
                const quickActions = document.createElement('div');
                quickActions.className = 'quick-actions';
                quickActions.innerHTML = `
                    <button class="quick-action-btn" onclick="quickAction('appointment')">Book Appointment</button>
                    <button class="quick-action-btn" onclick="quickAction('services')">Our Services</button>
                    <button class="quick-action-btn" onclick="quickAction('location')">Location</button>
                    <button class="quick-action-btn" onclick="quickAction('contact')">Contact Info</button>
                `;
                chatbotBody.appendChild(quickActions);
            }, 1000);

            window.quickAction = function(action) {
                let message = '';
                switch(action) {
                    case 'appointment': message = 'I want to book an appointment'; break;
                    case 'services': message = 'What services do you offer?'; break;
                    case 'location': message = 'Where are you located?'; break;
                    case 'contact': message = 'What is your contact number?'; break;
                }
                chatbotInput.value = message;
                sendMessage();
            };
        });
    </script>
"""

def process_file(filepath):
    """Process a single HTML file to add chatbot functionality"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already processed
        if 'floating-buttons' in content:
            print(f"  ⚠️  {filepath} already has chatbot - skipping")
            return False
        
        # Add CSS before </head>
        if '</head>' in content and CSS_STYLES not in content:
            content = content.replace('</head>', CSS_STYLES + '\n</head>', 1)
        
        # Add HTML before Footer
        footer_patterns = [
            r'(<!-- Footer Start -->)',
            r'(<footer class="main-footer">)',
            r'(        <!-- Footer Start -->)',
        ]
        html_added = False
        for pattern in footer_patterns:
            if re.search(pattern, content) and HTML_CONTENT not in content:
                content = re.sub(pattern, HTML_CONTENT + r'\n\n    ' + r'\1', content, count=1)
                html_added = True
                break
        
        # Add JavaScript before </body>
        if '</body>' in content and JS_CONTENT not in content:
            content = content.replace('</body>', JS_CONTENT + '\n</body>', 1)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ {filepath} - processed successfully")
        return True
    except Exception as e:
        print(f"  ❌ {filepath} - Error: {str(e)}")
        return False

def main():
    """Main function to process all HTML files"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_files = [f for f in os.listdir(current_dir) 
                  if f.endswith('.html') and f != 'index.html']
    
    print(f"Found {len(html_files)} HTML files to process (excluding index.html)")
    print("Processing files...\n")
    
    processed = 0
    for html_file in sorted(html_files):
        filepath = os.path.join(current_dir, html_file)
        if process_file(filepath):
            processed += 1
    
    print(f"\n✅ Completed! Processed {processed} files.")
    print(f"📝 Note: index.html, contact.html, and about.html were already processed manually.")

if __name__ == '__main__':
    main()

