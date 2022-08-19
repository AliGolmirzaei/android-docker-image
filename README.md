# Android docker image

This repository consists of scripts needed to build a docker image with an android emulator available for instrument tests. Right now a `.gitlab-ci.yml` is provided to build this image in Gitlab CICD. 

If you are also using Gitlab CICD you can use the following `.gitlab-ci.yml` to use the image build.
```
image: {path to your built image}

cache:
 key: "gradle"
 paths:
 - .gradle/

stages:
  - test
  - release

lintCheck:
  stage: test
  script:
    - ./gradlew -Pci --console=plain lint -PbuildDir=lint --priority low

unitTest:
  stage: test
  script:
    - ./gradlew -Pci --console=plain test --priority low

instrumentTest:
  stage: test
  script:
    - start_emulator.sh
    - ./gradlew -Pci --console=plain connectedAndroidTest --priority low

release:
  stage: release
  script:
    - echo $KEYSTORE | base64 -d > my.keystore
    - ./gradlew assembleRelease
      -Pandroid.injected.signing.store.file=$(pwd)/my.keystore
      -Pandroid.injected.signing.store.password=android
      -Pandroid.injected.signing.key.alias=androiddebugkey
      -Pandroid.injected.signing.key.password=android
      --priority low
```

A Gitlab CICD variable named `KEYSTORE` is used to sign the APK. Content of variable is base64 encode of the keystore file. You can use your own signing configuration.

