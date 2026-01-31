# Building ivxv tools (Ubuntu / WSL)

This document describes how to build the Java-based ivxv tools such as
processor, auditor, and key on Ubuntu or WSL.

The build system uses Makefiles that invoke a pinned Gradle version located
under `common/external` and runs Gradle in offline mode by default.

## Requirements

- Ubuntu or WSL2
- JDK 21
- make
- wget
- unzip

## Install Java 21

```bash
sudo apt update
sudo apt install -y openjdk-21-jdk
````

## Set Java environment variables

```bash
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

## Verify the installation

```bash
java -version
javac -version
```

## Checkout

```bash
git clone https://github.com/valimised/ivxv.git
cd ivxv
```

## Initialize submodules

```bash
make external
```

## Gradle setup

The Makefiles expect Gradle 8.11 to be available at the following path:

```
common/external/gradle-8.11/bin/gradle
```

Download and install Gradle into the expected location.

```bash
mkdir -p common/external
cd common/external
wget https://services.gradle.org/distributions/gradle-8.11-bin.zip
unzip gradle-8.11-bin.zip
rm gradle-8.11-bin.zip
mkdir -p java
cd ../..
```

## First build (populate dependency cache)

The Makefiles invoke Gradle with the options `-g=common/external/java`
and `--offline`.

On a clean checkout, the dependency cache under `common/external/java` is empty.
Before using Makefile targets, Gradle must be run once without offline mode to
download all dependencies.

Run the following command to populate the cache and build the processor tool.

```bash
common/external/gradle-8.11/bin/gradle \
  -g=common/external/java \
  -p processor \
  clean build installDist \
  --warning-mode all \
  --refresh-dependencies
```

## Build tools using the Makefile

After the dependency cache has been populated, the tools can be built using the
Makefile targets.

```bash
make processor
make auditor
make key
```

## Executables

The tools are built as Gradle application distributions.

### Processor

Executable location:

```
processor/build/install/processor/bin/processor
```

Run:

```bash
./processor/build/install/processor/bin/processor --help
```

### Auditor

Executable location:

```
auditor/build/install/auditor/bin/auditor
```

### Key

Executable location:

```
key/build/install/key/bin/key
```

## Troubleshooting

### invalid source release: 21

Java 21 is required. Ensure that `JAVA_HOME` points to
`/usr/lib/jvm/java-21-openjdk-amd64` and that both `java` and `javac`
are taken from that JDK.

### No cached version available for offline mode

The dependency cache under `common/external/java` is empty.
Run the first Gradle build without offline mode to populate the cache.

### gradle: command not found

Gradle 8.11 is not installed under `common/external`.
Download and extract it as described in the Gradle setup section.


