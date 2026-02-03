# ivxv-build
This project aims to provide a working build environment, automated test suites, and updated documentation for the IVXV e-voting system, overcoming the technical hurdles and outdated instructions found in the official repository.

The current state of the ivxv repository https://github.com/valimised/ivxv strongly suggests a formal or compliance-driven publication rather than an actively maintained development project.

The official build documentation is inconsistent and outdated. It refers to Java 11 and Go 1.9, while the current codebase requires Gradle 8.11 and compiles Java sources with --release 21. Following the documented instructions leads to immediate build failures on a clean system. Key steps required to build the project, such as the initial non-offline Gradle invocation to populate the dependency cache, are not documented at all and must be reverse-engineered from Makefiles and error messages.

The make external target is misleading. It only initializes a documentation submodule and does not fetch required build tools or external dependencies, despite the name and documentation implying otherwise. As a result, a clean clone is not buildable without manual intervention.

During the build process and initial code inspection, there are numerous indicators of stagnation: deprecated APIs in active use, unused code paths, and warnings that appear to have been ignored for a long time. This further reinforces the impression that the repository is not under continuous, disciplined maintenance.

Regarding repository activity: the ivxv GitHub repository shows little or no visible contribution activity because it is effectively a mirror or periodic dump, not the primary development location. Commits are sparse, often batched, and do not reflect day-to-day development. This is why the contribution graph you expect is either empty, flat, or difficult to find. In contrast, personal or actively developed repositories show a dense activity graph because real development happens there.

Taken together, the build friction, outdated documentation, lack of automation, and low visible activity give the impression of a repository that exists to satisfy publication or transparency requirements, rather than to support external developers or encourage independent technical scrutiny.

# note on test data
This repository contains test ballots and signatures. Some of these files contain real personal data (names and Estonian personal codes) from contributors who have explicitly consented to this for audit purposes. We are working on providing fully synthetic (mocked) datasets in the future. See NOTICE.txt for details.

# disclaimer
This is an independent research project. It is not affiliated with the Estonian State Electoral Office. Use these tools at your own risk.