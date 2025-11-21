# User Stories

## US-001 View Webpage

**As a** streaming engineer
**I want to** open the stream-view application in a web browser
**So that** I can check the details of a video stream based on its manifest URL

### Acceptance criteria
- [ ] The stream-view application can run as a web service either on the user's machine or a cloud server
- [ ] It should be possible to build the application without any knowledge of the application code
- [ ] The application should use a clean but modern user interface design
- [ ] The web application should have one single page
- [ ] The Realitech logotype should be present in the top left corner of the web page (source: `assets/images/realitech-logo.svg`)
- [ ] There should be no authentication or login required to run the web application

## US-002 View HLS stream information

**As a** streaming engineer
**I want to** insert a URL to a HLS stream manifest into a text field and press a button called "View"
**So that** I can view the details of the HLS stream

### Acceptance Criteria
- [ ] The application should validate that the manifest is well-formed, including the suffix .m3u8
- [ ] If the URL is not found or will not load, then a helpful error message should be presented to the user
- [ ] When the user clicks the "View" button, then underneath the URL and View button, the following information about the stream should be presented:
  - [ ] The number of bitrates and information about each bitrate level
  - [ ] Information about audio tracks, subtitles and thumbnails tracks
  - [ ] Information about any DRM encryption used in the stream

## US-003 View DASH stream information

**As a** streaming engineer
**I want to** insert a URL to a DASH stream manifest into a text field and press a button called "View"
**So that** I can view the details of the DASH stream

### Acceptance Criteria
- [ ] The application should validate that the manifest is well-formed, including the suffix .mpd
- [ ] When the user clicks the "View" button, then underneath the URL and View button, the following information about the stream should be presented:
  - [ ] The number of bitrates and information about each bitrate level
  - [ ] Information about audio tracks, subtitles and thumbnails tracks
  - [ ] Information about any DRM encryption used in the stream

## US-004 View SCTE information in stream

**As a** streaming engineer
**I want to** view information about SCTE-35 in the stream
**So that** I can see advertising-related information about the stream

### Acceptance Criteria
- [ ] The SCTE information presented to the user should include:
   - [ ] Splice commands
   - [ ] PTS timestamp
   - [ ] Pre-roll time
   - [ ] Out-of-network indicator
   - [ ] Return indicator
   - [ ] Unique Program ID (UPID)
   - [ ] Segmentation descriptors
   - [ ] Event ID
   - [ ] Auto return flag
   - [ ] Break duration


## US-005 View information about the video content

**As a** streaming engineer
**I want to** view information about the video fragments
**So that** I can see the details of the video stream

### Acceptance Criteria
- [ ] The information should include:
    - [ ] Container format
    - [ ] Fragment Duration
    - [ ] Bitrate
    - [ ] File size
    - [ ] Codec
    - [ ] Profile and Level
    - [ ] Resolution
    - [ ] Frame rate
    - [ ] Bit rate
    - [ ] Colour space
- [ ] It should be possible to get the information no matter whether the video stream is encrypted for DRM or not.
- [ ] The web application should download between one and ten video fragments for the analysis.
- [ ] The information should be presented in a multi-column table with:
   - [ ] Information item (e.g. "Codec")
   - [ ] Value
- [ ] For information such as video bitrate levels, use three columns with:
   - [ ] Name or number of bitrate level
   - [ ] Name of information item, e.g. "Resolution"
   - [ ] Value of parameter

## US-006 Application operation

**As a** Application operations engineer
**I want to** have support maintaining the application
**So that** I can deploy, start, stop and maintain the application

### Acceptance Criteria
- [ ] Appropriate documentation for deploying, starting and stopping the application must be available.
- [ ] There should be documentation which describes the application structure, including file and folder structure.

# User Interface Requirements
- [ ] A modern-looking UI design should be used for the application.


# Technical Requirements
 - [ ] TR-001: It should be possible to run the application in a container, either using Docker or something similar.
 - [ ] TR-002: It should be possible to run the application without a container during development and test.
 - [ ] TR-003: All environment requirements and dependencies for a Macbook should be confirmed before the development starts.
 - [ ] TR-004: It should be possible for the manifest URLs to include query parameters, which means that the validation should take into account that only the endpoint part of the URL should end with .mpd or .m3u8. Validation should include ensuring that query parameters are well-formed and syntactically valid.

# Test requirements
- [ ] All test data for stream manifest URLs should be saved in a separate file so that they can be updated without touching any code or test case.
- [ ] There should be some basic UI testing using some framework like Playwrite to ensure the user interface design conforms to modern UI design standards.
 
# Test Data
The following URLs can be used for building tests of the application:
| SOURCE | NAME | TYPE | DRM | URL |
|--------|------|------|-----|-----|
| BBC | BBC Two | DASH Live | No | https://vs-cmaf-push-uk-live.akamaized.net/x=4/i=urn:bbc:pips:service:bbc_two_hd/pc_hd_abr_v2.mpd |
| BBC | BBC News | DASH Live | No | https://pub-c4-b8-eqsl-bbc.live.bidi.net.uk/vs-cmaf-push-uk/x=4/i=urn:bbc:pips:service:bbc_news_channel_hd/pc_hd_abr_v2.mpd |
| Radiant | Radiant | HLS Live | No | https://www.radiantmediaplayer.com/media/rmp-segment/bbb-abr-aes/playlist.m3u8 |
| Shaka | Angel One | DASH VOD | Widevine | https://storage.googleapis.com/shaka-demo-assets/sintel-widevine/dash.mpd |
| Shaka | Sintel | DASH VOD | Widevine | https://storage.googleapis.com/shaka-demo-assets/sintel-widevine/dash.mpd |
| Shaka | Live sim | DASH Live | Playready | https://livesim2.dashif.org/livesim2/drm_EZDRM-1-key-cbcs/testpic_2s/Manifest.mpd |


