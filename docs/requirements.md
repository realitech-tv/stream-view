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
- [ ] The Realitech logotype should be present in the top left corner of the web page
- [ ] There should be no authentication or login required to run the web application

## US-002 View HLS stream information

**As a** streaming engineer
**I want to** insert a URL to a HLS stream manifest into a text field and press a button called "View"
**So that** I can view the details of the HLS stream

### Acceptance Criteria
- [ ] The application should validate that the manifest is well-formed, including the suffix .m3u8
- [ ] When the user clicks the "View" button, then underneath the URL and View button, the following information about the stream should be presented