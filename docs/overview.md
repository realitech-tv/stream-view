# Overview of the stream-view application

The stream-view application is an attempt to find some good practices for creating applications using Claude Code, while providing something which is useful for people working with streaming video.

The application we are trying to build is a video stream analyser, which takes as input a manifest URL to a video stream, and with this outputs technical information about the video stream. It should be possible to use this with both HLS and DASH manifests, and irrespective of whether the video is encrypted or not. The application will not attempt to play the video - just output information about the stream.

The requirements for this application will be relatively open, that is, we do not specify any particular technology stack. Instead, we will see what Claude Code recommends for this particular application. The requirements will be specified in a separate document, part of which will be user stories, part of which will be technical requirements.

The goal is to provide the application in some form of container, so that anyone who has access to the Github repository can download the code and get it running on any machine. Also, the Github repository is by design set as public which means that anyone can read and download from the repository. Only the edit/write permissions are protected.

This project will be extra documented to give a better insight into how Claude Code can be used to empower software developers. This includes prompts and responses generated outside Claude Code. We will try to keep things as much as possible within the Claude Code environment.

- **Author**: Nils Hagner
- **Company**: Realitech Limited
- **Copyright**: 2025 Realitech Limited