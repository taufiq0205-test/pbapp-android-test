FROM python:3.12

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    curl \
    unzip \
    nodejs \
    npm \
    git \
    openjdk-17-jdk \
    libgl1 \
    libpulse0 \
    && rm -rf /var/lib/apt/lists/*

# Android SDK setup
ENV ANDROID_HOME /opt/android-sdk
ENV ANDROID_SDK_ROOT ${ANDROID_HOME}
ENV PATH ${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools

# Install Android Command Line Tools
RUN mkdir -p ${ANDROID_HOME}/cmdline-tools && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O /tmp/cmdline-tools.zip && \
    unzip /tmp/cmdline-tools.zip -d ${ANDROID_HOME}/cmdline-tools && \
    mv ${ANDROID_HOME}/cmdline-tools/cmdline-tools ${ANDROID_HOME}/cmdline-tools/latest && \
    rm /tmp/cmdline-tools.zip

# Install Android components
RUN yes | sdkmanager --licenses && \
    sdkmanager "platform-tools" "emulator" "platforms;android-33" "build-tools;33.0.2" "system-images;android-33;google_apis;x86_64"

# Appium setup
RUN npm install -g appium
RUN appium driver install uiautomator2
RUN appium plugin install --source=npm appium-dashboard

# Add after Appium installation
RUN npm install -g allure-commandline --unsafe-perm=true
ENV PATH=$PATH:/usr/local/lib/node_modules/allure-commandline/dist/bin

# Python environment
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy tests and entrypoint
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]