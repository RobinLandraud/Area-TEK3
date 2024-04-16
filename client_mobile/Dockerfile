FROM openjdk:8-jdk

ENV CLIENT_MOBILE_HOME /home/app/client_mobile
RUN mkdir -p $CLIENT_MOBILE_HOME
WORKDIR $CLIENT_MOBILE_HOME

ENV NODE_ENV development

COPY . $CLIENT_MOBILE_HOME

ENV ANDROID_HOME /opt/android-sdk-linux
ENV PATH $PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

# Install Gradle
RUN apt-get update && apt-get install -y wget
RUN mkdir -p /opt/gradle
RUN cd /opt/gradle && wget https://services.gradle.org/distributions/gradle-6.8.3-bin.zip
RUN cd /opt/gradle && unzip gradle-6.8.3-bin.zip
RUN cd /opt/gradle && rm gradle-6.8.3-bin.zip
RUN cd /opt/gradle && mv gradle-6.8.3 gradle
ENV GRADLE_HOME /opt/gradle/gradle
ENV PATH $PATH:/opt/gradle/gradle/bin

# Install tree
RUN apt-get install -y tree

# Install Android SDK
RUN mkdir -p /opt/android-sdk-linux
RUN cd /opt/android-sdk-linux && wget https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip
RUN cd /opt/android-sdk-linux && unzip sdk-tools-linux-4333796.zip
RUN cd /opt/android-sdk-linux && rm sdk-tools-linux-4333796.zip
RUN cd /opt/android-sdk-linux && yes | tools/bin/sdkmanager --licenses
RUN cd /opt/android-sdk-linux && tools/bin/sdkmanager "platform-tools" "platforms;android-30" "build-tools;30.0.2"

# Install Node.js dependencies
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs
RUN npm install
RUN npm install -i -g --force react-native-cli

# Set paths
ENV PATH $PATH:/opt/apache-maven-3.6.3/bin:/opt/android-sdk-linux/tools:/opt/android-sdk-linux/platform-tools

# Create local.properties file
RUN mkdir -p android
RUN echo "sdk.dir=$ANDROID_HOME" > android/local.properties

# Bundle the app
RUN npx mkdirp android/app/src/main/assets/ && react-native bundle \
        --dev false \
        --platform android \
        --entry-file App.js \
        --bundle-output ./android/app/src/main/assets/index.android.bundle \
        --assets-dest ./android/app/src/main/res

# Build the app apk
RUN cd android && gradle init && gradle wrapper

# Create the missing build.gradle file
RUN cp ./android/build.gradle ./android/app/build.gradle

RUN echo "// Top-level build.gradle" >> android/build.gradle \
    && echo "" >> android/build.gradle \
    && echo "buildscript {" >> android/build.gradle \
    && echo "    repositories {" >> android/build.gradle \
    && echo "        google() // add Google's Maven repository" >> android/build.gradle \
    && echo "        jcenter()" >> android/build.gradle \
    && echo "    }" >> android/build.gradle \
    && echo "    dependencies {" >> android/build.gradle \
    && echo "        classpath 'com.android.tools.build::4.1.3' // use the version of the plugin that matches your project" >> android/build.gradle \
    && echo "    }" >> android/build.gradle \
    && echo "}" >> android/build.gradle \
    && echo "" >> android/build.gradle \
    && echo "allprojects {" >> android/build.gradle \
    && echo "    repositories {" >> android/build.gradle \
    && echo "        google() // add Google's Maven repository" >> android/build.gradle \
    && echo "        jcenter()" >> android/build.gradle \
    && echo "    }" >> android/build.gradle \
    && echo "}" >> android/build.gradle \
    && echo "" >> android/build.gradle \
    && echo "task clean(type: Delete) {" >> android/build.gradle \
    && echo "    delete rootProject.buildDir" >> android/build.gradle \
    && echo "}" >> android/build.gradle

RUN echo "apply plugin: 'com.android.application'" > android/app/build.gradle \
    && echo " " >> android/app/build.gradle \
    && echo "android {" >> android/app/build.gradle \
    && echo "    compileSdkVersion 30" >> android/app/build.gradle \
    && echo "    buildToolsVersion \"30.0.2\"" >> android/app/build.gradle \
    && echo " " >> android/app/build.gradle \
    && echo "    defaultConfig {" >> android/app/build.gradle \
    && echo "        applicationId \"com.example.myapp\"" >> android/app/build.gradle \
    && echo "        minSdkVersion 21" >> android/app/build.gradle \
    && echo "        targetSdkVersion 30" >> android/app/build.gradle \
    && echo "        versionCode 1" >> android/app/build.gradle \
    && echo "        versionName \"1.0\"" >> android/app/build.gradle \
    && echo "        testInstrumentationRunner \"androidx.test.runner.AndroidJUnitRunner\"" >> android/app/build.gradle \
    && echo "    }" >> android/app/build.gradle \
    && echo " " >> android/app/build.gradle \
    && echo "    buildTypes {" >> android/app/build.gradle \
    && echo "        debug {" >> android/app/build.gradle \
    && echo "            minifyEnabled false" >> android/app/build.gradle \
    && echo "            debuggable true" >> android/app/build.gradle \
    && echo "        }" >> android/app/build.gradle \
    && echo "    }" >> android/app/build.gradle \
    && echo "}" >> android/app/build.gradle \
    && echo " " >> android/app/build.gradle \
    && echo "task assembleDebug(type: GradleBuild) {" >> android/app/build.gradle \
    && echo "    tasks = ['assembleDebug']" >> android/app/build.gradle \
    && echo "}" >> android/app/build.gradle \
    && echo " " >> android/app/build.gradle \
    && echo "dependencies {" >> android/app/build.gradle \
    && echo "    implementation fileTree(dir: 'libs', include: ['*.jar'])" >> android/app/build.gradle \
    && echo "    implementation 'androidx.appcompat:appcompat:1.3.0'" >> android/app/build.gradle \
    && echo "    implementation 'com.google.android.material:material:1.3.0'" >> android/app/build.gradle \
    && echo "    implementation 'androidx.constraintlayout:constraintlayout:2.0.4'" >> android/app/build.gradle \
    && echo "    testImplementation 'junit:junit:4.+'" >> android/app/build.gradle \
    && echo "    androidTestImplementation 'androidx.test.ext:junit:1.1.3'" >> android/app/build.gradle \
    && echo "    androidTestImplementation 'androidx.test.espresso:espresso-core:3.4.0'" >> android/app/build.gradle \
    && echo "}" >> android/app/build.gradle

RUN cd android && cat build.gradle && ./gradlew assembleDebug