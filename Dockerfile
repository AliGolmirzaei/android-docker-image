FROM ubuntu:20.04

ENV ANDROID_HOME="/sdk"
ENV CMD_TOOL_VERSION=8512546
ENV ANDROID_COMPILE_SDK="30"
ENV ANDROID_BUILD_TOOLS="30.0.3"

ENV DEBIAN_FRONTEND=noninteractive

ENV PATH="$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/emulator:$ANDROID_HOME/platform-tools:/app"

RUN apt-get update \
    && apt-get install -y \
        wget \
        unzip \
        openjdk-11-jdk \
    && apt-get clean \
    && apt-get autoclean


RUN wget --quiet --output-document=cmdtools.zip https://dl.google.com/android/repository/commandlinetools-linux-${CMD_TOOL_VERSION}_latest.zip \
    && unzip -q -d cmdtools cmdtools.zip \
    && mkdir -p $ANDROID_HOME/cmdline-tools/latest/ \
    && mv cmdtools/cmdline-tools/* $ANDROID_HOME/cmdline-tools/latest/ \
    && rm -rf cmdtools cmdtools.zip

RUN yes | sdkmanager --licenses > /dev/null

RUN echo y | sdkmanager  "patcher;v4" \
    && echo y | sdkmanager  "platform-tools" \
    && echo y | sdkmanager  "build-tools;${ANDROID_BUILD_TOOLS}" \
    && echo y | sdkmanager  "platforms;android-${ANDROID_COMPILE_SDK}" \
    && echo y | sdkmanager  "emulator" \
    && echo y | sdkmanager  "system-images;android-${ANDROID_COMPILE_SDK};google_apis;x86_64" 

RUN echo no | avdmanager create avd -f -n testAVD -k "system-images;android-${ANDROID_COMPILE_SDK};google_apis;x86_64"

COPY ./start_emulator.sh /app/start_emulator.sh
RUN chmod +x /app/start_emulator.sh

