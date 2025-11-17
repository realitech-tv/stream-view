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
 - [ ] It should be possible to run the application in a container, either using Docker or something similar.
 - [ ] It should be possible to run the application without a container during development and test.
 - [ ] All environment requirements and dependencies for a Macbook should be confirmed before the development starts.

# Test requirements
- [ ] All test data for stream manifest URLs should be saved in a separate file so that they can be updated without touching any code or test case.
- [ ] There should be some basic UI testing using some framework like Playwrite to ensure the user interface design conforms to modern UI design standards.
 
# Test Data
The following URLs can be used for building tests of the application:
| SOURCE | NAME | TYPE | DRM | URL |
|--------|------|------|-----|-----|
| BBC | BBC Two | DASH Live | No | https://vs-cmaf-push-uk-live.akamaized.net/x=4/i=urn:bbc:pips:service:bbc_two_hd/pc_hd_abr_v2.mpd |
| BBC | BBC News | DASH Live | No | https://pub-c4-b8-eqsl-bbc.live.bidi.net.uk/vs-cmaf-push-uk/x=4/i=urn:bbc:pips:service:bbc_news_channel_hd/pc_hd_abr_v2.mpd |
| ITV | ITV1 | DASH Live | Yes | https://csm-e-ceitvaeuw1lived-0b7e0a49f383f6ce6.play.dar.itv.com/csm/extlive/itv01,itv1-dotcom-dash-prodb-multicdn.mpd?source=simulcast&size=pattern&supertag=dflt,sim&hmod=141.0.0.0&service=itv.x&generic=c8cfc2da-8106-4104-833b-de6c7e2f204b&pv=browser.4.1&yo.d.upi=true&yo.ap=https%3A%2F%2Fdar-live-blue-irdeto-ms.akamai.content.itv.com%2Fprdsda%2F&default=defaultpattern&dm=4eb3eecd-b3fe-4daf-afda-12e362283198&vfunapod=true&yo.t.jt=500&yo.up=https%3A%2F%2Fdar-live-blue-irdeto-ms.akamai.content.itv.com%2Fjwt%2FeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6InByZEZ6In0.eyJpcCI6IjgyLjE2LjEyMy4xNjciLCJwYXRoIjoiL3BsYXlvdXQvY29tbW9uL2l0djEvY2VuYy5pc21sIiwiZXhwIjoxNzYzNDAxNzc4LCJtaXAiOiJsb2ciLCJzdWIiOiI0ZWIzZWVjZC1iM2ZlLTRkYWYtYWZkYS0xMmUzNjIyODMxOTgiLCJzaWQiOiI5MWMwNzU0MS1hNWYzLTQ0ODMtODQyYS1jMWIwNmI0YzIzMTIifQ.LEYf4T5jtsqGBGH5R0hTSEVzPY90hAGgyeHaZAfsYZQ%2Fplayout%2Fcommon%2Fitv1%2Fcenc.isml%2F&tppm=x&pm=premium&random=9874345055&yo.eb.fb=aHR0cHM6Ly9saXZlLWJsdWUtaXJkZXRvLW1zLmFrYW1haS5jb250ZW50Lml0di5jb20vand0L2V5SjBlWEFpT2lKS1YxUWlMQ0poYkdjaU9pSklVekkxTmlJc0ltdHBaQ0k2SW5CeVpFWjZJbjAuZXlKcGNDSTZJamd5TGpFMkxqRXlNeTR4TmpjaUxDSndZWFJvSWpvaUwzQnNZWGx2ZFhRdlkyOXRiVzl1TDJsMGRqRXZZMlZ1WXkxdWIyUmhjaTVwYzIxc0lpd2laWGh3SWpveE56WXpOREF4TnpjNExDSnRhWEFpT2lKc2IyY2lMQ0p6ZFdJaU9pSTBaV0l6WldWalpDMWlNMlpsTFRSa1lXWXRZV1prWVMweE1tVXpOakl5T0RNeE9UZ2lMQ0p6YVdRaU9pSTVNV013TnpVME1TMWhOV1l6TFRRME9ETXRPRFF5WVMxak1XSXdObUkwWXpJek1USWlmUS5tbmliMFljaVFHRmNZSllRLXRkcnJzSV9BYzVJelVUUXc4Y0VRLUt5RzZrL3BsYXlvdXQvY29tbW9uL2l0djEvY2VuYy1ub2Rhci5pc21sL2RvdGNvbS5tcGQ%3D&area=itvplayer.simulcast.simadreplacement&rh=x&yo.br=false&subserv=x&us=ano&site=itv&osver=10.15.7&yo.av=3&conttier=x&chanbrand=itv1&os=macos&yo.tracking=true&plfcid=simadreplacement&plist=simadreplacement&yo.ad=false&yo.ch=true&profile=adult&player=html5.desktop&hman=chrome&viewid=0.c8cfc2da-8106-4104-833b-de6c7e2f204b&hdevid=x&tdur=21600&tparts=1&arp=x&yo.oh=Y3NtLWUtaXR2LWViLnBsYXkuZGFyLml0di5jb20= |
| ITV | ITV2 | DASH Live | Yes | https://csm-e-ceitvaeuw1lived-0f1bec7786a7f8a85.play.dar.itv.com/csm/extlive/itv01,itv2-dotcom-dash-prodb-multicdn.mpd?source=simulcast&size=pattern&supertag=dflt,sim&hmod=141.0.0.0&service=itv.x&generic=3cede13c-7aa1-4e7b-928a-4cdc22a6686b&pv=browser.4.1&yo.d.upi=true&yo.ap=https%3A%2F%2Fdar-live-blue-irdeto-ms.akamai.content.itv.com%2Fprdsda%2F&default=defaultpattern&dm=4eb3eecd-b3fe-4daf-afda-12e362283198&vfunapod=true&yo.t.jt=500&yo.up=https%3A%2F%2Fdar-live-blue-irdeto-ms.akamai.content.itv.com%2Fjwt%2FeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6InByZEZ6In0.eyJpcCI6IjgyLjE2LjEyMy4xNjciLCJwYXRoIjoiL3BsYXlvdXQvY29tbW9uL2l0djIvY2VuYy5pc21sIiwiZXhwIjoxNzYzNDAxODc2LCJtaXAiOiJsb2ciLCJzdWIiOiI0ZWIzZWVjZC1iM2ZlLTRkYWYtYWZkYS0xMmUzNjIyODMxOTgiLCJzaWQiOiJjYmQxZDk1Mi0yMGYzLTRlYjEtYjk0OC0xYTM5YTQ1MjhkZGMifQ.q6ElEz6sjApl6_i8KA20LP7Ljp2W009LiHf3C_dNVsQ%2Fplayout%2Fcommon%2Fitv2%2Fcenc.isml%2F&tppm=x&pm=premium&random=9040487571&yo.eb.fb=aHR0cHM6Ly9saXZlLWJsdWUtaXJkZXRvLW1zLmFrYW1haS5jb250ZW50Lml0di5jb20vand0L2V5SjBlWEFpT2lKS1YxUWlMQ0poYkdjaU9pSklVekkxTmlJc0ltdHBaQ0k2SW5CeVpFWjZJbjAuZXlKcGNDSTZJamd5TGpFMkxqRXlNeTR4TmpjaUxDSndZWFJvSWpvaUwzQnNZWGx2ZFhRdlkyOXRiVzl1TDJsMGRqSXZZMlZ1WXkxdWIyUmhjaTVwYzIxc0lpd2laWGh3SWpveE56WXpOREF4T0RjMkxDSnRhWEFpT2lKc2IyY2lMQ0p6ZFdJaU9pSTBaV0l6WldWalpDMWlNMlpsTFRSa1lXWXRZV1prWVMweE1tVXpOakl5T0RNeE9UZ2lMQ0p6YVdRaU9pSmpZbVF4WkRrMU1pMHlNR1l6TFRSbFlqRXRZamswT0MweFlUTTVZVFExTWpoa1pHTWlmUS5PSUVJN1ZrRjFQZEZtd3VhSWhWRGItVVFuQ2hCakZCQXA3TTRlSDY1b1VFL3BsYXlvdXQvY29tbW9uL2l0djIvY2VuYy1ub2Rhci5pc21sL2RvdGNvbS5tcGQ%3D&area=itvplayer.simulcast.simadreplacement&rh=x&yo.br=false&subserv=x&us=ano&site=itv&osver=10.15.7&yo.av=3&conttier=x&chanbrand=itv2&os=macos&yo.tracking=true&plfcid=simadreplacement&plist=simadreplacement&yo.ad=false&yo.ch=true&profile=adult&player=html5.desktop&hman=chrome&viewid=0.3cede13c-7aa1-4e7b-928a-4cdc22a6686b&hdevid=x&tdur=21600&tparts=1&arp=x&yo.oh=Y3NtLWUtaXR2LWViLnBsYXkuZGFyLml0di5jb20= |
| Freevee | Blitz | DASH VOD | Yes | https://abfeed3aaaaaaaambiujbb4u6pxy3.s3-iad-2.cf.dash.row.aiv-cdn.net/dm/3$0ChoIAiAfMAFSBoDAAoHwA3oDgLgXggEBAYgBAhgB/ffa5/c9ea/7737/4fcc-b1e9-958ef7b8da49/2aebbb07-a91e-40aa-8175-d91ef2acaf1a_corrected.mpd?amznDtid=AOAGZA014O5RE&encoding=segmentBase |
| Channel4 | Hollyoaks | DASH VOD | Yes | https://ak-jos-c4assets-com.akamaized.net/CH4_08_02_900_76933_134_3_176286419941369/CH4_08_02_900_76933_134_3_176286419941369_J01.ism/stream.mpd?c3.ri=14624474022417338684&mpd_segment_template=time&filter=%28type%3D%3D%22video%22%26%26%28%28DisplayHeight%3E%3D288%29%26%26%28DisplayHeight%3C%3D576%29%29%29%7C%7Ctype%21%3D%22video%22&ts=1763380931&e=600&st=eu9GjsZsIfVfPYwVV0qihmPzFvXuW0_P0OaaTAJ_4Iw |
| Freevee | Euronews| HLS Live | Yes | https://abfeed3aaaaaaaamf5vasuv2qg7ov.emt-cf.live.pv-cdn.net/DUB/725666c82c534d4fabb3b69212bd7bf7/v1/master/159325541587/imdb_wurl_eu_amzn1_dv_live_csid_581eb81b-158d-4b2a-9214-dc8ae4ce1c9f_us-west-2_dub_hls_h264_none_stereo/live/clients/hls/enc/fo7z7fu9wm/out/v1/0ef37854c75842d39294ccd104dded60/fp.m3u8?aws.sessionId=7b09c3d7-0221-4665-b8e2-a4d93aaf0fb8 |
| Amazon Prime | Playdate | HLS VOD | Yes | https://s3-dub-ww.cf.hls.row.aiv-cdn.net/dm/3$0CqQHCAEgHzABWgQI0IYDggEBAYgBBLoBCAiA-gEQwJoMugEICID0AxDgxlvCAQgIgOgHEODGW8IBCAiA9AMQwJoMwgEICID6ARDQhgPKASIKDtin2YTYudix2KjZitipEg5hci1hZV9kaWFsb2dfMBgEygEdCgnEjGXFoXRpbmESDmNzLWN6X2RpYWxvZ18wGBXKARsKB0RldXRzY2gSDmRlLWRlX2RpYWxvZ18wGBnKARsKB0VuZ2xpc2gSDmVuLXVzX2RpYWxvZ18wGCXKAS4KGUVzcGHDsW9sIChMYXRpbm9hbcOpcmljYSkSD2VzLTQxOV9kaWFsb2dfMBgnygEmChJFc3Bhw7FvbCAoRXNwYcOxYSkSDmVzLWVzX2RpYWxvZ18wGC3KASYKEkZyYW7Dp2FpcyAoQ2FuYWRhKRIOZnItY2FfZGlhbG9nXzAYO8oBJgoSRnJhbsOnYWlzIChGcmFuY2UpEg5mci1mcl9kaWFsb2dfMBg9ygEmChLgpLngpL_gpKjgpY3gpKbgpYASDmhpLWluX2RpYWxvZ18wGEPKARoKBk1hZ3lhchIOaHUtaHVfZGlhbG9nXzAYRcoBHAoISXRhbGlhbm8SDml0LWl0X2RpYWxvZ18wGEjKASMKD-CyleCyqOCzjeCyqOCyoRIOa24taW5fZGlhbG9nXzAYTcoBJgoS4LSu4LSy4LSv4LS-4LSz4LSCEg5tbC1pbl9kaWFsb2dfMBhSygEaCgZQb2xza2kSDnBsLXBsX2RpYWxvZ18wGF3KAScKE1BvcnR1Z3XDqnMgKEJyYXNpbCkSDnB0LWJyX2RpYWxvZ18wGF7KASMKD-CupOCuruCuv-CutOCvjRIOdGEtaW5fZGlhbG9nXzAYasoBJgoS4LCk4LGG4LCy4LGB4LCX4LGBEg50ZS1pbl9kaWFsb2dfMBhrygEcCghUw7xya8OnZRIOdHItdHJfZGlhbG9nXzAYbdoBBgignAEQA9oBBgiA-gEQA9oBBgiArBsQBdoBBgiAlCMQBdoBBgiA7gUQBNoBBgiA6AcQBNoBBgiA3AsQBNoBBgiA1g0QBNoBBgiA0A8QBNoBBgiAuBcQBNoBBgiAoB8QBNoBBgiAiCcQBOoBRApAYzExN2ExMWJiNGU1MmEzYmM4YmQwOWY4YjczYjY4NmE1M2U5Y2NmZTU5OTZlMTk3Mzc2MmQzMGFkNTcwZTlhORAG8gEOZW4tdXNfZGlhbG9nXzAYAQ/d84c/b16a/9743/4c99-9a88-6d3493021033/6d208581-8355-4acf-a955-b9b410af26ff_v4.m3u8 |
| Channel4 | 4 | HLS Live | Yes | https://csm-e-cec4prdlgblonlive-82278107.bln1.yospace.com/csm/extlive/channelfour01,c4-v3-hls.m3u8?yo.ac=false&yo.br=false&siteSectionId=watchlive.channel4.com/C4&GUID=ba57a52f-a029-417f-9941-746491ab98e8&yo.av=4&targetedAdvertising=accepted&_fw_cookie_consent=1&yo.oh=Y3NtLWUtYzR1ay1lYi50bHMxLnlvc3BhY2UuY29t |
| Channel4 | Hollyoaks | HLS VOD | Yes | https://ak-jos-c4assets-com.akamaized.net/CH4_08_02_900_76933_135_2_176279784878071/CH4_08_02_900_76933_135_2_176279784878071_J01.ism/stream.m3u8?c3.ri=14639392197130879226&filter=%28type%3D%3D%22video%22%26%26%28%28DisplayHeight%3E%3D288%29%26%26%28DisplayHeight%3C%3D576%29%29%29%7C%7Ctype%21%3D%22video%22&ts=1763381786&e=600&st=QxA_0HpfZnK8G8x-ed3xVcw6l2gd0NoMQ3zVryu3NJU |


